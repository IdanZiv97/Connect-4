import numpy as np

PLAYER1 = 1
PLAYER2 = 2
NUM_ROWS = 6
NUM_COLS = 7
TOP_ROW = NUM_ROWS -1

def create_board():
    """
    this function creates the 
    """
    board = np.zeros((NUM_ROWS,NUM_COLS))
    return board

def is_valid_column(board, column):
    """
    Checks if the column inserted by the user is full or not:
    if the row is full than the top element should have the value 1, else the value 0
    """
    return board[TOP_ROW][column] == 0

def play_turn(board, col, row, disc):
    # place the disc
    board[row][col] = disc

def find_next_open_slot(board, col):
    for row in range(NUM_ROWS):
        if board[row][col] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0))

# game engine
game_over = False
board = create_board()
print_board(board)
turn = PLAYER1
while not game_over:
    if turn == PLAYER1:
        col = int(input("Player 1 enter a row index (0-6)"))
        if is_valid_column(board, col):
            row = find_next_open_slot(board, col)
            play_turn(board, col, row, PLAYER1)
        turn = PLAYER2
    else: # turn == PLAYER2
        col = int(input("Player 2 enter a row index (0-6)"))
        if is_valid_column(board, col):
            row = find_next_open_slot(board, col)
            play_turn(board, col, row, PLAYER2)
        turn = PLAYER1
    print_board(board)

