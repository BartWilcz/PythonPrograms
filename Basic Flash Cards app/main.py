BACKGROUND_COLOR = "#B1DDC6"

from tkinter import *
import pandas as pd
import random

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

current_card = {}
data_to_practice = {}

try:
    data = pd.read_csv("data/data_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    words_dict = data.to_dict(orient="records")
else:
    words_dict = data.to_dict(orient="records")


# ---------------------------- CHANGE WORD ------------------------------- #
def next_card():
    global current_card, flip_timer, i
    window.after_cancel(flip_timer)
    canvas.itemconfig(image_container, image=front_image)
    current_card = random.choice(words_dict)
    canvas.itemconfig(word_cv, text=current_card["French"], fill="black")
    canvas.itemconfig(title_cv, text="French", fill="black")
    flip_timer = window.after(3000, flip_card)

# ---------------------------- CHANGE WORD ------------------------------- #
def flip_card():
    global current_card
    canvas.itemconfig(image_container, image=back_image)
    canvas.itemconfig(word_cv, text=current_card["English"], fill="white")
    canvas.itemconfig(title_cv, text="English", fill="white")

def is_known():
    global current_card
    words_dict.remove(current_card)
    print(len(words_dict))
    data = pd.DataFrame(words_dict)
    data.to_csv("data/data_to_learn.csv", index=False)
    next_card()

#Canvas
canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
image_container = canvas.create_image(400, 263, image=front_image)
title_cv = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_cv = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

#Buttons
right_image=PhotoImage(file="images/right.png")
wrong_image=PhotoImage(file="images/wrong.png")

right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=2)

wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=2)


flip_timer = window.after(3000, flip_card)
next_card()





window.mainloop()