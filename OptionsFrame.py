from tkinter import Frame, Label, Entry, Button, Text, END
from sys import exc_info


class OptionsFrame(Frame):
    def __init__(self, parent, game_manager, game_frame):
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

        self.score_1 = Label(self, text="{}: {}".format(self.gm.player1["name"], 0))
        self.score_1.grid(row=2, column=0)
        self.score_2 = Label(self, text="{}: {}".format(self.gm.player2["name"], 0))
        self.score_2.grid(row=3, column=0)

        # Control panel

        player_letters = self.gm.get_active_player()["letters"]

        self.letters_label = Label(self, text="Your letters are: {}".format(player_letters))
        self.letters_label.grid(row=1, column=1)

        self.user_input = Entry(self)
        self.user_input.grid(row=2, column=1)

        self.discard_button = Button(self, text="Discard letters", command=self.discard_letters)
        self.discard_button.grid(row=3, column=1)

        # Log window

        self.T = Text(self, height=5, width=30)
        self.T.grid(row=1, column=2, rowspan=3, padx=20)
        self.T.insert(END, "It is {}'s turn.".format(self.gm.get_active_player()["name"]))
        self.T.see(END)

    def discard_letters(self):
        try:
            self.gm.attempt_discard_letters(self.user_input.get())

            self.T.insert(END, "\n{} discarded: '{}'".format(self.gm.get_active_player()["name"],
                                                             self.user_input.get().upper()))

            self.user_input.delete(0, END)

            game_state, winner = self.gm.is_game_over()
            if game_state:
                if winner == 0:
                    self.error_text.config(text="Game is over. It's a tie! Press any key to exit")
                    self.T.insert(END, "\nIt's a tie!")
                else:
                    self.error_text.config(text="Game is over. {} wins! Press any key to exit".format(winner["name"]))
                    self.T.insert(END, "\n{} wins!".format(winner["name"]))

                self.T.see(END)
                self.gm.wait_for_game_exit()

            self.gm.change_player()

            new_player = self.gm.get_active_player()

            self.T.insert(END, "\nIt is {}'s turn.".format(new_player["name"]))
            self.T.see(END)

            self.letters_label.config(text="Your letters are: {}".format(new_player["letters"]))

            self.error_text.config(text="There are {} letters left".format(self.gm.get_number_of_letters_left()))

        except ValueError:
            self.error_text.config(text=exc_info()[1])
        except Exception:
            self.error_text.config(text="Unexpected error.")
            print(exc_info())
