import random


class LetterGenerator:
    def __init__(self):

        self.letters = ('E' * 12) + ('AI' * 9) + ('O' * 8) + ('NRT' * 6) + ('LSUD' * 4) + ('G' * 3) + ('BCMPFHVWY' * 2) + 'KJXQZ'
        self.letters = [i for i in self.letters]

    def draw(self, number_of_tiles):
        random.shuffle(self.letters)
        drawn_letters = self.letters[:number_of_tiles].copy()
        self.letters = self.letters[number_of_tiles + 1:]
        return drawn_letters

