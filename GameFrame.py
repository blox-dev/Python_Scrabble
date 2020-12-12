from tkinter import Frame, Label, END
from PIL import ImageTk, Image
from constants import GRID_SIZE, TILE_SIZE, SEPARATOR_SIZE
from sys import exc_info
import utils


# TODO: class refactoring
# TODO: add PEP comments

class GameFrame(Frame):
    def __init__(self, parent, game_manager):
        self.gm = game_manager
        self.of = None
        self.hover_img = Image.open("img/hover_placement.png")
        self.hover_img_cpy = None
        self.letter_ref = utils.create_letter_images()
        self.bgImage = ImageTk.PhotoImage(Image.open("img/scrabble_board.png"))

        Frame.__init__(self, parent, width=self.bgImage.width(), height=self.bgImage.height())
        self.hover_x = 0
        self.hover_y = 0
        self.hover_length = 0
        self.word_direction = [1, 0]
        self.word_direction_changed = False

        self.hover_rect = Label(self, image=ImageTk.PhotoImage(self.hover_img))

        self.background = Label(self, image=self.bgImage)
        self.background.bind('<Motion>', self.motion_function)

        parent.bind('<Button-3>', self.change_word_direction)

        self.background.place(x=0, y=0)

    def change_word_direction(self, event):
        self.word_direction[0] = 1 - self.word_direction[0]
        self.word_direction[1] = 1 - self.word_direction[1]
        self.word_direction_changed = True

    def place_word(self, event):
        try:
            self.gm.attempt_word_placement(self.hover_x, self.hover_y, self.word_direction, self.of.user_input.get())

            player = self.gm.get_active_player()

            if player["name"] == self.gm.player1["name"]:
                self.of.score_1.config(text="{}: {}".format(player["name"], player["score"]))
            else:
                self.of.score_2.config(text="{}: {}".format(player["name"], player["score"]))

            self.of.T.insert(END, "\n{} played: '{}'".format(player["name"], self.of.user_input.get().upper()))

            self.place_word_on_canvas()

            game_state, winner = self.gm.is_game_over()
            if game_state:
                if winner == 0:
                    self.of.error_text.config(text="Game is over. It's a tie! Press any key to exit")
                    self.of.T.insert(END, "\nIt's a tie!")
                else:
                    self.of.error_text.config(text="Game is over. {} wins! Press any key to exit".format(winner["name"]))
                    self.of.T.insert(END, "\n{} wins!".format(winner["name"]))

                self.of.T.see(END)
                self.hover_rect.destroy()
                self.gm.wait_for_game_exit()

            self.gm.change_player()

            new_player = self.gm.get_active_player()

            self.of.T.insert(END, "\nIt is {}'s turn.".format(new_player["name"]))
            self.of.T.see(END)

            self.of.letters_label.config(text="Your letters are: {}".format(new_player["letters"]))
            self.of.error_text.config(text="There are {} letters left".format(self.gm.get_number_of_letters_left()))
            self.of.user_input.delete(0, END)
        except ValueError:
            self.of.error_text.config(text=exc_info()[1])
        except Exception:
            self.of.error_text.config(text="Unexpected error.")
            print(exc_info())

    def motion_function(self, event, x=None, y=None):

        if x is None and y is None:
            new_x = (event.x - SEPARATOR_SIZE // 2) // (TILE_SIZE + SEPARATOR_SIZE)
            new_y = (event.y - SEPARATOR_SIZE // 2) // (TILE_SIZE + SEPARATOR_SIZE)
        else:
            new_x = x
            new_y = y
            self.hover_x = 0

        if new_x >= GRID_SIZE or new_x < 0 or new_y >= GRID_SIZE or new_y < 0:
            return

        if len(self.of.user_input.get()) == 0:
            self.hover_rect.place_forget()
            return

        if len(self.of.user_input.get()) != self.hover_length or self.word_direction_changed:
            self.hover_length = len(self.of.user_input.get())
            img_cpy = self.hover_img.resize(  # TODO: put in own if condition
                ((TILE_SIZE + SEPARATOR_SIZE) * (self.hover_length if self.word_direction[0] == 1 else 1),
                 (TILE_SIZE + SEPARATOR_SIZE) * (self.hover_length if self.word_direction[1] == 1 else 1)),
                Image.ANTIALIAS)
            self.hover_img_cpy = ImageTk.PhotoImage(img_cpy)
            self.hover_rect.place_forget()
            self.hover_rect = Label(self, image=self.hover_img_cpy)

        if len(self.of.user_input.get()) != 0:
            if new_y != self.hover_y or new_x != self.hover_x or self.word_direction_changed:
                self.word_direction_changed = False
                self.hover_y = new_y
                self.hover_x = new_x
                self.hover_rect.bind('<Button-1>', self.place_word)
                self.hover_rect.place(x=self.hover_x * (TILE_SIZE + SEPARATOR_SIZE) + SEPARATOR_SIZE // 2,
                                      y=self.hover_y * (TILE_SIZE + SEPARATOR_SIZE) + SEPARATOR_SIZE // 2)

    def place_word_on_canvas(self):
        word = self.of.user_input.get().upper()
        for i in range(len(word)):
            letter_label = Label(self, image=self.letter_ref[ord(word[i]) - ord('A')])

            letter_label.bind('<Motion>',
                              lambda event, ind=i, hovx=self.hover_x, hovy=self.hover_y, xx=self.word_direction[0],
                              yy=self.word_direction[1]:
                              self.motion_function(event,
                                                   x=hovx + ind * xx,
                                                   y=hovy + ind * yy))
            letter_label.place(
                x=(self.hover_x + i * self.word_direction[0]) * (TILE_SIZE + SEPARATOR_SIZE) + SEPARATOR_SIZE // 2,
                y=(self.hover_y + i * self.word_direction[1]) * (TILE_SIZE + SEPARATOR_SIZE) + SEPARATOR_SIZE // 2)

    def setOptionsFrame(self, of):
        self.of = of
