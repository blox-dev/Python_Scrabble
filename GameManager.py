"""Contains the GameManager class"""

from LetterGenerator import LetterGenerator
from ScoreManager import ScoreManager
import utils
from constants import GRID_SIZE, MAX_HAND_SIZE
from tkinter import Toplevel


class GameManager:
    """Contains the game logic"""

    def __init__(self, root, dictionary_file):
        """
        Contains the game logic variable initialisation.
        root -- the root window,
        dictionary_file -- the path to the file which contains the word dictionary.
        """

        self.root = root
        self.gameBoard = ['-' * GRID_SIZE] * GRID_SIZE
        self.gameBoard[GRID_SIZE // 2] = '-' * (GRID_SIZE // 2) + '0' + '-' * (GRID_SIZE // 2)
        self.lg = LetterGenerator()
        self.sm = ScoreManager()
        self.dictionary = utils.read_dict(dictionary_file)

        self.active_player = 0

        self.player1 = {'name': "Player1", 'letters': self.lg.draw(MAX_HAND_SIZE), 'score': 0}
        self.player2 = {'name': "Player2", 'letters': self.lg.draw(MAX_HAND_SIZE), 'score': 0}

    def is_game_over(self):
        """
        Checks if the game is over.
        Returns a list containing [game_is_over, winning_player]
        """
        if len(self.lg.letters) == 0:
            if self.player1["score"] > self.player2["score"]:
                return [True, self.player1]
            elif self.player1["score"] < self.player2["score"]:
                return [True, self.player2]
            else:
                return [True, 0]
        return [False, 0]

    def get_number_of_letters_left(self):
        """Checks how many letters are remaining in the current game."""
        return len(self.lg.letters)

    def get_active_player(self):
        """Returns the active player."""
        if self.active_player == 0:
            return self.player1
        return self.player2

    def change_player(self):
        """Changes the active player, simulating a turn."""
        self.active_player = 1 - self.active_player

    def attempt_word_placement(self, hover_x, hover_y, word_direction, word):
        """
        Checks if a word can be placed, raises an exception otherwise.
        hover_x -- starting x position,
        hover_y -- starting y position,
        word_direction -- the word orientation,
        word -- the word to be placed.
        Returns True if all conditions are met.
        """
        active_player = self.get_active_player()
        player_letters = active_player["letters"]

        word = word.upper()
        word_len = len(word)

        if word_len < 2:
            raise ValueError("Your word must be at least two letters long")

        if word_direction[0] == 1:
            if hover_x + word_len > GRID_SIZE:
                raise ValueError("Word is out of bounds.")
        elif hover_y + word_len > GRID_SIZE:
            raise ValueError("Word is out of bounds.")

        # if word not in self.dictionary:
        #     raise ValueError("The word '{}' doesn't exist in your dictionary!".format(word))

        letters_on_board = []
        all_letters_on_board = True
        contains_starting_tile = False

        for i in range(word_len):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            if self.gameBoard[row][col] != '-':
                if self.gameBoard[row][col] != '0':
                    letters_on_board.append(self.gameBoard[row][col])
                else:
                    contains_starting_tile = True
            else:
                all_letters_on_board = False

        if all_letters_on_board:
            raise ValueError("You must use at least one of your letters")

        if len(letters_on_board) == 0 and not contains_starting_tile:
            raise ValueError("You must place your word connected to another word or the starting tile")

        pl_let = player_letters[:]
        pl_let.extend(letters_on_board)

        for letter in word:
            if letter not in pl_let:
                raise ValueError("You can't make '{}' from your letters".format(word))

            pl_let.remove(letter)

        for i in range(word_len):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            if self.gameBoard[row][col] not in ['-', '0'] and self.gameBoard[row][col] != word[i]:
                raise ValueError("Your can't place your word there")

        # Placement is okay

        # Remove letters form player hand

        letters_to_remove = []

        for i in range(word_len):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            if self.gameBoard[row][col] in ['-', '0']:
                letters_to_remove.append(word[i])

        for letter in letters_to_remove:
            player_letters.remove(letter)

        # Add new letters to player hand

        player_letters.extend(self.lg.draw(len(letters_to_remove)))

        self.place_word(hover_x, hover_y, word_direction, word)

        score = self.sm.calculate_word_score(hover_x, hover_y, word_direction, word)

        active_player["score"] += score

        return True

    def place_word(self, hover_x, hover_y, word_direction, word):
        """
        Places the word on the board game representation.
        hover_x -- starting x position,
        hover_y -- starting y position,
        word_direction -- the word orientation,
        word -- the word to be placed.
        """
        for i in range(len(word)):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            self.gameBoard[row] = self.gameBoard[row][:col] + word[i] + self.gameBoard[row][col + 1:]

    def attempt_discard_letters(self, word):
        """
        Checks if the given letters can be discarded, raises an error otherwise.
        word -- the letters to be discarded.
        """
        player = self.get_active_player()
        player_letters = player["letters"]

        word = word.upper()
        word_len = len(word)

        if word_len < 1 or word_len > MAX_HAND_SIZE:
            raise ValueError("You must discard between 1 and {} letters".format(MAX_HAND_SIZE))

        pl_let = player_letters[:]
        for letter in word:
            if letter not in pl_let:
                raise ValueError("You don't have these letters".format(word))

            pl_let.remove(letter)

        # Remove letters from the player hand

        for letter in word:
            player_letters.remove(letter)

        # Add new letters to the player hand

        player_letters.extend(self.lg.draw(word_len))
        return True

    def wait_for_game_exit(self):
        """Pauses the game execution using a Toplevel widget until any key is pressed"""
        dlg = Toplevel(self.root, height=1, width=1)
        # Intercept close button
        dlg.protocol("WM_DELETE_WINDOW", dlg.destroy)
        # Deselect any active widgets
        dlg.focus_force()
        # Can't grab until window appears
        dlg.wait_visibility()
        # Ensure all input goes to our window
        dlg.grab_set()

        dlg.bind('<KeyPress>', lambda event: dlg.destroy())
        # Block until window is destroyed
        dlg.wait_window()
        # Close the application
        exit(0)
