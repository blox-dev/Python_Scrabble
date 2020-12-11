from LetterGenerator import LetterGenerator
import utils
from constants import GRID_SIZE


class GameManager:
    def __init__(self, dictionary_file):
        self.gameBoard = ['-' * GRID_SIZE] * GRID_SIZE
        self.gameBoard[GRID_SIZE // 2] = '-' * (GRID_SIZE // 2) + '0' + '-' * (GRID_SIZE // 2)
        self.lg = LetterGenerator()
        self.current_player = 1
        self.player1_letters = self.draw(7)
        self.player2_letters = self.draw(7)
        self.dictionary = utils.read_dict(dictionary_file)

    def draw(self, number_of_letters):
        drawn_letters = self.lg.draw(number_of_letters)
        print("Letters left:", len(self.lg.letters))
        return drawn_letters

    def get_player_letters(self):
        if self.current_player == 1:
            return self.player1_letters
        return self.player2_letters

    def attempt_word_placement(self, hover_x, hover_y, word_direction, word):
        player_letters = self.get_player_letters()

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

        # PLACEMENT IS OKAY

        # REMOVE LETTERS

        letters_to_remove = []

        for i in range(word_len):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            if self.gameBoard[row][col] in ['-', '0']:
                letters_to_remove.append(word[i])

        for letter in letters_to_remove:
            player_letters.remove(letter)

        # ADD NEW LETTERS

        player_letters.extend(self.draw(len(letters_to_remove)))

        self.place_word(hover_x, hover_y, word_direction, word)
        self.current_player = 1 - self.current_player
        return True

    def place_word(self, hover_x, hover_y, word_direction, word):
        for i in range(len(word)):
            row, col = hover_y + i * word_direction[1], hover_x + i * word_direction[0]
            self.gameBoard[row] = self.gameBoard[row][:col] + word[i] + self.gameBoard[row][col + 1:]

    def attempt_discard_letters(self, word):
        player_letters = self.get_player_letters()

        word = word.upper()
        word_len = len(word)

        if word_len < 1 or word_len > 7:
            raise ValueError("You must discard between 1 and 7 letters")

        pl_let = player_letters[:]
        for letter in word:
            if letter not in pl_let:
                raise ValueError("You don't have these letters".format(word))

            pl_let.remove(letter)

        # REMOVE LETTERS

        for letter in word:
            player_letters.remove(letter)

        # ADD NEW LETTERS

        player_letters.extend(self.draw(word_len))
        self.current_player = 1 - self.current_player
        return True
