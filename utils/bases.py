"""Module contains square and piece logic"""
import sys


class Square:
    """Contains logic and properties for square"""

    length = 75
    colors = ("#455a64", "#bdbdbd")  # dark blue/grey, light grey
    selectedColor = "#ffff00"  # Gold
    possibleColor = "#00e000"  # Green
    threatColor = "#c62828"  # Red


    @classmethod
    def update_length(cls, length):
        """Updates square length based on input"""

        cls.length = int(length)

    def __init__(self, row, col):
        (self.row, self.col) = (row, col)
        self.color = self.colors[(self.row + self.col) % 2]
        self.is_selected = False
        self.is_possible = False
        self.is_threat = False

    def __str__(self):
        return self.position + str(self.length)

    @property
    def position(self):
        """Property for square position"""

        return "ABCDEFGH"[self.col] + str(self.row + 1)

    @property
    def x_1(self):
        """Top left x coordinate for square"""

        return self.length * self.col

    @property
    def y_1(self):
        """Top left y coordinate for square"""

        return self.length * self.row

    @property
    def x_2(self):
        """Bottom right x coordinate for square"""

        return self.length + self.x_1

    @property
    def y_2(self):
        """Bottom right y coordinate for square"""

        return self.length + self.y_1

    @property
    def coords(self):
        """Compiled all corners into coordinates"""

        return (self.x_1, self.y_1, self.x_2, self.y_2)

    def draw(self, canvas):
        """Draw square to canvas"""

        if self.is_selected:
            canvas.create_rectangle(*self.coords, fill=self.selectedColor)
        elif self.is_possible:
            canvas.create_rectangle(*self.coords, fill=self.possibleColor)
        elif self.is_threat:
            canvas.create_rectangle(*self.coords, fill=self.threatColor)
        else:
            canvas.create_rectangle(*self.coords, fill=self.color)

    def reset_state(self):
        """Reset state of square"""

        self.is_threat = False
        self.is_possible = False
        self.is_selected = False


class Piece:
    """Contains logic and properties for piece"""

    white = "white"
    black = "black"

    def __init__(self, row, col, *args):
        (self.row, self.col) = (row, col)
        (char, color, name) = args
        self.char = chr(char)
        self.color = color
        self.name = name

    def __str__(self):
        return f"({self.name}, {self.position})"

    @property
    def position(self):
        """Property for piece position"""

        return "ABCDEFGH"[self.col] + str(self.row + 1)

    def draw(self, canvas):
        """Draw piece to canvas"""

        font_size = self.get_font_size()
        x_pos = (Square.length * self.col) + (Square.length / 2)
        y_pos = (Square.length * self.row) + (Square.length / 2)
        canvas.create_text(x_pos, y_pos, text=self.char,
            fill=self.color, font=("", font_size))

    @staticmethod
    def get_font_size():
        """Cross platform compatability for font size"""

        if sys.platform == "linux":
            font_size = int(Square.length * 0.74667) # 74.667% of 75 is 56
        else:
            font_size = int(Square.length * 0.48) # 48% of 75 is 36
        return font_size

    @staticmethod
    def get_moves_in_play(moves):
        """Return moves within the board"""

        moves_in_play = []
        for move in moves:
            if move[0] in range(8) and move[1] in range(8):
                moves_in_play.append(move)
        return moves_in_play
