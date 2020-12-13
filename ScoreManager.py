"""Contains the ScoreManager class"""


class ScoreManager:
    """Generates the special tiles board and calculates the score for a specific word"""

    def __init__(self):
        """Generates the letter_socres dictionary and the special_tiles board"""
        self.letter_scores = {"R": 1, "B": 3, "I": 1, "N": 1, "O": 1, "L": 1, "C": 3, "V": 4, "G": 2, "A": 1, "S": 1,
                              "P": 3, "E": 1, "K": 5, "M": 3, "J": 8, "F": 4, "T": 1, "Y": 4, "U": 1, "Z": 10, "W": 4,
                              "Q": 10, "X": 8, "D": 2, "H": 4}
        self.special_tiles = [
            'W   l    W    l   W',
            ' w   L L   L L   w ',
            '  w     l l     w  ',
            '   L     L     L   ',
            'l   w    l    w   l',
            ' L   w   w   w   L ',
            '      L     L      ',
            ' L     l   l     l ',
            '  l     l l     l  ',
            'W  Llw   *   wlL  W',
            '  l     l l     l  ',
            ' L     l   l     l ',
            '      L     L      ',
            ' L   w   w   w   L ',
            'l   w    l    w   l',
            '   L     L     L   ',
            '  w     l l     w  ',
            ' w   L L   L L   w ',
            'W   l    W    l   W',
        ]

    def calculate_word_score(self, posx, posy, word_direction, word):
        """
        Computes the score for a given word and returns it.
        posx -- starting x position,
        posy -- starting y position,
        word_direction -- the word orientation on the board,
        word -- the word to be computed.
        """
        score = 0
        word_multiplier = 1
        word = word.upper()
        for i in range(len(word)):
            row, col = posy + i * word_direction[1], posx + i * word_direction[0]
            letter_score = self.letter_scores[word[i]]

            special_tile = self.special_tiles[row][col]

            if special_tile == 'l':
                letter_score *= 2
            elif special_tile == 'L':
                letter_score *= 3
            elif special_tile == 'w':
                word_multiplier *= 2
            elif special_tile == 'W':
                word_multiplier *= 3

            score += letter_score

        return score * word_multiplier
