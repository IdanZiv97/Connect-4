from graphics import gameGUI as GUI

class Game:
    def __init__(self, game_board):
        self.board = game_board
        self.turn = GUI.PLAYER1

    def is_over(self):
       result = self.check_board(board, self.turn)
    
    def check_board(self, board, player):
        pass

    def play_next_turn(self):
        if self.turn == GUI.PLAYER1:
            self.make_move(GUI.PLAYER1)
            self.turn = GUI.PLAYER2
        else: # PLAYER2 move
            self.make_move(GUI.PLAYER2)
            self.turn = GUI.PLAYER1
    
    def get_next_open_slot(board, column):
        for row in range(GUI.BOARD_ROWS):
            if board[row][column] == GUI.EMPTY:
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
        #update the the board
        board[self.get_next_open_slot(board, column)][column] == player


    
    def isValidColumn(self, board, column) -> bool:
        if board[0][column] is GUI.EMPTY:
            return True
        else:
            return False

if __name__ == "__main__":
    print("Starting Connect-4 game..\n")
    GUI.run()
    while True:
        board = GUI.create_board()
        GUI.draw_board(board)
        GUI.refresh()
        game = Game(board)
        while True:
            game.play_next_turn()
            GUI.draw_board(game.board)
            GUI.refresh()
        