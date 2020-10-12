import tkinter as tk
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
    isSelected = False
    isPossible = False

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
        return f"Square ({self.row}, {self.col}) "

    def draw(self, canvas):
        if self.isSelected:
            canvas.create_rectangle(*self.coords, fill=self.selectedColor)
        elif self.isPossible:
            canvas.create_rectangle(*self.coords, fill=self.possibleColor)
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
        return f"{self.name} ({self.row}, {self.col}) {self.char} {self.color}"

    def draw(self, canvas):
        x = (Square.length * self.col) + (Square.length / 2) 
        y = (Square.length * self.row) + (Square.length / 2)
        canvas.create_text(x, y, text=self.char, 
            fill=self.color, font=("", piece_size))


class Pawn(Piece):

    hasNotMoved = True
    
    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265f, color, "Pawn")


class Rook(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265c, color, "Rook")


class Knight(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265e, color, "Knight")

class Bishop(Piece):

    def __init__(self, row, col, color):
        super().__init__(row, col, 0x265d, color, "Bishop")

class Queen(Piece):
    
    def __init__(self, row, color):
        super().__init__(row, 3, 0x265b, color, "Queen")

class King(Piece):
    
    def __init__(self, row, color):
        super().__init__(row, 4, 0x265a, color, "King")


class Board:

    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=600, height=600)
        self.squares = self.init_squares()
        self.pieces = self.init_pieces()
        self.draw_squares()
        self.draw_pieces()
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.pack()

    def left_click(self, event):
        """
            Nothing is primed
                1. Click square with no piece (deselect)
                2. Click piece (select)

            Piece is primed
                1. Click square with no piece (deselect)
                2. Click primed piece (deselect)
                3. Click unprimed piece (reselect)
                4. Click possible move (move piece, deselect)
                5. Click opponent piece (move piece, deselect, remove opponent piece)
        """
        pass

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
