import tkinter as tk
from tkinter import messagebox

# --- Game state ---
root = tk.Tk()
root.title("Tic Tac Toe")

buttons = []             # list of 9 button widgets
current_player = "X"     # "X" or "O"
game_over = False        # set True when someone wins or tie

# winning combinations (indices into buttons list)
WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6)              # diagonals
]

# --- Functions ---
def check_winner():
    """Check for a winner. If found, highlight and announce."""
    global game_over
    for a, b, c in WIN_COMBOS:
        t1 = buttons[a]["text"]
        t2 = buttons[b]["text"]
        t3 = buttons[c]["text"]
        if t1 == t2 == t3 != "":
            # highlight winning buttons
            buttons[a].config(bg="lightgreen")
            buttons[b].config(bg="lightgreen")
            buttons[c].config(bg="lightgreen")

            messagebox.showinfo("Tic Tac Toe", f"Player {t1} wins!")
            game_over = True
            disable_all_buttons()
            return

    # If no winner, check for tie
    if all(btn["text"] != "" for btn in buttons):
        messagebox.showinfo("Tic Tac Toe", "It's a tie!")
        game_over = True
        disable_all_buttons()

def disable_all_buttons():
    for btn in buttons:
        btn.config(state="disabled")

def make_move(index):
    """Handle a player's move when they click a button."""
    global current_player, game_over
    if game_over:
        return

    btn = buttons[index]
    if btn["text"] == "":
        btn.config(text=current_player)
        check_winner()
        # switch player only if game still going
        if not game_over:
            current_player = "O" if current_player == "X" else "X"
            status_label.config(text=f"Turn: {current_player}")

def restart_game():
    """Reset board to initial state."""
    global current_player, game_over
    current_player = "X"
    game_over = False
    status_label.config(text=f"Turn: {current_player}")
    for btn in buttons:
        btn.config(text="", state="normal", bg="SystemButtonFace")

# --- UI layout ---
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

for i in range(9):
    btn = tk.Button(frame,
                    text="",
                    font=("Helvetica", 24),
                    width=4,
                    height=2,
                    command=lambda i=i: make_move(i))
    btn.grid(row=i//3, column=i%3, padx=3, pady=3)
    buttons.append(btn)

controls = tk.Frame(root)
controls.pack(pady=(0,10))

status_label = tk.Label(controls, text=f"Turn: {current_player}", font=("Helvetica", 12))
status_label.pack(side="left", padx=(0,10))

restart_btn = tk.Button(controls, text="Restart", command=restart_game)
restart_btn.pack(side="left")

root.mainloop()
