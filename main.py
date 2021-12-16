from typing import Pattern
from graphics import gameGUI as GUI
import numpy as np
from scipy.signal import convolve2d

class Game:
    SIZE = 42
    def __init__(self, game_board, patterns):
        self.board = game_board
        self.turn = GUI.PLAYER1
        self.winner = None
        self.patterns = patterns
        self.open_slots = self.SIZE

    # check for winner
    def is_game_over(self):
        # create a nparray from the board
        arr = np.asarray(self.board)
        # create players array
        player1_board = (arr == 1)
        player2_board = (arr == 2)
        player1_board = player1_board.astype(int)
        player2_board = player2_board.astype(int)
        for pattern in patterns:
            if ((convolve2d(player1_board, pattern, mode="valid")) == 4).any():
                result1 = True
                break
        for pattern in patterns:
            if (convolve2d(player2_board, pattern, mode="valid") == 4).any():
                result2 = True
                break
        
    
    def play_next_turn(self):
        if self.turn == GUI.PLAYER1:
            self.make_move(GUI.PLAYER1)
            self.turn = GUI.PLAYER2
        else: # PLAYER2 move
            self.make_move(GUI.PLAYER2)
            self.turn = GUI.PLAYER1
    
    def get_next_open_slot(self, board, column):
        for row in range(GUI.BOARD_ROWS, -1, -1):
            if board[column][row] == GUI.EMPTY:
                return row

    def make_move(self, player):
        """
        We need tp get the column for the user by dragging mouse so we need to 
        handle it from the GUI
        """
        column = None
        # keep running until you find a column
        while column is None:
            column = GUI.dragTokenEvent(self.board, player)
            # check for correct column index
            if not column <= column <= GUI.BOARD_COLUMNS - 1:
                column = None
            # check if column is empty
            if not self.isValidColumn(self.board, column):
                column = None
            if column is None:
                print("\n Invalid move")
        # create the animation of dropping the disc
        # animate
        GUI.droppingTokenAnimation(self.board, column, player, self.get_next_open_slot(self.board, column))
        self.board[column][self.get_next_open_slot(self.board, column)] = player

    
    def isValidColumn(self, board, column) -> bool:
        if board[column][0] is GUI.EMPTY:
            return True
        else:
            return False

def create_patterns():
    patterns = []
    vertical_pattern = np.array([[1,1,1,1]])
    patterns.append(vertical_pattern)
    horizontal_pattern = vertical_pattern.transpose()
    patterns.append(horizontal_pattern)
    diagnoal1_pattern = np.eye(4, dtype = np.uint8)
    patterns.append(diagnoal1_pattern)
    diagnoal2_pattern = np.fliplr(diagnoal1_pattern)
    patterns.append(diagnoal2_pattern)
    return patterns

if __name__ == "__main__":
    print("Starting Connect-4 game..\n")
    GUI.run()
    while True:
        board = GUI.create_board()
        GUI.draw_board(board)
        GUI.refresh()
        patterns = create_patterns()
        game = Game(board, patterns)
        while not game.is_game_over():
            game.play_next_turn()
            GUI.draw_board(game.board)
            GUI.refresh()
        