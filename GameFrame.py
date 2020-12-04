from tkinter import *
from PIL import ImageTk, Image
from constants import GRID_SIZE, TILE_SIZE, SEPARATOR_SIZE
from GameManager import GameManager
from sys import exc_info


# TODO: class refactoring!

class GameFrame(Frame):
    def __init__(self, parent, dictionary_file):
        self.gm = GameManager(dictionary_file)

        self.img = Image.open("img/hover_placement.png")

        self.bgImage = ImageTk.PhotoImage(Image.open("img/scrabble_board.png"))

        Frame.__init__(self, parent, width=self.bgImage.width(), height=self.bgImage.height())
        self.hover_x = 0
        self.hover_y = 0
        self.hover_length = 0
        self.word_direction = [1, 0]
        self.word_direction_changed = False

        self.hover_rect = Label(self, image=ImageTk.PhotoImage(self.img))

        self.background = Label(self, image=self.bgImage)
        self.background.bind('<Motion>', self.myfunction)

        parent.bind('<Button-3>', self.change_word_direction)

        self.background.place(x=0, y=0)

        self.pack()

        player_letters = self.gm.draw(7)

        letters_label = Label(parent, text="Your letters are: {}".format(player_letters), padx=10, pady=10)
        letters_label.pack()

        self.user_input = Entry(parent)
        self.user_input.pack(pady=10)

    def change_word_direction(self, event):
        self.word_direction[0] = 1 - self.word_direction[0]
        self.word_direction[1] = 1 - self.word_direction[1]
        self.word_direction_changed = True

    def place_word(self, event):
        try:
            self.gm.attempt_word_placement(self.hover_x, self.hover_y, self.word_direction, self.user_input.get())
        except ValueError:
            print(exc_info()[1])

    def myfunction(self, event):
        new_x = (event.x - SEPARATOR_SIZE // 2) // (TILE_SIZE + SEPARATOR_SIZE)
        new_y = (event.y - SEPARATOR_SIZE // 2) // (TILE_SIZE + SEPARATOR_SIZE)

        if new_x >= GRID_SIZE or new_x < 0 or new_y >= GRID_SIZE or new_y < 0:
            return

        if len(self.user_input.get()) == 0:
            self.hover_rect.place_forget()
            return

        if len(self.user_input.get()) != self.hover_length or self.word_direction_changed:
            hover_length = len(self.user_input.get())
            img_cpy = self.img.resize(  # TODO: put in own if condition
                ((TILE_SIZE + SEPARATOR_SIZE) * (hover_length if self.word_direction[0] == 1 else 1),
                 (TILE_SIZE + SEPARATOR_SIZE) * (hover_length if self.word_direction[1] == 1 else 1)),
                Image.ANTIALIAS)
            self.hover_rect.place_forget()
            self.hover_rect = Label(self, image=ImageTk.PhotoImage(img_cpy))

        if len(self.user_input.get()) != 0:
            if new_y != self.hover_y or new_x != self.hover_x or self.word_direction_changed:
                self.word_direction_changed = False
                self.hover_y = new_y
                self.hover_x = new_x
                self.hover_rect.bind('<Button-1>', self.place_word)
                self.hover_rect.place(x=self.hover_x * (TILE_SIZE + SEPARATOR_SIZE) + SEPARATOR_SIZE // 2,
                                      y=self.hover_y * (TILE_SIZE + SEPARATOR_SIZE) + SEPARATOR_SIZE // 2)
