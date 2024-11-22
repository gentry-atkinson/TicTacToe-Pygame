# Author: Gentry Atkinson
# Organization: St. Edward's University
# Date: November 22, 2024

import pygame
import os

# Global Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
FPS = 60

# Load Images
BOARD = pygame.transform.scale(
    pygame.image.load(os.path.join('imgs', 'board.png')), (WINDOW_WIDTH, WINDOW_HEIGHT)
)

if __name__ == '__main__':

    # Init Game
    pygame.init()
    pygame.display.set_caption('Tic Tac Toe')
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    # Main Game Loop
    while running:
        # Get delta time
        clock.tick(FPS)
        dt = clock.get_time()

        # Get Keyboard Inputs
        keys = pygame.key.get_pressed()