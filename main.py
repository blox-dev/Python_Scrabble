from tkinter import *
from LetterGenerator import LetterGenerator
from GameFrame import GameFrame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
root = Tk()

root.title("Tkinter Scrabble")
root.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))

user_input = Entry(root)
gf = GameFrame(root, user_input)
gf.pack()

lg = LetterGenerator()
player_letters = lg.draw(7)

letters_label = Label(root, text="Your letters are: {}".format(player_letters), padx=10, pady=10)
letters_label.pack()

user_input.pack(pady=10)

root.mainloop()
