import tkinter as tk
import json
from bases import Square, Piece, MoveValidation
from pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Board(MoveValidation):

    turn = 0

    @classmethod
    def inc_turn(cls):
        cls.turn += 1

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
        label = tk.Label()

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

    @property
    def turnColor(self):
        return "white" if not self.turn % 2 else "black"
    

    def left_click(self, event):
        self.reset_squares()

        row = event.y // Square.length
        col = event.x // Square.length

        self.square = self.find_square(row, col)
        self.piece = self.find_piece(row, col)

        self.display()

        # no piece selected previously
        if not self.selectedPiece:
            if self.piece:
                # a piece was clicked, selecting
                if self.turnColor == self.piece.color:
                    # correct color chosen based on turn color
                    self.selectedPiece = self.piece
                else:
                    # incorrect color chosen based on turn color
                    print(f"It's {self.turnColor}'s turn!")
            else:
                # square clicked, deselecting
                self.selectedPiece = None
        else:
            # piece selected previously
            if self.piece:
                # a piece was clicked
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
                        # enemy piece is clicked, deselect
                        self.selectedPiece = None
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
        validate_func = None
        if self.selectedPiece.name == "Knight":
            validate_func = self.validate_knight
        elif self.selectedPiece.name == "King":
            validate_func = self.validate_king
        elif self.selectedPiece.name == "Pawn":
            validate_func = self.validate_pawn
        elif self.selectedPiece.name == "Queen":
            validate_func = self.validate_queen
        elif self.selectedPiece.name == "Rook":
            validate_func = self.validate_rook
        elif self.selectedPiece.name == "Bishop":
            validate_func = self.validate_bishop
        else:
            raise Exception("Unidentified piece.")

        validMoves = validate_func()
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
        Board.inc_turn()

    def display(self):
        print(json.dumps({
            "square": str(self.square),
            "piece": str(self.piece),
            "selectedPiece": str(self.selectedPiece),
            "vailidMoves": str(self.validMoves),
            "turn": str(self.turn),
        }, indent=2))

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


def main():
    root = tk.Tk()
    Board(root)
    root.mainloop()


if __name__ == "__main__":
    main()
