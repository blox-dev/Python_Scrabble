from LetterGenerator import LetterGenerator
import utils
from constants import GRID_SIZE


class GameManager:
    def __init__(self, dictionary_file):
        self.gameBoard = ['-' * GRID_SIZE] * GRID_SIZE
        self.gameBoard[GRID_SIZE // 2] = '-' * (GRID_SIZE // 2) + '0' + '-' * (GRID_SIZE // 2)
        self.lg = LetterGenerator()
        self.player_letters = []
        self.dictionary = utils.read_dict(dictionary_file)

    def draw(self, number_of_letters):
        drawn_letters = self.lg.draw(number_of_letters)
        self.player_letters.extend(drawn_letters)
        return drawn_letters

    def attempt_word_placement(self, hover_x, hover_y, word_direction, word):
        print(hover_x, hover_y, word_direction, word, self.player_letters)
        word = word.upper()
        word_len = len(word)

        # if word not in self.dictionary:
        #     raise ValueError("The word '{}' doesn't exist in your dictionary!".format(word))

        pl = self.player_letters[:]
        for letter in word:
            if letter not in pl:
                raise ValueError("You can't make your word from those letters")

            for index in range(len(pl)):
                if pl[index] == letter:
                    pl[index] = '0'
                    break

        # WORD IS OKAY
        ok = 0
        for i in range(word_len):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            if self.gameBoard[row][col] != '-':
                ok = 1
                break

        if ok == 0:
            raise ValueError("You must place your word connected to another word")

        for i in range(word_len):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            if self.gameBoard[row][col] not in ['-', '0'] and self.gameBoard[row][col] != word[i]:
                raise ValueError("Your can't place your word there")

        self.place_word(hover_x, hover_y, word_direction, word)
        return True

    def place_word(self, hover_x, hover_y, word_direction, word):
        for i in range(len(word)):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            self.gameBoard[row] = self.gameBoard[row][:col] + word[i] + self.gameBoard[row][col+1:]
