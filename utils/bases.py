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

    @staticmethod
    def gen_moves_in_play(moves):
        for move in moves:
            if move[0] in range(8) and move[1] in range(8):
                yield move


class MoveValidation:

    def validate_pawn(self):
        moves = self.selectedPiece.get_possible_moves()
        diagonals = moves.get("diagonals")
        straight = moves.get("straight")

        validMoves = []
        for move in diagonals:
            posSquare = self.find_square(*move)
            posPiece = self.find_piece(*move)
            if posPiece:
                if posPiece.color != self.selectedPiece.color:
                    # enemy piece, attack
                    posSquare.isThreat = True
                    validMoves.append(move)
        for move in straight:
            posSquare = self.find_square(*move)
            posPiece = self.find_piece(*move)
            if not posPiece:
                posSquare.isPossible = True
                validMoves.append(move)
            else:
                break
        return validMoves

    def validate_rook(self):
        moves = self.selectedPiece.get_possible_moves()       

        validMoves = []
        for _moves in moves.values():
            for move in _moves:
                posSquare = self.find_square(*move)
                posPiece = self.find_piece(*move)
                if posPiece:
                    if posPiece.color != self.selectedPiece.color:
                        # enemy piece
                        posSquare.isThreat = True
                        validMoves.append(move)
                    break    
                else:
                    posSquare.isPossible = True
                    validMoves.append(move)
        return validMoves

    def validate_knight(self):
        moves = self.selectedPiece.get_possible_moves()
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

    def validate_bishop(self):
        moves = self.selectedPiece.get_possible_moves()       

        validMoves = []
        for _moves in moves.values():
            for move in _moves:
                posSquare = self.find_square(*move)
                posPiece = self.find_piece(*move)
                if posPiece:
                    if posPiece.color != self.selectedPiece.color:
                        # enemy piece
                        posSquare.isThreat = True
                        validMoves.append(move)
                    break    
                else:
                    posSquare.isPossible = True
                    validMoves.append(move)
        return validMoves

    def validate_queen(self):
        moves = self.selectedPiece.get_possible_moves()       

        validMoves = []
        for _moves in moves.values():
            for move in _moves:
                posSquare = self.find_square(*move)
                posPiece = self.find_piece(*move)
                if posPiece:
                    if posPiece.color != self.selectedPiece.color:
                        # enemy piece
                        posSquare.isThreat = True
                        validMoves.append(move)
                    break    
                else:
                    posSquare.isPossible = True
                    validMoves.append(move)
        return validMoves

    def validate_king(self):
        moves = self.selectedPiece.get_possible_moves()
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
