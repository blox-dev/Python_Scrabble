"""Contains the LetterGenerator class"""

import random


class LetterGenerator:
    """Generates the letter set and binds it to the game manager"""
    def __init__(self):
        """Initialises the letter set"""
        self.letters = ('E' * 12) + ('AI' * 9) + ('O' * 8) + ('NRT' * 6) + ('LSUD' * 4) + ('G' * 3) \
            + ('BCMPFHVWY' * 2) + 'KJXQZ'

        self.letters = [i for i in self.letters]

    def draw(self, number_of_letters):
        """
        Draws a specified number of letters.
        number_of_letters -- the number of letters to be drawn.
        Returns the drawn letters.
        """
        random.shuffle(self.letters)
        drawn_letters = self.letters[:number_of_letters].copy()
        self.letters = self.letters[number_of_letters:]
        return drawn_letters
