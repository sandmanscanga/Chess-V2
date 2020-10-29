import tkinter as tk
import json
import sys
from utils.bases import Square, Piece, MoveValidation
from utils.pieces import Pawn, Rook, Knight, Bishop, Queen, King

if sys.platform == "linux":
    window_arg = "-zoomed"
else:
    window_arg = "-fullscreen"


class Board(MoveValidation):

    turn = 0
    boardSize = 600

    @classmethod
    def inc_turn(cls):
        cls.turn += 1

    @classmethod
    def update_board_size(cls, size):
        cls.boardSize = size

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.canvas = tk.Canvas(self.master,
            width=self.boardSize, height=self.boardSize)
        Square.update_length(self.boardSize / 8)
        Piece.update_square_length(Square.length)
        self.squares = self.init_squares()
        self.pieces = self.init_pieces()
        self.selectedPiece = None
        self.draw_squares()
        self.draw_pieces()
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.pack()
        # self.label = tk.Label(self.master, text=self.turnColor.title(), fg="red")
        # self.label.pack()

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
        # self.label.destroy()
        # self.label = tk.Label(self.master, text=self.turnColor.title(), fg="red")
        # self.label.pack()
            
    def on_resize(self, event):
        # (width, height) = (event.width, event.height)
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        newSize = width if width < height else height
        # Board.update_board_size(newSize - 4)
        self.boardSize = newSize - (newSize % 8)
        self.master.geometry(f"{self.boardSize}x{self.boardSize}")
        self.canvas.config(width=self.boardSize, height=self.boardSize)
        Square.update_length(self.boardSize / 8)
        Piece.update_square_length(Square.length)
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
            "squareLength": self.square.length if self.square else None,
            "pieceSize": self.piece.get_piece_size() if self.piece else None
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


"""class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)"""


class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('Chess V2')
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        # self.geometry(f"{w}x{h}")
        self.fullscreenState = False
        self.attributes(window_arg, self.fullscreenState)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
        # self.bind("<Configure>", lambda e:print(f"on resize: {event.width}, {event.height}"))
        self.board = Board(self)
        self.mainloop()

    def toggle_fullscreen(self, event):
        self.fullscreenState = not self.fullscreenState
        self.attributes(window_arg, self.fullscreenState)

    def exit_fullscreen(self, event):
        self.attributes(window_arg, False)

    def on_resize(self, event):
        print(f"on resize: {event.width}, {event.height}")


def main():
    App()


if __name__ == "__main__":
    main()
