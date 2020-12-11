from tkinter import *
from sys import exc_info


class OptionsFrame(Frame):
    def __init__(self, parent, game_manager, game_frame):
        Frame.__init__(self, parent, width=610, height=100)

        self.gm = game_manager
        self.gf = game_frame
        self.error_text = Label(self, text="", pady=5, fg='red', font=('TkDefaultFont', 15))
        self.error_text.pack()

        player_letters = self.gm.get_player_letters()

        self.letters_label = Label(self, text="Your letters are: {}".format(player_letters), pady=5)
        self.letters_label.pack()

        self.user_input = Entry(self)
        self.user_input.pack(pady=5)

        self.discard_button = Button(self, text="Discard letters", command=self.discard_letters)
        self.discard_button.pack(pady=5)

    def discard_letters(self):
        try:
            self.gm.attempt_discard_letters(self.user_input.get())

            new_player_letters = self.gm.get_player_letters()

            self.letters_label.config(text="Your letters are: {}".format(new_player_letters))

            self.error_text.config(text="")

        except ValueError:
            self.error_text.config(text=exc_info()[1])
        except Exception:
            self.error_text.config(text="Unexpected error.")
