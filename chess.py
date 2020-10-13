import tkinter as tk
import json
import sys

## Cross-Platform Compatibility
if sys.platform == "linux":
    piece_size = 56
else:
    piece_size = 36


class Square:

    length = 75
    colors = ("#212121", "#bdbdbd")
    selectedColor = "#ffeb3b" # Gold
    possibleColor = "#26c6da" # Cyan
    threatColor = "#c62828" # Red
    isSelected = False
    isPossible = False
    isThreat = False

    def __init__(self, row, col):
        (self.row, self.col) = (row, col)
        color_id = (self.row + self.col) % 2
        self.color = self.colors[color_id]
        x1 = self.length * self.col
        y1 = self.length * self.row
        x2 = self.length + x1
        y2 = self.length + y1
        self.coords = (x1, y1, x2, y2)

    def __str__(self):
        return f"(Square [{self.row}, {self.col}])"

    def draw(self, canvas):
        if self.isSelected:
            canvas.create_rectangle(*self.coords, fill=self.selectedColor)
        elif self.isPossible:
            canvas.create_rectangle(*self.coords, fill=self.possibleColor)
        elif self.isThreat:
            canvas.create_rectangle(*self.coords, fill=self.threatColor)
        else:
            canvas.create_rectangle(*self.coords, fill=self.color)


class Piece:
    
    white = "white"
    black = "black"

    def __init__(self, row, col, char, color, name):
        (self.row, self.col) = (row, col)
        self.char = chr(char)
        self.color = color
        self.name = name

    def __str__(self):
        return f"({self.name} [{self.row}, {self.col}] {self.color})"

    def draw(self, canvas):
        x = (Square.length * self.col) + (Square.length / 2) 
        y = (Square.length * self.row) + (Square.length / 2)
        canvas.create_text(x, y, text=self.char, 
            fill=self.color, font=("", piece_size))

    def get_possible_moves(self):
        return []


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


class MoveValidation:
    
    def validate_knight(self, moves):
        validMoves = []
        for move in moves:
            posSquare = self.find_square(*move)
            posPiece = self.find_piece(*move)
            if posPiece:
                if posPiece.color != self.selectedPiece.color:
                    # enemy piece, attack
                    posSquare.isThreat = True
                    validMoves.append(move)
                else:
                    # friendly piece
                    pass
            else:
                posSquare.isPossible = True
                validMoves.append(move)

        return validMoves

    def validate_king(self, moves):
        validMoves = []
        for move in moves:
            posSquare = self.find_square(*move)
            posPiece = self.find_piece(*move)
            if posPiece:
                if posPiece.color != self.selectedPiece.color:
                    # enemy piece, attack
                    posSquare.isThreat = True
                    validMoves.append(move)
                else:
                    # friendly piece
                    pass
            else:
                posSquare.isPossible = True
                validMoves.append(move)
        return validMoves

    def validate_pawn(self, moves):
        validMoves = []
        for move in moves[:2]:
            posSquare = self.find_square(*move)
            posPiece = self.find_piece(*move)
            if posPiece:
                if posPiece.color != self.selectedPiece.color:
                    # enemy piece, attack
                    posSquare.isThreat = True
                    validMoves.append(move)
        for move in moves[2:]:
            posSquare = self.find_square(*move)
            posPiece = self.find_piece(*move)
            if not posPiece:
                posSquare.isPossible = True
                validMoves.append(move)
        return validMoves


class Board(MoveValidation):

    def __init__(self, master):
        super().__init__()
        self.canvas = tk.Canvas(master, width=600, height=600)
        self.squares = self.init_squares()
        self.pieces = self.init_pieces()
        self.selectedPiece = None
        self.draw_squares()
        self.draw_pieces()
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.pack()

    @property
    def selectedPiece(self):
        return self.__selectedPiece

    @selectedPiece.setter
    def selectedPiece(self, piece):
        if piece:
            self.square.isSelected = True
            self.__selectedPiece = piece
            self.validMoves = self.get_valid_moves()
        else:
            self.__selectedPiece = None
            self.validMoves = []

    def left_click(self, event):
        self.reset_squares()

        row = event.y // Square.length
        col = event.x // Square.length

        self.square = self.find_square(row, col)
        self.piece = self.find_piece(row, col)

        # log the board state
        print(json.dumps({
            "square": str(self.square),
            "piece": str(self.piece),
            "selectedPiece": str(self.selectedPiece),
            "vailidMoves": str(self.validMoves)
        }, indent=2))

        # no piece selected previously
        if not self.selectedPiece:
            if self.piece:
                # a piece was clicked, selecting
                self.selectedPiece = self.piece
            else:
                # square clicked, deselecting
                self.selectedPiece = None
        else:
            # piece selected previously
            if self.piece:
                if self.selectedPiece.color == self.piece.color:
                    # another piece on same team selected (reselect)
                    self.selectedPiece = self.piece
                else:
                    # enemy piece was clicked
                    if (row, col) in self.validMoves:
                        # enemy piece is captured
                        self.move_piece(row, col)
                        self.remove_piece(self.piece)
                    else:
                        # enemy piece is new selection
                        self.selectedPiece = self.piece
            else:
                # a square was clicked
                if (row, col) in self.validMoves:
                    # square is valid, moving piece
                    self.move_piece(row, col)
                else:
                    # square is invalid, deselect
                    self.selectedPiece = None

        # redraw updated board
        self.draw_squares()
        self.draw_pieces()
            

    def draw_squares(self):
        for square in self.squares:
            square.draw(self.canvas)

    def draw_pieces(self):
        for piece in self.pieces:
            piece.draw(self.canvas)

    def find_square(self, row, col):
        for square in self.squares:
            if square.row == row and square.col == col:
                return square

    def find_piece(self, row, col):
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return piece

    def reset_squares(self):
        for square in self.squares:
            square.isSelected = False
            square.isPossible = False
            square.isThreat = False

    def get_valid_moves(self):
        moves = self.selectedPiece.get_possible_moves()
        movesInPlay = self.get_moves_in_play(moves)

        validate_func = None
        if self.selectedPiece.name == "Knight":
            validate_func = self.validate_knight
        elif self.selectedPiece.name == "King":
            validate_func = self.validate_king
        elif self.selectedPiece.name == "Pawn":
            validate_func = self.validate_pawn

        if not validate_func:
            validMoves = []
        else:
            validMoves = validate_func(movesInPlay)
        
        return validMoves

    def remove_piece(self, piece):
        pieceId = self.pieces.index(piece)
        self.pieces.pop(pieceId)

    def move_piece(self, row, col):
        if self.selectedPiece.name == "Pawn":
            self.selectedPiece.hasNotMoved = False
        self.selectedPiece.row = row
        self.selectedPiece.col = col
        self.selectedPiece = None
        self.validMoves = []

    @staticmethod
    def init_squares():
        squares = []
        for row in range(8):
            for col in range(8):
                square = Square(row, col)
                squares.append(square)
        return squares

    @staticmethod
    def init_pieces():
        pieces = []
        for row in range(8):
            for col in range(8):
                if row in (0, 1, 6, 7):
                    color = "black" if row in (0, 1) else "white"

                    if row in (1, 6):
                        piece = Pawn(row, col, color)
                    elif row in (0, 7):
                        if col in (0, 7):
                            piece = Rook(row, col, color)
                        elif col in (1, 6):
                            piece = Knight(row, col, color)
                        elif col in (2, 5):
                            piece = Bishop(row, col, color)
                        elif col == 3:
                            piece = Queen(row, color)
                        elif col == 4:
                            piece = King(row, color)

                    pieces.append(piece)
        return pieces

    @staticmethod
    def get_moves_in_play(moves):
        movesInPlay = []
        for move in moves:
            if move[0] in range(8) and move[1] in range(8):
                movesInPlay.append(move)
        return movesInPlay


def main():
    root = tk.Tk()
    Board(root)
    root.mainloop()


if __name__ == "__main__":
    main()
