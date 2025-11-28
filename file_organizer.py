#!/usr/bin/env python3
"""
File Renamer & Organizer (MVP)
- Preview mode (dry-run)
- Apply mode
- Rule config via YAML or command-line flags
- Action logging for undo
- Optional folder watching (requires watchdog)

Usage examples:
  python file_organizer.py --config rules.yaml --preview
  python file_organizer.py --config rules.yaml --apply
  python file_organizer.py --src /path/to/folder --organize-by extension --apply
"""

import argparse
import shutil
import sys
import time
import yaml
import json
from pathlib import Path
from datetime import datetime
import logging

# Try import optional libs
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except Exception:
    WATCHDOG_AVAILABLE = False

LOG_DIR = Path(".file_organizer_logs")
LOG_DIR.mkdir(exist_ok=True)

# -------------------------
# Helpers
# -------------------------
def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def safe_move(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    # if dest exists, add suffix
    if dest.exists():
        base = dest.stem
        ext = dest.suffix
        i = 1
        while True:
            new = dest.with_name(f"{base}_{i}{ext}")
            if not new.exists():
                dest = new
                break
            i += 1
    shutil.move(str(src), str(dest))
    return dest

# -------------------------
# Core transforms
# -------------------------
def rename_pattern(path: Path, pattern: str, seq=None):
    """
    Pattern example: "{date}_{orig}" or "project_{seq}_{orig}"
    Supported placeholders:
      {orig} - original filename (without extension)
      {ext} - extension without dot
      {date} - YYYYMMDD
      {time} - HHMMSS
      {seq} - sequence number (if provided)
    """
    orig = path.stem
    ext = path.suffix.lstrip(".")
    ctx = {
        "orig": orig,
        "ext": ext,
        "date": datetime.now().strftime("%Y%m%d"),
        "time": datetime.now().strftime("%H%M%S"),
        "seq": f"{seq:03d}" if seq is not None else "",
    }
    name = pattern.format(**ctx)
    return f"{name}.{ext}" if ext else name

def organize_target(path: Path, mode: str):
    """
    mode: 'extension' | 'date' | 'type' (basic) or custom folder name
    """
    if mode == "extension":
        ext = path.suffix.lstrip(".").lower() or "no_ext"
        return Path(ext) / path.name
    if mode == "date":
        d = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y/%m/%d")
        return Path(d) / path.name
    # fallback: treat mode as fixed folder name
    return Path(mode) / path.name

# -------------------------
# Rule engine
# -------------------------
def process_folder(src: Path, rules: dict, preview=True):
    """
    rules example (from YAML):
    - match_ext: ['jpg','jpeg','png']
      action: rename
      pattern: "{date}_{orig}"
      target_folder: "Photos/{date}"
    - match_glob: "invoices/*.pdf"
      action: move
      target_folder: "Finance/Invoices"
    - match_ext: ['pdf']
      action: move
      organize_by: date
    """
    log_entries = []
    seq_counters = {}

    files = sorted([p for p in src.rglob("*") if p.is_file()])
    for i, p in enumerate(files, start=1):
        rel = p.relative_to(src)
        applied = False
        for r in rules:
            # match by extension
            if "match_ext" in r:
                if p.suffix.lstrip(".").lower() not in [e.lower() for e in r["match_ext"]]:
                    continue
            if "match_glob" in r:
                # glob match relative path
                if not rel.match(r["match_glob"]):
                    continue
            # matched — determine action
            action = r.get("action", "move")
            target_folder = r.get("target_folder")
            if action == "rename":
                pattern = r.get("pattern", "{date}_{orig}")
                key = r.get("seq_key", "default")
                seq_counters.setdefault(key, 0)
                seq_counters[key] += 1
                new_name = rename_pattern(p, pattern, seq=seq_counters[key])
                dest_rel = (Path(r.get("target_folder", "")) / new_name).as_posix()
            elif action == "move":
                organize_by = r.get("organize_by")
                if organize_by:
                    dest_rel = organize_target(p, organize_by).as_posix()
                elif target_folder:
                    dest_rel = (Path(target_folder) / p.name).as_posix()
                else:
                    dest_rel = p.name
            else:
                # unknown action
                continue

            dest_path = (src / Path(dest_rel)).resolve()
            entry = {"src": str(p.resolve()), "dest": str(dest_path), "timestamp": timestamp(), "rule": r}
            log_entries.append(entry)

            print(f"[MATCH] {p} -> {dest_path}")
            if not preview:
                # move/rename
                actual_dest = safe_move(p, dest_path)
                entry["actual_dest"] = str(actual_dest)
            applied = True
            break  # stop at first matching rule
        if not applied:
            # optionally default rule; skip for now
            pass

    return log_entries

# -------------------------
# Logging / Undo
# -------------------------
def write_log(entries, tag=None):
    if not entries:
        return None
    fname = LOG_DIR / f"log_{timestamp()}{('_'+tag) if tag else ''}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
    print(f"Actions logged to: {fname}")
    return fname

def undo_log(logfile):
    with open(logfile, "r", encoding="utf-8") as f:
        entries = json.load(f)
    # undo in reverse order
    for e in reversed(entries):
        src = Path(e.get("actual_dest") or e["dest"])
        orig = Path(e["src"])
        if src.exists():
            print(f"Restoring {src} -> {orig}")
            orig.parent.mkdir(parents=True, exist_ok=True)
            safe_move(src, orig)
        else:
            print(f"Cannot restore, not found: {src}")
    print("Undo complete.")

# -------------------------
# Watcher (optional)
# -------------------------
class FolderWatcher(FileSystemEventHandler):
    def __init__(self, src: Path, rules: dict, preview=False):
        self.src = src
        self.rules = rules
        self.preview = preview

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"New file detected: {event.src_path} — running rules")
        entries = process_folder(self.src, self.rules, preview=self.preview)
        if entries and not self.preview:
            write_log(entries, tag="watch")

# -------------------------
# CLI
# -------------------------
def parse_args():
    p = argparse.ArgumentParser(description="File Renamer & Organizer (MVP)")
    p.add_argument("--src", required=False, default=".", help="Source folder to operate on")
    p.add_argument("--config", required=False, help="YAML rules config file")
    p.add_argument("--preview", action="store_true", help="Show what will be done but don't move/rename")
    p.add_argument("--apply", action="store_true", help="Actually perform changes")
    p.add_argument("--watch", action="store_true", help="Watch folder and auto-apply on new files (requires watchdog)")
    p.add_argument("--undo-log", required=False, help="Path to a log json file to undo actions")
    return p.parse_args()

def load_rules(path):
    if not path:
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or []

def main():
    args = parse_args()
    src = Path(args.src).resolve()
    if args.undo_log:
        undo_log(args.undo_log)
        return

    rules = load_rules(args.config)
    preview_mode = args.preview or not args.apply

    if args.watch:
        if not WATCHDOG_AVAILABLE:
            print("watchdog not available. Install: pip install watchdog")
            return
        print(f"Watching {src} — preview={preview_mode}")
        event_handler = FolderWatcher(src, rules, preview=preview_mode)
        observer = Observer()
        observer.schedule(event_handler, str(src), recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        return

    entries = process_folder(src, rules, preview=preview_mode)
    if entries:
        logpath = write_log(entries, tag="dry" if preview_mode else "applied")
        if preview_mode:
            print("\nPreview mode — no changes made. To apply run with --apply")
        else:
            print("\nChanges applied.")
    else:
        print("No files matched the rules.")

if __name__ == "__main__":
    try:
        import yaml  # ensure yaml available
    except Exception:
        print("PyYAML required. Install with: pip install pyyaml")
        sys.exit(1)
    main()

