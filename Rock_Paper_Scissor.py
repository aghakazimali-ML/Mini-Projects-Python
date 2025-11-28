# rock paper scissor game in python
# workflow:
# user chooses (rock/paper/scissor)
# computer chooses (random)
# result displayed
# animated "thinking..." effect

import tkinter as tk
import random

root = tk.Tk()
root.title("Rock Paper Scissor (Animated)")
root.geometry("480x480")
root.config(bg="#000000")

# ---------------------------------
# Animation: Computer "thinking..."
# ---------------------------------
def computer_thinking(callback):
    texts = ["Thinking.", "Thinking..", "Thinking..."]
    
    def animate(i=0):
        status_label.config(text=texts[i])
        if i < 2:
            root.after(400, animate, i + 1)
        else:
            callback()
    animate()

# ---------------------------------
# Main game logic (your logic)
# ---------------------------------
def play(user_choice):
    
    def after_thinking():
        computer_choice = random.choice(["rock", "paper", "scissor"])
        
        user_label.config(text=f"Your Choice: {user_choice}")
        comp_label.config(text=f"Computer Choice: {computer_choice}")
        
        # Tie
        if user_choice == computer_choice:
            result_label.config(text="Match Ties!", fg="yellow")
        
        # User = Rock
        elif user_choice == "rock":
            if computer_choice == "paper":
                result_label.config(text="Computer Wins!", fg="red")
            else:
                result_label.config(text="You Win!", fg="lightgreen")
        
        # User = Paper
        elif user_choice == "paper":
            if computer_choice == "rock":
                result_label.config(text="You Win!", fg="lightgreen")
            else:
                result_label.config(text="Computer Wins!", fg="red")
        
        # User = Scissor
        elif user_choice == "scissor":
            if computer_choice == "rock":
                result_label.config(text="Computer Wins!", fg="red")
            else:
                result_label.config(text="You Win!", fg="lightgreen")

    # Start animation then result
    computer_thinking(after_thinking)

# ---------------------------------
# GUI Layout
# ---------------------------------

title = tk.Label(root, text="Rock Paper Scissor", font=("Arial", 20, "bold"), bg="#1b1b1b", fg="white")
title.pack(pady=10)

status_label = tk.Label(root, text="Choose Your Move", font=("Arial", 16), bg="#1b1b1b", fg="white")
status_label.pack(pady=10)

# Choice buttons
btn_frame = tk.Frame(root, bg="#1b1b1b")
btn_frame.pack(pady=20)

rock_btn = tk.Button(btn_frame, text="Rock", width=10, font=("Arial", 14), command=lambda: play("rock"))
paper_btn = tk.Button(btn_frame, text="Paper", width=10, font=("Arial", 14), command=lambda: play("paper"))
scissor_btn = tk.Button(btn_frame, text="Scissor", width=10, font=("Arial", 14), command=lambda: play("scissor"))

rock_btn.grid(row=0, column=0, padx=10)
paper_btn.grid(row=0, column=1, padx=10)
scissor_btn.grid(row=0, column=2, padx=10)

# Output labels
user_label = tk.Label(root, text="Your Choice:", font=("Arial", 14), bg="#1b1b1b", fg="white")
user_label.pack(pady=5)

comp_label = tk.Label(root, text="Computer Choice:", font=("Arial", 14), bg="#1b1b1b", fg="white")
comp_label.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 18, "bold"), bg="#1b1b1b")
result_label.pack(pady=20)

root.mainloop()
