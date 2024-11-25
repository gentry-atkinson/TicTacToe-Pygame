# Author: Gentry Atkinson
# Organization: St. Edward's University
# Date: November 22, 2024

import pygame
import os
from random import randint, choice

# Global Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
ITEM_WIDTH = 130
ITEM_HEIGHT = 130
FPS = 20
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
def draw(screen, highlighted, Xs, Os, x_score_label, o_score_label, win_label):
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
    score_positions = {
        'x' : (300, 20),
        'o' : (640, 20)
    }
    screen.blit(BOARD, (0, 0))
    screen.blit(SELECTOR, board_positions[highlighted])
    for x in Xs:
        screen.blit(X_IMG, board_positions[x])
    for o in Os:
        screen.blit(O_IMG, board_positions[o])
    if x_score_label:
        screen.blit(x_score_label, score_positions['x'])
    if o_score_label:
        screen.blit(o_score_label, score_positions['o'])
    if win_label:
        screen.blit(win_label, (120, 730))

def computer_move(Xs, Os) -> tuple:
    def get_moves(Xs, Os): 
        possible_moves = set([(a, b) for a in range(3) for b in range(3)])
        possible_moves = possible_moves.difference(Xs, Os)
        return list(possible_moves)
    
    def evaluate(Xs, Os) -> int:
        score = 0
        # Winning is good
        if o_winner(Os):
            score += 100
        
        # Rows w/ two Os is good
        for r in range(3):
            if len(set([(r,0), (r,1), (r,2)]).intersection(Os)) >= 2:
                score += 10

        # Columns w/ two Os is good
        for c in range(3):
            if len(set([(0, c), (1, c), (2, c)]).intersection(Os)) >= 2:
                score += 10

        # Diagnol w/ two Os is good
        if len(set([(0, 0), (1, 1), (2, 2)]).intersection(Os)) >= 2:
                score += 20

        # Diagnol w/ two Os is good
        if len(set([(0, 2), (1, 1), (2, 0)]).intersection(Os)) >= 2:
                score += 20

        return score

    # Evaluate every possible move
    possible_moves = get_moves(Xs, Os)
    evals = dict()
    for move in possible_moves:
        print('move', move)
        new_Os = Os.copy()
        new_Os.add(move)
        evals[move] = evaluate(Xs, new_Os)
    evals = {i:j for (i, j) in sorted(evals.items(), key=lambda x: x[1])}

    # Return the move with the highest evaluation
    return list(evals.keys())[-1]

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

    # Main Font
    main_font = pygame.font.Font(os.path.join('font', 'slkscr.ttf'), 60)

    highlighted = (1,1)
    Xs = set()
    Os = set()

    X_score = 0
    O_score = 0

    pressable = True
    player_turn = True

    win_str = ""
    new_mark = None

    # Draw Initial Screen
    draw(SCREEN, highlighted, Xs, Os, None, None, None)
    pygame.display.update()

    # Main Game Loop
    while running:
        # Get delta time
        clock.tick(FPS)
        dt = clock.get_time()

        new_mark = None
        # Get Keyboard Inputs
        if player_turn:
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
            elif keys[pygame.K_SPACE] and pressable:
                new_mark = highlighted
                player_turn = False
                pressable = False
            else:
                pressable = True

            if new_mark in Xs or new_mark in Os:
                win_str = "Duplicate mark."
                O_score += 1
            else:
                if new_mark:
                    Xs.add(new_mark)
                if x_winner(Xs):
                    win_str = "X wins!"
                    X_score += 1
            new_mark = None

        elif len(Xs) + len(Os) == 9:
            win_str = "Cat's Game"

        elif not player_turn and win_str == "":
            new_mark = computer_move(Xs, Os)
            
            if new_mark in Os or new_mark in Xs:
                win_str = "Duplicate mark."
                X_score += 1
            else:
                Os.add(new_mark)
                if o_winner(Os):
                    win_str = "O wins"
                    O_score += 1
            player_turn = True
        

        # Break main loop on quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Render Scores
        x_score_lbl = main_font.render(str(X_score), 1, (171, 108, 77))
        o_score_lbl = main_font.render(str(O_score), 1, (171, 108, 77))
        win_str_lbl = main_font.render(str(win_str), 1, (171, 108, 77))
        draw(SCREEN, highlighted, Xs, Os, x_score_lbl, o_score_lbl, win_str_lbl)
        
        keys = None

        pygame.display.update()

        # Pause on win
        if  win_str != "":
            Xs = set()
            Os = set()
            win_str = ""
            player_turn = True
            pygame.time.delay(1000)