"""
The starting point of the project.
arguments: <dictionary_file> -- contains the word dictionary used for this game of scrabble.
"""

from tkinter import Tk
from GameManager import GameManager
from GameFrame import GameFrame
from OptionsFrame import OptionsFrame
from utils import get_geometry
from sys import argv


def main():
    if len(argv) > 2:
        print("Wrong number of arguments. Correct usage: py main.py <dictionary file>")
        exit(0)

    dictionary_file = argv[1] if len(argv) == 2 else "dictionary.txt"

    # Initialises the root window
    root = Tk()
    root.title("Tkinter Scrabble")

    geometry = get_geometry(root)
    root.geometry(geometry)
    root.update()

    # Initialises the game manager and packs it
    gm = GameManager(root, dictionary_file)

    # Initialises the game frame
    gf = GameFrame(root, gm)
    gf.grid(row=0, column=0)

    # Initialises the options frame and packs it
    of = OptionsFrame(root, gm, gf)
    of.grid(row=0, column=1)

    gf.setOptionsFrame(of)

    # The main loop of the program
    root.mainloop()

if __name__ == "__main__":
    main()
