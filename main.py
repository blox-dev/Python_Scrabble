from tkinter import Tk

from GameManager import GameManager
from GameFrame import GameFrame
from OptionsFrame import OptionsFrame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

from sys import argv

if len(argv) != 2:
    print("Wrong number of arguments. Correct usage: py main.py <dictionary file>")
    exit(0)

dictionary_file = argv[1]

root = Tk()

root.title("Tkinter Scrabble")
root.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))

gm = GameManager(root, dictionary_file)

gf = GameFrame(root, gm)
gf.pack()

of = OptionsFrame(root, gm, gf)
of.pack()

gf.setOptionsFrame(of)

root.mainloop()
