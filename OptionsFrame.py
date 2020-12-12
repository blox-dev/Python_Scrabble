from tkinter import *
from sys import exc_info


class OptionsFrame(Frame):
    def __init__(self, parent, game_manager, game_frame):
        self.parent = parent
        Frame.__init__(self, parent)
        self.gm = game_manager
        self.gf = game_frame

        # Error text

        self.error_text = Label(self, text="There are {} letters left.".format(self.gm.get_number_of_letters_left()),
                                pady=5, fg='red', font=('TkDefaultFont', 15))
        self.error_text.grid(row=0, column=0, columnspan=3)

        # Scoreboard

        self.score_title = Label(self, text="Scoreboard", font=('TkDefaultDFont', 15))
        self.score_title.grid(row=1, column=0, padx=20)

        self.score_1 = Label(self, text="{}: {}".format(self.gm.player1_name, 0))
        self.score_1.grid(row=2, column=0)
        self.score_2 = Label(self, text="{}: {}".format(self.gm.player2_name, 0))
        self.score_2.grid(row=3, column=0)

        # Control panel

        player_letters = self.gm.get_player()[1]

        self.letters_label = Label(self, text="Your letters are: {}".format(player_letters))
        self.letters_label.grid(row=1, column=1)

        self.user_input = Entry(self)
        self.user_input.grid(row=2, column=1)

        self.discard_button = Button(self, text="Discard letters", command=self.discard_letters)
        self.discard_button.grid(row=3, column=1)

        # Log window

        self.T = Text(self, height=5, width=30)
        self.T.grid(row=1, column=2, rowspan=3, padx=20)
        self.T.insert(END, "It is {}'s turn.".format(self.gm.get_player()[0]))
        self.T.see(END)

    def discard_letters(self):
        try:
            self.gm.attempt_discard_letters(self.user_input.get())

            self.T.insert(END, "\n{} discarded: '{}'".format(self.gm.get_player()[0], self.user_input.get().upper()))

            self.user_input.delete(0, END)

            game_state = self.gm.is_game_over()
            if game_state[0]:
                if game_state[1] == 0:
                    self.error_text.config(text="Game is over. It's a tie!".format(game_state[1]))
                else:
                    self.error_text.config(text="Game is over. {} wins!".format(game_state[1]))

                self.gm.wait_for_game_exit()

            self.gm.change_player()

            new_player = self.gm.get_player()

            self.T.insert(END, "\nIt is {}'s turn.".format(new_player[0]))
            self.T.see(END)

            self.letters_label.config(text="Your letters are: {}".format(new_player[1]))

            self.error_text.config(text="There are {} letters left".format(self.gm.get_number_of_letters_left()))

        except ValueError:
            self.error_text.config(text=exc_info()[1])
        except Exception:
            self.error_text.config(text="Unexpected error.")
            print(exc_info())
