# ---------------------------------------------
# STUDENT MANAGEMENT SYSTEM (OOP + ALL CONCEPTS)
# ---------------------------------------------
import tkinter as tk
from tkinter import messagebox, ttk

# 1️⃣ Tuple (fixed data)
DEFAULT_SUBJECTS = ("Math", "Science", "English")

# 2️⃣ Using Set to store unique IDs
used_ids = set()


# 3️⃣ OOP Class
class Student:
    def __init__(self, student_id, name, marks_dict):
        self.student_id = student_id
        self.name = name
        self.marks = marks_dict   # Dictionary of subject → marks

    def total_marks(self):
        return sum(self.marks.values())

    def average(self):
        return self.total_marks() / len(self.marks)


# 4️⃣ Student Manager
class StudentManager:
    def __init__(self):
        self.students = []  # list of Student objects

    def add_student(self, student):
        self.students.append(student)

    def search_recursive(self, student_list, target_id, index=0):
        if index == len(student_list):
            return None
        if student_list[index].student_id == target_id:
            return student_list[index]
        return self.search_recursive(student_list, target_id, index + 1)

    def show_all(self):
        for s in self.students:
            print(f"ID: {s.student_id} | Name: {s.name} | Avg: {s.average()}")


# ORIGINAL MAIN PROGRAM (CLI)
def main():
    manager = StudentManager()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. Search Student by ID")
        print("3. Show All Students")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            student_id = input("Enter Student ID: ")

            if student_id in used_ids:
                print("❌ ID already used!")
                continue
            used_ids.add(student_id)

            name = input("Enter Student Name: ")

            marks = {}
            for subject in DEFAULT_SUBJECTS:
                marks[subject] = int(input(f"Enter marks for {subject}: "))

            student = Student(student_id, name, marks)
            manager.add_student(student)
            print("✔ Student Added Successfully")

        elif choice == "2":
            search_id = input("Enter ID to search: ")
            result = manager.search_recursive(manager.students, search_id)

            if result:
                print("\n🎉 Student Found!")
                print(f"ID: {result.student_id}")
                print(f"Name: {result.name}")
                print(f"Marks: {result.marks}")
                print(f"Total: {result.total_marks()}")
                print(f"Average: {result.average()}")
            else:
                print("❌ Student not found")

        elif choice == "3":
            manager.show_all()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")


# ------------------------------
# ⭐ ADDING GUI (Your code stays same!)
# ------------------------------

manager = StudentManager()  # shared manager object

def gui_add_student():
    win = tk.Toplevel(root)
    win.title("Add Student")
    win.geometry("300x350")

    tk.Label(win, text="Student ID").pack()
    id_entry = tk.Entry(win)
    id_entry.pack()

    tk.Label(win, text="Student Name").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    mark_entries = {}
    for subject in DEFAULT_SUBJECTS:
        tk.Label(win, text=f"{subject} Marks").pack()
        e = tk.Entry(win)
        e.pack()
        mark_entries[subject] = e

    def save():
        sid = id_entry.get()
        name = name_entry.get()

        if sid in used_ids:
            messagebox.showerror("Error", "ID already used")
            return
        
        used_ids.add(sid)

        marks = {}
        try:
            for sub in DEFAULT_SUBJECTS:
                marks[sub] = int(mark_entries[sub].get())
        except:
            messagebox.showerror("Error", "Marks must be numbers")
            return

        student = Student(sid, name, marks)
        manager.add_student(student)
        messagebox.showinfo("Success", "Student Added")
        win.destroy()

    tk.Button(win, text="Save", command=save).pack(pady=10)


def gui_search_student():
    win = tk.Toplevel(root)
    win.title("Search Student")
    win.geometry("300x200")

    tk.Label(win, text="Enter Student ID").pack()
    id_entry = tk.Entry(win)
    id_entry.pack()

    def search():
        sid = id_entry.get()
        result = manager.search_recursive(manager.students, sid)

        if result:
            msg = (
                f"ID: {result.student_id}\n"
                f"Name: {result.name}\n"
                f"Marks: {result.marks}\n"
                f"Total: {result.total_marks()}\n"
                f"Average: {result.average()}"
            )
            messagebox.showinfo("Found", msg)
        else:
            messagebox.showerror("Not Found", "Student not found")

    tk.Button(win, text="Search", command=search).pack(pady=10)


def gui_show_all():
    win = tk.Toplevel(root)
    win.title("All Students")
    win.geometry("500x300")

    table = ttk.Treeview(win, columns=("ID","Name","Math","Science","English","Total","Average"), show="headings")

    for col in ("ID","Name","Math","Science","English","Total","Average"):
        table.heading(col, text=col)
        table.column(col, width=70)

    for s in manager.students:
        table.insert("", tk.END, values=(
            s.student_id, 
            s.name, 
            s.marks["Math"],
            s.marks["Science"],
            s.marks["English"],
            s.total_marks(),
            round(s.average(), 2)
        ))

    table.pack(fill=tk.BOTH, expand=True)


# ---- MAIN GUI WINDOW ----
root = tk.Tk()
root.title("Student Management System (GUI)")
root.geometry("300x300")

tk.Label(root, text="Student Management System", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Add Student", width=20, command=gui_add_student).pack(pady=5)
tk.Button(root, text="Search Student", width=20, command=gui_search_student).pack(pady=5)
tk.Button(root, text="Show All Students", width=20, command=gui_show_all).pack(pady=5)

tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=10)

root.mainloop()
