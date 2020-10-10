# Notes

Board
    + squares
        - row, col
    + pieces
        - row, col

key = (row, col)

if square.has_piece():
    square.draw_piece()

```python

board_keys = []
for row in range(8):
    for col in range(8):
        board_keys.append([row, col])

```


## Left Click

if first left click:
    1. click a piece
    2. highlight the square
    3. show legal moves for that piece
elif second left click:
    1. move the piece to the square