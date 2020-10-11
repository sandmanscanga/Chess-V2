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
    selectedColor = "#4dd0e1"
    possibleColor = "#26c6da"
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
        char = 0x265f
        name = "Pawn"
        super().__init__(row, col, char, color, name)

    def get_possible_moves(self):
        moves = []
        if self.color == "white":
            moves.append((self.row - 1), self.col)
            if self.hasNotMoved:
                moves.append((self.row - 2), self.col)
        else:
            moves.append((self.row + 1), self.col)
            if self.hasNotMoved:
                moves.append((self.row + 2), self.col)


class Rook:
    pass

class Knight:
    pass

class Bishop:
    pass

class Queen:
    pass

class King:
    pass


class Board:

    clickedLast = None
    piecePrimed = False

    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=600, height=600)

        ## create the initial squares
        self.squares = []
        self.pieces = []
        for row in range(8):
            for col in range(8):
                square = Square(row, col)
                self.squares.append(square)
                if row in (0,1,6,7):
                    
                    ## Pawn
                    if row in (1, 6):
                        if row == 1:
                            pawn = Pawn(row, col, "black")
                        else:
                            pawn = Pawn(row, col, "white")

                        self.pieces.append(pawn)
                        continue

                    # setting character
                    if row in (0,7):
                        if col in (0,7):
                            char = 0x265c
                            name = "Rook"
                        elif col in (1,6):
                            char = 0x265e
                            name = "Knight"
                        elif col in (2,5):
                            char = 0x265d
                            name = "Bishop"
                        elif col == 3: 
                            char = 0x265b
                            name = "Queen"
                        elif col == 4:
                            char = 0x265a
                            name = "King"

                    # setting color
                    if row in (0,1):
                        color = Piece.black
                    elif row in (6,7):
                        color = Piece.white    

                    piece = Piece(row, col, char, color, name)
                    self.pieces.append(piece)

        self.draw_squares()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.pack()

    def left_click(self, event):
        col = event.x // Square.length
        row = event.y // Square.length

        selectedSquare = self.find_square(row, col)  
        selectedPiece = self.find_piece(row, col)
        if selectedPiece:
            print(selectedSquare, selectedPiece)
        else:
            print(selectedSquare, "No piece selected")

        if self.clickedLast == selectedSquare:
            selectedSquare.isSelected = False
            self.clickedLast = None
        else:
            selectedSquare.isSelected = True
            self.clickedLast = selectedSquare

        if selectedPiece:
            if selectedPiece.name == "Pawn":
                ## get possible moves for pawn
                selectedPiece.move()
                selectedSquare.isSelected = False

        self.draw_squares()
        self.draw_pieces()

        selectedSquare.isSelected = False

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


def main():
    root = tk.Tk()
    Board(root)
    root.mainloop()


if __name__ == "__main__":
    main()
