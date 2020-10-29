from .bases import Piece


class Pawn(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265f, color, "Pawn")
        self.hasNotMoved = True

    def get_possible_moves(self):
        if self.color == "white":
            diagonals = [
                (self.row - 1, self.col + 1),
                (self.row - 1, self.col - 1)
            ]
            straight = [(self.row - 1, self.col)]
            if self.hasNotMoved:
                straight.append((self.row - 2, self.col))
        else:
            diagonals = [
                (self.row + 1, self.col + 1),
                (self.row + 1, self.col - 1)
            ]
            straight = [(self.row + 1, self.col)]
            if self.hasNotMoved:
                straight.append((self.row + 2, self.col))
        
        moves = {
            "diagonals": list(self.gen_moves_in_play(diagonals)),
            "straight": list(self.gen_moves_in_play(straight))
        }
        return moves


class Rook(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265c, color, "Rook")

    def get_possible_moves(self):
        north = [(self.row - n, self.col) for n in range(1, 9)]
        east = [(self.row, self.col + n) for n in range(1, 9)]
        south = [(self.row + n, self.col) for n in range(1, 9)]
        west = [(self.row, self.col - n) for n in range(1, 9)]
        moves = {
            "north": list(self.gen_moves_in_play(north)),
            "east": list(self.gen_moves_in_play(east)),
            "south": list(self.gen_moves_in_play(south)),
            "west": list(self.gen_moves_in_play(west))
        }
        return moves


class Knight(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265e, color, "Knight")

    def get_possible_moves(self):
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
        moves = list(self.gen_moves_in_play(_moves))
        return moves


class Bishop(Piece):

    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265d, color, "Bishop")

    def get_possible_moves(self):
        northEast = [(self.row - n, self.col + n) for n in range(1, 9)]
        southEast = [(self.row + n, self.col + n) for n in range(1, 9)]
        southWest = [(self.row + n, self.col - n) for n in range(1, 9)]
        northWest = [(self.row - n, self.col - n) for n in range(1, 9)]
        moves = {
            "northEast": list(self.gen_moves_in_play(northEast)),
            "southEast": list(self.gen_moves_in_play(southEast)),
            "southWest": list(self.gen_moves_in_play(southWest)),
            "northWest": list(self.gen_moves_in_play(northWest)),
        }
        return moves


class Queen(Piece):
    
    def __init__(self, row, color):
        super().__init__(row, 3, 0x265b, color, "Queen")

    def get_possible_moves(self):
        north = [(self.row - n, self.col) for n in range(1, 9)]
        northEast = [(self.row - n, self.col + n) for n in range(1, 9)]
        east = [(self.row, self.col + n) for n in range(1, 9)]
        southEast = [(self.row + n, self.col + n) for n in range(1, 9)]
        south = [(self.row + n, self.col) for n in range(1, 9)]
        southWest = [(self.row + n, self.col - n) for n in range(1, 9)]
        west = [(self.row, self.col - n) for n in range(1, 9)]
        northWest = [(self.row - n, self.col - n) for n in range(1, 9)]
        moves = {
            "north": list(self.gen_moves_in_play(north)),
            "northEast": list(self.gen_moves_in_play(northEast)),
            "east": list(self.gen_moves_in_play(east)),
            "southEast": list(self.gen_moves_in_play(southEast)),
            "south": list(self.gen_moves_in_play(south)),
            "southWest": list(self.gen_moves_in_play(southWest)),
            "west": list(self.gen_moves_in_play(west)),
            "northWest": list(self.gen_moves_in_play(northWest)),
        }
        return moves


class King(Piece):
    
    def __init__(self, row, color):
        super().__init__(row, 4, 0x265a, color, "King")

    def get_possible_moves(self):
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
        moves = list(self.gen_moves_in_play(_moves))
        return moves