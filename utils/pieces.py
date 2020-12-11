"""Module contains logic for pieces"""
from utils.logger import LOGGER
from utils.bases import Piece

# pylint: disable=too-few-public-methods

logger = LOGGER.get_logger('pieces')
logger.debug('Hello from pieces')

class Pawn(Piece):
    """Contains logic for pawn"""

    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265f, color, "Pawn")
        self.has_not_moved = True

    def get_possible_moves(self):
        """Get possible moves for pawn"""

        if self.color == "white":
            diagonals = [
                (self.row - 1, self.col + 1),
                (self.row - 1, self.col - 1)
            ]
            straight = [(self.row - 1, self.col)]
            if self.has_not_moved:
                straight.append((self.row - 2, self.col))
        else:
            diagonals = [
                (self.row + 1, self.col + 1),
                (self.row + 1, self.col - 1)
            ]
            straight = [(self.row + 1, self.col)]
            if self.has_not_moved:
                straight.append((self.row + 2, self.col))

        moves = [
            self.get_moves_in_play(diagonals),
            self.get_moves_in_play(straight)
        ]
        return moves


class Rook(Piece):
    """Contains logic for rook"""

    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265c, color, "Rook")

    def get_possible_moves(self):
        """Get possible moves for rook"""

        north = [(self.row - n, self.col) for n in range(1, 9)]
        east = [(self.row, self.col + n) for n in range(1, 9)]
        south = [(self.row + n, self.col) for n in range(1, 9)]
        west = [(self.row, self.col - n) for n in range(1, 9)]
        moves = [
            self.get_moves_in_play(north),
            self.get_moves_in_play(east),
            self.get_moves_in_play(south),
            self.get_moves_in_play(west)
        ]
        return moves


class Knight(Piece):
    """Contains logic for knight"""

    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265e, color, "Knight")

    def get_possible_moves(self):
        """Get possible moves for knight"""

        _moves = [
            (self.row - 2, self.col - 1),
            (self.row - 2, self.col + 1),
            (self.row - 1, self.col + 2),
            (self.row + 1, self.col + 2),
            (self.row + 2, self.col + 1),
            (self.row + 2, self.col - 1),
            (self.row + 1, self.col - 2),
            (self.row - 1, self.col - 2),
        ]
        moves = self.get_moves_in_play(_moves)
        return moves


class Bishop(Piece):
    """Contains logic for bishop"""

    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265d, color, "Bishop")

    def get_possible_moves(self):
        """Get possible moves for bishop"""

        north_east = [(self.row - n, self.col + n) for n in range(1, 9)]
        south_east = [(self.row + n, self.col + n) for n in range(1, 9)]
        south_west = [(self.row + n, self.col - n) for n in range(1, 9)]
        north_west = [(self.row - n, self.col - n) for n in range(1, 9)]
        moves = [
            self.get_moves_in_play(north_east),
            self.get_moves_in_play(south_east),
            self.get_moves_in_play(south_west),
            self.get_moves_in_play(north_west)
        ]
        return moves


class Queen(Piece):
    """Contains logic for queen"""

    def __init__(self, row, color):
        super().__init__(row, 3, 0x265b, color, "Queen")

    def get_possible_moves(self):
        """Get possible moves for queen"""

        north = [(self.row - n, self.col) for n in range(1, 9)]
        north_east = [(self.row - n, self.col + n) for n in range(1, 9)]
        east = [(self.row, self.col + n) for n in range(1, 9)]
        south_east = [(self.row + n, self.col + n) for n in range(1, 9)]
        south = [(self.row + n, self.col) for n in range(1, 9)]
        south_west = [(self.row + n, self.col - n) for n in range(1, 9)]
        west = [(self.row, self.col - n) for n in range(1, 9)]
        north_west = [(self.row - n, self.col - n) for n in range(1, 9)]
        moves = [
            self.get_moves_in_play(north),
            self.get_moves_in_play(north_east),
            self.get_moves_in_play(east),
            self.get_moves_in_play(south_east),
            self.get_moves_in_play(south),
            self.get_moves_in_play(south_west),
            self.get_moves_in_play(west),
            self.get_moves_in_play(north_west),
        ]
        return moves


class King(Piece):
    """Contains logic for king"""

    def __init__(self, row, color):
        super().__init__(row, 4, 0x265a, color, "King")

    def get_possible_moves(self):
        """Get possible moves for king"""

        _moves = [
            (self.row - 1, self.col),
            (self.row - 1, self.col + 1),
            (self.row, self.col + 1),
            (self.row + 1, self.col + 1),
            (self.row + 1, self.col),
            (self.row + 1, self.col - 1),
            (self.row, self.col - 1),
            (self.row - 1, self.col - 1),
        ]
        moves = self.get_moves_in_play(_moves)
        return moves
