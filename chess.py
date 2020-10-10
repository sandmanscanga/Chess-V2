import tkinter as tk


class Piece:
    
    length = 75

    def __init__(self, row, col, char, color, name):
        (self.row, self.col) = (row, col)
        self.char = char
        self.color = color
        self.name = name

    def draw(self, canvas):
        x = (self.length * self.col) + (self.length / 2) 
        y = (self.length * self.row) + (self.length / 2)
        canvas.create_text(x, y, text=chr(self.char), 
            fill=self.color, font=("", 36))

# king = 0x265a, queen = 0x265b, rook = 0x265c, bishop = 0x265d, knight = 0x265e, pawn = 0x265f

class Square:

    length = 75
    colors = ("#212121", "#bdbdbd")

    def __init__(self, row, col):
        (self.row, self.col) = (row, col)

    def draw(self, canvas):
        x1 = self.length * self.col
        y1 = self.length * self.row
        x2 = self.length + x1
        y2 = self.length + y1
        coords = (x1, y1, x2, y2)

        color_id = (self.row + self.col) % 2
        color = self.colors[color_id]

        canvas.create_rectangle(*coords, fill=color)

class Board:

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
                    
                    # setting character
                    if row in (1,6):
                        char = 0x265f
                        name = "Pawn"
                    elif row in (0,7):
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
                        color = "#000000"
                    elif row in (6,7):
                        color = "#ffffff"     

                    piece = Piece(row, col, char, color, name)
                    self.pieces.append(piece)

        self.draw_squares()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.pack()

    def left_click(self, event):
        col = event.x // 75
        row = event.y // 75
        key = (col, row)

        # square = squares.lookup(key)
        # piece = pieces.lookup(key)

        # if piece.is_not_selected:
        #     square.select_it


        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                print(row, col, piece.name)
                break
        else:
            print(row,col)


    def draw_squares(self):
        for square in self.squares:
            square.draw(self.canvas)

    def draw_pieces(self):
        for piece in self.pieces:
            piece.draw(self.canvas)


def main():
    root = tk.Tk()
    Board(root)
    root.mainloop()


if __name__ == "__main__":
    main()
