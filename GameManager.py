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

        word = word.upper()
        word_len = len(word)

        if word_len < 2 or word_len > 7:
            raise ValueError("Your word must be between 2 and 7 letters long")

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
            raise ValueError("You must place your word connected to another word")

        player_letters = self.player_letters[:]
        player_letters.extend(letters_on_board)

        for letter in word:
            if letter not in player_letters:
                raise ValueError("You can't make '{}' from your letters".format(word))

            player_letters.remove(letter)

        for i in range(word_len):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            if self.gameBoard[row][col] not in ['-', '0'] and self.gameBoard[row][col] != word[i]:
                raise ValueError("Your can't place your word there")

        # PLACEMENT IS OKAY

        # REMOVE LETTERS

        letters_to_remove = []

        for i in range(word_len):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            if self.gameBoard[row][col] in ['-', '0']:
                letters_to_remove.append(word[i])

        for letter in letters_to_remove:
            self.player_letters.remove(letter)

        # ADD NEW LETTERS

        self.player_letters.extend(self.lg.draw(len(letters_to_remove)))

        self.place_word(hover_x, hover_y, word_direction, word)

        return self.player_letters

    def place_word(self, hover_x, hover_y, word_direction, word):
        for i in range(len(word)):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            self.gameBoard[row] = self.gameBoard[row][:col] + word[i] + self.gameBoard[row][col + 1:]
