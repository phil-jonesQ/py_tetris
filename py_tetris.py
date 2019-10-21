""" Version 1.00 - simple version of the tetris game.. The game uses pygame to handle the graphics and is desinged on a grid
Phil Jones September 2019 - phil.jones.24.4@gmail.com
"""

import pygame
import random

# Constants

WindowWidth = 800
WindowHeight = 700
play_width = 300
play_height = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (101, 152, 101)
GREY = (128, 128, 128)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
tetris_surface = pygame.display.set_mode((WindowWidth, WindowHeight))
clock = pygame.time.Clock()
MY_VERSION = "1.0"
top_left_x = (WindowWidth - play_width) // 2
top_left_y = WindowHeight - play_height - 80
scale = 90
offset = 45
start_x = WindowWidth / 2 - scale
start_y = WindowHeight / 2 - scale * 4

grid = ['O..........O',
        'O..........O'
        'O..........O',
        'O..........O',
        'O..........O',
        'O..........O',
        'O..........O',
        'O..........O',
        'O..........O',
        'O.....X....O',
        'O.....X....O',
        'O.....X....O',
        'O.....X....O',
        'O..........O',
        'O..........O',
        'O..........O',
        'O..........O',
        'O..........O',
        'O..........O',
        'O..........O',
        'O..........O',
        'OOOOOOOOOOOO']

L = ['....',
     '.X..',
     '.X..',
     '.XX.']

O = ['....',
     '.XX.',
     '.XX.',
     '....']

Z = ['....',
     '.X..',
     '.XX.',
     '..X.']

T = ['....',
     '.X..',
     '.XX.',
     '.X..']

I =  ['.X..',
      '.X..',
      '.X..',
      '.X..']

S = ['....',
     '..X.',
     '.XX.',
     '.X..']

piece = [L, O, Z, T, I, S]

piece_store = {}


def reset_game():
    global frame_rate, game_over, tetris_lines, level
    tetris_lines = 0
    game_over = False
    frame_rate = 120
    level = 1


def play_field_grid(col, row, surface):
    sx = top_left_x
    sy = top_left_y
    for i in range(row + 1):
        pygame.draw.line(surface, (RED), (sx, sy + i * 30),
                         (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col + 1):
            pygame.draw.line(surface, (RED), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))  # vertical lines

def play_field_grid2(row, col, surface):
    sx = top_left_x
    sy = top_left_y
    for i in (range(col)):
        for j in (range(row)):
            if grid[j][i] == ".":
                pygame.draw.rect(surface, GREY,
                                 (sx + i * scale / 3, sy + j * scale / 3, scale / 3 - 2, scale / 3 - 2))
            if grid[j][i] == "X":
                pygame.draw.rect(surface, BLACK,
                                 (sx + i * scale / 3, sy + j * scale / 3, scale / 3 - 2, scale / 3 - 2))



def draw_piece(surface, select, x, y, start, rotate):
    # Colour map switch

    if select == 0:
        colour = BLUE
    if select == 1:
        colour = GREEN
    if select == 2:
        colour = RED
    if select == 3:
        colour = WHITE
    if select == 4:
        colour = YELLOW
    if select == 5:
        colour = MAGENTA

    if start:
        sx = start_x
        sy = start_y
    else:
        sx = x
        sy = y
    if rotate:
        for i in (range(4)):
            for j in (range(4)):
                if piece[select][i][j] == "X":
                    pygame.draw.rect(surface, colour, (sx + i * scale / 3, sy + j * scale / 3, scale / 3 - 2, scale / 3 - 2))
    else:
        for i in (range(4)):
            for j in (range(4)):
                if piece[select][j][i] == "X":
                    pygame.draw.rect(surface, colour, (sx + i * scale / 3, sy + j * scale / 3, scale / 3 - 2, scale / 3 - 2))
    # Update the screen
    pygame.display.flip()

def update_play_field(surface, font, font2):
    # Update screen
    tetris_surface.fill(BLACK)
    # Redraw Grid
    play_field_grid2(20, 10, tetris_surface)

    # Draw historic pieces
    for piece in piece_store:
        draw_piece(surface, piece_store[piece], piece[0], piece[1], False, False)

    # Update Display for user
    text = font.render("SCORE " + str(tetris_lines), True, WHITE)
    text2 = font.render("LEVEL " + str(level), True, WHITE)
    if game_over:
        text = font.render("SCORE " + str(tetris_lines), True, WHITE)
        text2 = font.render("LEVEL " + str(level), True, WHITE)
        text_game_over = font2.render("GAME OVER!!! SPACE TO RESTART..", True, RED)
        tetris_surface.blit(text_game_over, [80, WindowHeight - 400])
    pygame.draw.line(tetris_surface, WHITE, (0, WindowHeight - 65), (WindowWidth, WindowHeight - 65))
    tetris_surface.blit(text, [20, WindowHeight - 60])
    tetris_surface.blit(text2, [WindowWidth - 190, WindowHeight - 60])
    # Update the screen
    pygame.display.flip()


def select_piece():
    piece_select = random.randrange(0, 5)
    return piece_select


def freeze_piece(current_piece, x, y):
    d = {(x, y): current_piece}
    piece_store.update(dict(d))  # update it

def piece_occupied(current_piece, x, y):
    for piece in piece_store:
        if piece[0] == x and piece[1] == y:
            return True


def main():
    reset_game()
    loop = True
    # Declare Global Vars
    pygame.init()
    pygame.display.set_caption("Tetris " + MY_VERSION)

    # Initialise fonts we will use
    font = pygame.font.SysFont('Arial', 50, False, False)
    font2 = pygame.font.SysFont('Arial', 25, False, False)
    rotate = False

    # Initialise the display
    x = start_x
    y = start_y
    current_piece = select_piece()
    update_play_field(tetris_surface, font, font2)
    draw_piece(tetris_surface, current_piece, x, y, False, False)



    while loop:
        # Control FPS
        clock.tick(frame_rate)

        # Check if piece is occupied

        if piece_occupied(current_piece, x, y):
            print ("Overlapping!!")

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    freeze_piece(current_piece, x, y)
                    #print(piece_store)
                    update_play_field(tetris_surface, font, font2)
                    current_piece = select_piece()
                    x = start_x
                    y = start_y
                    draw_piece(tetris_surface, current_piece, x, y, True, rotate)

                if event.key == pygame.K_RIGHT:
                    x = x + scale / 3
                    update_play_field(tetris_surface, font, font2)
                    draw_piece(tetris_surface, current_piece, x, y, False, rotate)
                if event.key == pygame.K_LEFT:
                    x = x - scale / 3
                    update_play_field(tetris_surface, font, font2)
                    draw_piece(tetris_surface, current_piece, x, y, False, rotate)
                if event.key == pygame.K_DOWN:
                    y = y + scale / 3
                    update_play_field(tetris_surface, font, font2)
                    draw_piece(tetris_surface, current_piece, x, y, False, rotate)
                if event.key == pygame.K_UP:
                    rotate = True


# Call main
main()
