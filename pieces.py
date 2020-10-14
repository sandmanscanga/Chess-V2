from bases import Piece


class Pawn(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265f, color, "Pawn")
        self.hasNotMoved = True

    def get_possible_moves(self):
        if self.color == "white":
            # up 1, right 1
            # up 1, left 1
            # up 1
            moves = [
                (self.row - 1, self.col + 1),
                (self.row - 1, self.col - 1),
                (self.row - 1, self.col)
            ]
            if self.hasNotMoved:
                # up 2
                moves.append((self.row - 2, self.col))
        else:
            # down 1, right 1
            # down 1, left 1
            # down 1
            moves = [
                (self.row + 1, self.col + 1),
                (self.row + 1, self.col - 1),
                (self.row + 1, self.col)
            ]
            if self.hasNotMoved:
                # down 2
                moves.append((self.row + 2, self.col))
        return moves


class Rook(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265c, color, "Rook")


class Knight(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265e, color, "Knight")

    def get_possible_moves(self):
        # up 2 left 1, 
        # up 2 right 1, 
        # right 2 up 1,
        # right 2 down 1,
        # down 2 right 1,
        # down 2 left 1, 
        # left 2 down 1, 
        # left 2 up 1
        moves = [
            (self.row - 2, self.col - 1),
            (self.row - 2, self.col + 1),
            (self.row - 1, self.col + 2),
            (self.row + 1, self.col + 2),
            (self.row + 2, self.col + 1),
            (self.row + 2, self.col - 1),
            (self.row + 1, self.col - 2),
            (self.row - 1, self.col - 2),
        ]
        return moves

class Bishop(Piece):

    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265d, color, "Bishop")

class Queen(Piece):
    
    def __init__(self, row, color):
        super().__init__(row, 3, 0x265b, color, "Queen")

class King(Piece):
    
    def __init__(self, row, color):
        super().__init__(row, 4, 0x265a, color, "King")

    def get_possible_moves(self):
        # up 1
        # up 1, right 1
        # right 1
        # right 1, down 1
        # down 1
        # down 1, left 1
        # left 1
        # left 1, up 1

        moves = [
            (self.row - 1, self.col),
            (self.row - 1, self.col + 1),
            (self.row, self.col + 1),
            (self.row + 1, self.col + 1),
            (self.row + 1, self.col),
            (self.row + 1, self.col - 1),
            (self.row, self.col - 1),
            (self.row - 1, self.col - 1),
        ]
        return moves
