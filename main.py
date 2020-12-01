from tkinter import *
from PIL import ImageTk, Image
import random

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 750
GRID_SIZE = 19
TILE_SIZE = 30
SEPARATOR_SIZE = 2

root = Tk()

root.title("Tkinter Scrabble")
root.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))

hover_x = 0
hover_y = 0
hover_length = 0

img = Image.open("hover_placement.png")
img_cpy = Image.open("hover_placement.png")

bgImage = ImageTk.PhotoImage(Image.open("better_board.png"))

gameFrame = Frame(root)

background = Label(gameFrame, image=bgImage)

hover_rect = Label(gameFrame, image=ImageTk.PhotoImage(img))


def myfunction(event):
    new_x = (event.x - SEPARATOR_SIZE / 2) // (TILE_SIZE + SEPARATOR_SIZE)
    new_y = (event.y - SEPARATOR_SIZE / 2) // (TILE_SIZE + SEPARATOR_SIZE)

    if new_x >= GRID_SIZE or new_x < 0 or new_y >= GRID_SIZE or new_y < 0:
        return

    global hover_y, hover_x, hover_length, hover_rect, img_cpy

    if len(user_input.get()) != hover_length:
        hover_length = len(user_input.get())
        img_cpy = img.resize((TILE_SIZE * hover_length, TILE_SIZE), Image.ANTIALIAS)
        hover_rect.place_forget()
        hover_rect = Label(gameFrame, image=ImageTk.PhotoImage(img_cpy))

    if len(user_input.get()) != 0:
        if new_y != hover_y or new_x != hover_x:
            hover_y = new_y
            hover_x = new_x
            print(hover_x, hover_y)
            hover_rect.place(x=hover_x * (TILE_SIZE + SEPARATOR_SIZE) + SEPARATOR_SIZE, y=hover_y * (TILE_SIZE + SEPARATOR_SIZE) + SEPARATOR_SIZE)

    # print((event.x - 1) // 32 * 32 + 2, (event.y - 1) // 32 * 32 + 2)


background.bind('<Motion>', myfunction)
background.pack()

gameFrame.pack()

player_letters = [chr(i) for i in range(65, 91)]

random.shuffle(player_letters)

letters_label = Label(root, text="Your letters are: {}".format(" ".join(player_letters[:7])), padx=10, pady=10)
letters_label.pack()

user_input = Entry()
user_input.pack()

root.mainloop()
