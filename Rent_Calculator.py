#### we are making our first python mini projesct its bacisally we caled rend calculator in python
# what we need 1.input form user about total rent, total rent,electicity bills,charge  per unit
# output total amount you have to pay
#person living in room 

import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        rent = int(rent_entry.get())
        food = int(food_entry.get())
        bills = int(bills_entry.get())
        units = int(units_entry.get())
        persons = int(persons_entry.get())

        total_bill = bills * units
        output = (rent + food + total_bill) // persons

        result_label.config(text=f"Each person pays: {output}")

    except ValueError:
        messagebox.showerror("Error", "Please enter numbers only")

# Main window
root = tk.Tk()
root.title("Rent & Bill Calculator")
root.geometry("350x350")

# Title
title = tk.Label(root, text="Monthly Expense Calculator", font=("Arial", 14, "bold"))
title.pack(pady=10)

# Rent
tk.Label(root, text="Total Rent:").pack()
rent_entry = tk.Entry(root)
rent_entry.pack()

# Food
tk.Label(root, text="Total Food Price:").pack()
food_entry = tk.Entry(root)
food_entry.pack()

# Electricity Bills
tk.Label(root, text="Electricity Units Used:").pack()
bills_entry = tk.Entry(root)
bills_entry.pack()

# Charge per unit
tk.Label(root, text="Charge per Unit:").pack()
units_entry = tk.Entry(root)
units_entry.pack()

# Number of Persons
tk.Label(root, text="Number of Persons:").pack()
persons_entry = tk.Entry(root)
persons_entry.pack()

# Calculate button
calculate_btn = tk.Button(root, text="Calculate", command=calculate)
calculate_btn.pack(pady=15)

# Result label
result_label = tk.Label(root, text="Each person pays: ---", font=("Arial", 12))
result_label.pack()

root.mainloop()
