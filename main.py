from tkinter import *
from PIL import ImageTk, Image
import random

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GRID_SIZE = 19

root = Tk()

root.title("Tkinter Scrabble")
root.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))

hover_x = 0
hover_y = 0

rect_img = Image.open("hover_placement.png")
rect_img_cpy = Image.open("hover_placement.png")

hover_rect = ImageTk.PhotoImage(rect_img)

panel = Label(root, image=hover_rect)


def myfunction(event):
    new_x = event.x // 31
    new_y = event.y // 31

    global hover_y, hover_x, rect_img, rect_img_cpy, panel

    if hover_x != new_x or hover_y != new_y:
        panel.place_forget()
        panel.tkraise(aboveThis=gameFrame)
        hover_x = new_x
        hover_y = new_y
        print(hover_x, hover_y)
        rect_img_cpy = rect_img.resize((30 * random.randint(1, 5), 30), Image.ANTIALIAS)
        abc = ImageTk.PhotoImage(rect_img_cpy)
        panel = Label(root, image=abc)
        panel.place(x=31 * (hover_x + 1), y=31 * (hover_y + 1))


# gameFrame = Frame(root)

bgImage = ImageTk.PhotoImage(Image.open("scrabble_board.png"))
gameFrame = Label(root, image=bgImage)
gameFrame.bind('<Motion>', myfunction)
gameFrame.pack()

# gameFrame.pack()

# def tile_click(posx, posy):
#     print(posx, posy)
#
#
# for i in range(GRID_SIZE):
#     for j in range(GRID_SIZE):
#         button = Button(gameFrame, height=1, width=2, command=lambda posx=i, posy=j: tile_click(posx, posy))
#         button.grid(row=i, column=j)

optionsFrame = Label(root, text="Lmao1234", padx=10, pady=10)
optionsFrame.pack()

# b = Button(gameFrame, text="abcd")
# b2 = Button(gameFrame, text="defg")
# b.grid(row=0, column=0)
# b2.grid(row=1, column=1)

# buttonsFrame = Frame(root)
# buttonsFrame.pack(pady=20)
#
# b3 = Button(buttonsFrame, text="lol")
# b3.pack()

root.mainloop()
