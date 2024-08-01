
from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
is_work_time = True
# ---------------------------- TIMER RESET ------------------------------- # 


def reset_timer():
    global reps
    reps = 0
    window.after_cancel(timer)
    title_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    check_marks.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- #


"""
Work Sessions: reps is odd (1, 3, 5, 7, etc.), indicating a work session.
Short Breaks: reps is even but not divisible by 8 (2, 4, 6, etc.), indicating a short break.
Long Breaks: reps is divisible by 8 (8, 16, 24, etc.), indicating a long break.
"""


def start_timer():
    global reps
    reps += 1

    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)
        title_label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        title_label.config(text="Short Break", fg=PINK)
    else:  # It starts a work session.
        count_down(WORK_MIN * 60)
        title_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


"""The count_down function calculates the minutes and seconds remaining.
count represents the total time in seconds
count_min is calculated by dividing 60 and taking the floor value to get the full minutes."""


def count_down(count):
    global reps, is_work_time

    # Calculate minutes and seconds
    count_min = math.floor(count / 60)
    count_sec = count % 60  # remainder seconds
    # Format seconds to always have two digits
    if count_sec < 10:  # dynamic typing, from int to string
        count_sec = f"0{count_sec}"

    # It updates the timer_text on the canvas with the formatted time.
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    # If the countdown is not finished (count > 0), it calls
    # window.after to continue the countdown after 1000 milliseconds (1 second).
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""  # this empty string will be used to store the check marks.
        """
        reps represents the total number of sessions (both work and breaks) completed.
        reps/2 gives the number of completed work sessions because each work session
        is followed by a break.
        math.floor ensures the result is an integer"""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✓"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
# window.minsize(width=500, height=300)
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="Timber", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
canvas.grid(column=1, row=1)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

# count_down(5)

start_button = Button(text="Start", font=(FONT_NAME, 12), highlightbackground=YELLOW, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", font=(FONT_NAME, 12), highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()
