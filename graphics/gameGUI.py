import pygame
import sys
from pygame.locals import *

#color arguments in (r, g, b) format
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
# GUI Dimensions
GUI_WIDTH = 640
GUI_HEIGHT = 480
BACKGROUND_COLOR = WHITE
TEXT_COLOR = BLUE

# Board Dimensions
SPACE = 50
BOARD_ROWS = 6 # how tall the board is
BOARD_COLUMNS = 7 # how wide the board is
X_MARGIN = int((GUI_WIDTH - BOARD_COLUMNS * SPACE) / 2) # setting the cordinates of the bottom left cornner of the board
Y_MARGIN = int((GUI_HEIGHT - BOARD_ROWS * SPACE) / 2)


# Game Objects
PLAYER1 = '1'
PLAYER2 = '2'
EMPTY = None
FPS = 30 # refresh rate

# lets see if we can create a gui
def run():
    global DISPLAY, RED_TOKEN, BLACK_TOKEN, BOARD_CELL
    global RED_START_POSITION, BLACK_START_POSITION, CLOCK
    pygame.init()
    DISPLAY = pygame.display.set_mode((GUI_WIDTH, GUI_HEIGHT))
    pygame.display.set_caption('Connect-4')
    # load player tokens
    RED_TOKEN = pygame.image.load("/Users/idanziv/dev/Connect-4/graphics/images/red_token.png")
    RED_TOKEN = pygame.transform.smoothscale(RED_TOKEN, (SPACE, SPACE))
    BLACK_TOKEN = pygame.image.load("/Users/idanziv/dev/Connect-4/graphics/images/black_token.png")
    BLACK_TOKEN = pygame.transform.smoothscale(BLACK_TOKEN, (SPACE, SPACE))
    # load board cell - we will construct the board from this one image
    BOARD_CELL = pygame.image.load("/Users/idanziv/dev/Connect-4/graphics/images/board.png")
    BOARD_CELL = pygame.transform.smoothscale(BOARD_CELL, (SPACE, SPACE))

    # create place holder for player's tokens - will use as drawing canvas
    RED_START_POSITION = pygame.Rect(int(SPACE / 2), GUI_HEIGHT - int(3 * SPACE / 2), SPACE, SPACE)
    BLACK_START_POSITION = pygame.Rect(GUI_WIDTH - int(3 * SPACE / 2), GUI_HEIGHT - int(3 * SPACE / 2), SPACE, SPACE)
    
    CLOCK = pygame.time.Clock()

def dragTokenEvent(board, player):
    is_dragging_token = False
    token_xValue, token_yValue = None, None
    token = None
    if player == PLAYER1:
        token = RED_START_POSITION
    else:
        token = BLACK_START_POSITION
    while True:
        for event in pygame.event.get():
            # check if are trying to leave the game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # check if the user pressed the correct token - for the first time
            elif event.type == MOUSEBUTTONDOWN and not is_dragging_token and token.collidepoint(event.pos):
                is_dragging_token = True
                token_xValue, token_yValue = event.pos
            # track the movement of the mouse
            elif event.type == MOUSEMOTION and is_dragging_token:
                token_xValue, token_yValue = event.pos
            # see if the user "dropped" the disc
            elif event.type == MOUSEBUTTONUP and is_dragging_token:
                # check valid column and return it
                if token_yValue < Y_MARGIN and token_xValue > X_MARGIN and GUI_WIDTH - X_MARGIN:
                    column = int((token_xValue - X_MARGIN) / SPACE)
                    return column
                # if not we need to 'drop' the
                token_xValue = token_yValue = None
            # check if there is a need to print an additional disk or not
            if token_xValue is None: # you only need to check one of the cordinates
                draw_board(board)
            else:
                draw_board(board, {'xValue': token_xValue - int(SPACE / 2), 'yValue': token_yValue - int(SPACE / 2),'player': player})
            refresh()

def droppingTokenAnimation(board, column, player, stop):
    xValue = X_MARGIN + column * SPACE
    yValue = Y_MARGIN - SPACE
    speed = 2
    
    while True:
        yValue += speed
        speed += 2
        # check if we reach the proper location - stop
        if int((yValue - Y_MARGIN) / SPACE) >= stop:
            return
        # draw the board with the extra disk
        draw_board(board, {'xValue': xValue, 'yValue': yValue, 'player': player})
        refresh()

def refresh():
    pygame.display.update()
    CLOCK.tick(FPS)


def draw_board(board, drag_token=None):
    # create the background
    DISPLAY.fill(BACKGROUND_COLOR)
    # creating a surface to draw on, since the blit function requires a rectangle object
    canvas = pygame.Rect(0, 0, SPACE, SPACE)
    # draw the tokens
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            canvas.topleft = (X_MARGIN + (row * SPACE), Y_MARGIN + (column * SPACE))
            if board[row][column] == PLAYER1:
                DISPLAY.blit(RED_TOKEN, canvas)
            elif board[row][column] == PLAYER2:
                DISPLAY.blit(BLACK_TOKEN, canvas)        
    # draw the board cells - we draw it over the the tokens, and because all the tokens and board cells
    # share the same dimensions we don't need to calculate the positioning of the tokens
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            canvas.topleft = (X_MARGIN + (row * SPACE), Y_MARGIN + (column * SPACE))
            DISPLAY.blit(BOARD_CELL, canvas)

    # In the case of a player dragging a token
    if drag_token != None:
        if drag_token['player'] == PLAYER1:
            DISPLAY.blit(RED_TOKEN, (drag_token['xValue'], drag_token['yValue'], SPACE, SPACE))
        else: # the other option
            DISPLAY.blit(BLACK_TOKEN, (drag_token['xValue'], drag_token['yValue'], SPACE, SPACE))
    # draw the players token
    DISPLAY.blit(RED_TOKEN, RED_START_POSITION)
    DISPLAY.blit(BLACK_TOKEN, BLACK_START_POSITION)
    
def create_board():
    board = []
    for x in range(BOARD_ROWS):
        board.append([EMPTY] * BOARD_COLUMNS)
    return board