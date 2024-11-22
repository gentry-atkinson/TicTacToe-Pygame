# Author: Gentry Atkinson
# Organization: St. Edward's University
# Date: November 22, 2024

import pygame
import os
from random import randint

# Global Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
ITEM_WIDTH = 130
ITEM_HEIGHT = 130
FPS = 30
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Load Images
BOARD = pygame.transform.scale(
    pygame.image.load(os.path.join('imgs', 'board.png')), (WINDOW_WIDTH, WINDOW_HEIGHT)
)
SELECTOR = pygame.transform.scale(
    pygame.image.load(os.path.join('imgs', 'selector.png')), (ITEM_WIDTH, ITEM_HEIGHT)
)
X_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join('imgs', 'X.png')), (ITEM_WIDTH, ITEM_HEIGHT)
)
O_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join('imgs', 'O.png')), (ITEM_WIDTH, ITEM_HEIGHT)
)


# Function to draw screen
def draw(screen, highlighted, Xs, Os):
    board_positions = {
        (0,0) : (160, 150),
        (0,1) : (350, 150),
        (0,2) : (530, 150),
        (1,0) : (160, 330),
        (1,1) : (350, 330),
        (1,2) : (530, 330),
        (2,0) : (160, 530),
        (2,1) : (350, 530),
        (2,2) : (530, 530),
    }
    screen.blit(BOARD, (0, 0))
    screen.blit(SELECTOR, board_positions[highlighted])
    for x in Xs:
        screen.blit(X_IMG, board_positions[x])
    for o in Os:
        screen.blit(O_IMG, board_positions[o])

def computer_move(Xs, Os) -> tuple:
    return (randint(0, 2), randint(0,2))

def x_winner(Xs) -> bool:
    for row in range(0,3):
        if (row, 0) in Xs and  (row, 1) in Xs and  (row, 2) in Xs:
            return True
    for col in range(0,3):
        if (0, col) in Xs and  (1, col) in Xs and  (2, col) in Xs:
            return True
    if (0,0) in Xs and (1,1) in Xs and (2,2) in Xs:
        return True
    if (0,2) in Xs and (1,1) in Xs and (2,0) in Xs:
        return True
    return False

def o_winner(Os) -> bool:
    for row in range(0,3):
        if (row, 0) in Os and  (row, 1) in Os and  (row, 2) in Os:
            return True
    for col in range(0,3):
        if (0, col) in Os and  (1, col) in Os and  (2, col) in Os:
            return True
    if (0,0) in Os and (1,1) in Os and (2,2) in Os:
        return True
    if (0,2) in Os and (1,1) in Os and (2,0) in Os:
        return True
    return False

if __name__ == '__main__':

    # Init Game
    pygame.init()
    pygame.display.set_caption('Tic Tac Toe')
    clock = pygame.time.Clock()
    running = True
    pygame.key.set_repeat()

    highlighted = (1,1)
    Xs = set()
    Os = set()

    pressable = True
    player_turn = True

    # Main Game Loop
    while running:
        # Get delta time
        clock.tick(FPS)
        dt = clock.get_time()

        # Get Keyboard Inputs
        keys = pygame.key.get_pressed()
        # Handle keyboard input
        if keys[pygame.K_UP] and pressable:
            highlighted = (max(highlighted[0]-1, 0), highlighted[1])
            pressable = False
        elif keys[pygame.K_DOWN] and pressable:
            highlighted = (min(highlighted[0]+1, 2), highlighted[1])
            pressable = False
        elif keys[pygame.K_LEFT] and pressable:
            highlighted = (highlighted[0], max(highlighted[1]-1, 0))
            pressable = False
        elif keys[pygame.K_RIGHT] and pressable:
            highlighted = (highlighted[0], min(highlighted[1]+1, 2))
            pressable = False
        elif keys[pygame.K_SPACE] and pressable and player_turn:
            Xs.add(highlighted)
            player_turn = False
            pressable = False
        else:
            pressable = True

        if x_winner(Xs):
            print("X wins")

        if not player_turn:
            Os.add(computer_move(Xs, Os))
            player_turn = True
            pass

        if o_winner(Os):
            print("O wins")
        

        # Break main loop on quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(SCREEN, highlighted, Xs, Os)
        keys = None
        pygame.display.update()