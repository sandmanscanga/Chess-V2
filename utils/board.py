"""Module contains chess board logic"""
import tkinter as tk
import json

from utils.logger import LOGGER
from utils.bases import Square
from utils.pieces import Pawn, Rook, Knight, Bishop, Queen, King

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods

logger = LOGGER.get_logger('board')

class Board:
    """Contains logic to render and resize board"""

    turn = 0
    board_size = 600

    @classmethod
    def inc_turn(cls):
        """Increments turn"""

        cls.turn += 1

    @classmethod
    def update_board_size(cls, size):
        """Updates board size based on size input"""

        cls.board_size = size

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.canvas = tk.Canvas(self.master,
            width=self.board_size, height=self.board_size)
        Square.update_length(self.board_size / 8)
        self.squares = self.init_squares()
        self.pieces = self.init_pieces()
        self.selected_piece = None
        self.square = None
        self.piece = None
        self.draw_squares()
        self.draw_pieces()
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.pack()
        # self.label = tk.Label(self.master, text=self.turn_color.title(), fg="red")
        # self.label.pack()

    @property
    def selected_piece(self):
        """Return private copy of selected piece"""

        return self.__selected_piece

    @selected_piece.setter
    def selected_piece(self, piece):
        """Sets private copy of selected piece to current piece"""

        if piece:
            self.square.is_selected = True
            self.__selected_piece = piece
            self.valid_moves = self.get_valid_moves()
        else:
            self.__selected_piece = None
            self.valid_moves = []

    @property
    def turn_color(self):
        """Returns team color based on turn index"""

        return "white" if not self.turn % 2 else "black"


    def left_click(self, event):
        """Event handler for left click"""

        self.reset_squares()

        row = event.y // Square.length
        col = event.x // Square.length

        self.square = self.find_square(row, col)
        self.piece = self.find_piece(row, col)

        self.display()

        # no piece selected previously
        if not self.selected_piece:
            if self.piece:
                # a piece was clicked, selecting
                if self.turn_color == self.piece.color:
                    # correct color chosen based on turn color
                    self.selected_piece = self.piece
                else:
                    # incorrect color chosen based on turn color
                    print(f"It's {self.turn_color}'s turn!")
            else:
                # square clicked, deselecting
                self.selected_piece = None
        else:
            # piece selected previously
            if self.piece:
                # a piece was clicked
                if self.selected_piece.color == self.piece.color:
                    # another piece on same team selected (reselect)
                    self.selected_piece = self.piece
                else:
                    # enemy piece was clicked
                    if (row, col) in self.valid_moves:
                        # enemy piece is captured
                        self.move_piece(row, col)
                        self.remove_piece(self.piece)
                        Board.inc_turn()
                    else:
                        # enemy piece is clicked, deselect
                        self.selected_piece = None
            else:
                # a square was clicked
                if (row, col) in self.valid_moves:
                    # square is valid, moving piece
                    self.move_piece(row, col)
                    Board.inc_turn()
                else:
                    # square is invalid, deselect
                    self.selected_piece = None

        # redraw updated board
        self.draw_squares()
        self.draw_pieces()
        # self.label.destroy()
        # self.label = tk.Label(self.master, text=self.turn_color.title(), fg="red")
        # self.label.pack()

    def on_resize(self, _):
        """Event handler for window resize"""

        width = self.master.winfo_width()
        height = self.master.winfo_height()
        new_size = width if width < height else height
        self.board_size = new_size - (new_size % 8)
        self.canvas.config(width=self.board_size, height=self.board_size)
        self.master.geometry(f"{self.board_size}x{self.board_size}")
        Square.update_length(self.board_size / 8)
        self.draw_squares()
        self.draw_pieces()

    def draw_squares(self):
        """Draws squares to board"""

        for square in self.squares:
            square.draw(self.canvas)

    def draw_pieces(self):
        """Draws pieces to board"""

        for piece in self.pieces:
            piece.draw(self.canvas)

    def find_square(self, row, col):
        """Locates a square on the board based on input"""

        found_square = None
        for square in self.squares:
            if square.row == row and square.col == col:
                found_square = square
                break

        return found_square

    def find_piece(self, row, col):
        """Locates a piece on the board based on input"""

        found_piece = None
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                found_piece = piece
                break

        return found_piece

    def reset_squares(self):
        """Resets state of squares"""

        for square in self.squares:
            square.reset_state()

    def get_valid_moves(self):
        """Retrieves valid moves for selected piece"""

        validate_func = None
        if self.selected_piece.name == "Knight":
            validate_func = self.validate_knight
        elif self.selected_piece.name == "King":
            validate_func = self.validate_king
        elif self.selected_piece.name == "Pawn":
            validate_func = self.validate_pawn
        elif self.selected_piece.name == "Queen":
            validate_func = self.validate_queen
        elif self.selected_piece.name == "Rook":
            validate_func = self.validate_rook
        elif self.selected_piece.name == "Bishop":
            validate_func = self.validate_bishop
        else:
            raise Exception("Unidentified piece.")

        valid_moves = validate_func()
        return valid_moves

    def remove_piece(self, piece):
        """Removes piece from board"""

        piece_id = self.pieces.index(piece)
        self.pieces.pop(piece_id)

    def move_piece(self, row, col):
        """Moves selected piece to coordinates"""

        if self.selected_piece.name == "Pawn":
            self.selected_piece.hasNotMoved = False
        self.selected_piece.row = row
        self.selected_piece.col = col
        self.selected_piece = None
        self.valid_moves = []

    def validate_pawn(self):
        """Returns valid moves for pawn"""

        (diagonals, straight) = self.selected_piece.get_possible_moves()

        valid_moves = []
        for move in diagonals:
            pos_square = self.find_square(*move)
            pos_piece = self.find_piece(*move)
            if pos_piece:
                if pos_piece.color != self.selected_piece.color:
                    # enemy piece, attack
                    pos_square.is_threat = True
                    valid_moves.append(move)

        for move in straight:
            pos_square = self.find_square(*move)
            pos_piece = self.find_piece(*move)
            if not pos_piece:
                pos_square.is_possible = True
                valid_moves.append(move)
            else:
                break

        return valid_moves

    def validate_rook(self):
        """Returns valid moves for rook"""

        moves = self.selected_piece.get_possible_moves()

        valid_moves = []
        for _moves in moves:
            for move in _moves:
                pos_square = self.find_square(*move)
                pos_piece = self.find_piece(*move)
                if pos_piece:
                    if pos_piece.color != self.selected_piece.color:
                        # enemy piece
                        pos_square.is_threat = True
                        valid_moves.append(move)
                    break
                pos_square.is_possible = True
                valid_moves.append(move)

        return valid_moves

    def validate_knight(self):
        """Returns valid moves for knight"""

        moves = self.selected_piece.get_possible_moves()

        valid_moves = []
        for move in moves:
            pos_square = self.find_square(*move)
            pos_piece = self.find_piece(*move)
            if pos_piece:
                if pos_piece.color != self.selected_piece.color:
                    # enemy piece, attack
                    pos_square.is_threat = True
                    valid_moves.append(move)
            else:
                pos_square.is_possible = True
                valid_moves.append(move)

        return valid_moves

    def validate_bishop(self):
        """Returns valid moves for bishop"""

        moves = self.selected_piece.get_possible_moves()

        valid_moves = []
        for _moves in moves:
            for move in _moves:
                pos_square = self.find_square(*move)
                pos_piece = self.find_piece(*move)
                if pos_piece:
                    if pos_piece.color != self.selected_piece.color:
                        # enemy piece
                        pos_square.is_threat = True
                        valid_moves.append(move)
                    break
                pos_square.is_possible = True
                valid_moves.append(move)

        return valid_moves

    def validate_queen(self):
        """Returns valid moves for queen"""

        moves = self.selected_piece.get_possible_moves()

        valid_moves = []
        for _moves in moves:
            for move in _moves:
                pos_square = self.find_square(*move)
                pos_piece = self.find_piece(*move)
                if pos_piece:
                    if pos_piece.color != self.selected_piece.color:
                        # enemy piece
                        pos_square.is_threat = True
                        valid_moves.append(move)
                    break
                pos_square.is_possible = True
                valid_moves.append(move)

        return valid_moves

    def validate_king(self):
        """Returns valid moves for king"""

        moves = self.selected_piece.get_possible_moves()

        valid_moves = []
        for move in moves:
            pos_square = self.find_square(*move)
            pos_piece = self.find_piece(*move)
            if pos_piece:
                if pos_piece.color != self.selected_piece.color:
                    # enemy piece, attack
                    pos_square.is_threat = True
                    valid_moves.append(move)
            else:
                pos_square.is_possible = True
                valid_moves.append(move)

        return valid_moves

    def display(self):
        """Prints game data"""

        logger.info(json.dumps({
            "square": str(self.square),
            "piece": str(self.piece),
            "selected_piece": str(self.selected_piece),
            "vailidMoves": str(self.valid_moves),
            "turn": str(self.turn),
            "squareLength": self.square.length if self.square else None,
            "pieceSize": self.piece.get_font_size() if self.piece else None
        }, indent=2))

    @staticmethod
    def init_squares():
        """Initializes board squares"""

        squares = []
        for row in range(8):
            for col in range(8):
                square = Square(row, col)
                squares.append(square)
        return squares

    @staticmethod
    def init_pieces():
        """Initializes board pieces"""

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
