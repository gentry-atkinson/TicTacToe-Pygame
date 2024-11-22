# Author: Gentry Atkinson
# Organization: St. Edward's University
# Date: November 22, 2024

import pygame
import os

# Global Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
FPS = 60
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Load Images
BOARD = pygame.transform.scale(
    pygame.image.load(os.path.join('imgs', 'board.png')), (WINDOW_WIDTH, WINDOW_HEIGHT)
)

if __name__ == '__main__':

    # Init Game
    pygame.init()
    pygame.display.set_caption('Tic Tac Toe')
    clock = pygame.time.Clock()
    running = True

    highlighted = None
    Xs = []
    Os = []

    # Main Game Loop
    while running:
        # Get delta time
        clock.tick(FPS)
        dt = clock.get_time()

        # Get Keyboard Inputs
        keys = pygame.key.get_pressed()

        # Break main loop on quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.blit(BOARD, (0, 0))
        pygame.display.update()