import tkinter as tk


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
        for row in range(8):
            for col in range(8):
                square = Square(row, col)
                self.squares.append(square)

        self.draw_squares()

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

        print(key)

    def draw_squares(self):
        for square in self.squares:
            square.draw(self.canvas)


def main():
    root = tk.Tk()
    Board(root)
    root.mainloop()


if __name__ == "__main__":
    main()
