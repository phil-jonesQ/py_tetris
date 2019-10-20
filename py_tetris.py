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
tetris_surface = pygame.display.set_mode((WindowWidth, WindowHeight))
clock = pygame.time.Clock()
MY_VERSION = "1.0"
top_left_x = (WindowWidth - play_width) // 2
top_left_y = WindowHeight - play_height - 80
scale = 90
offset = 45
start_x = WindowWidth / 2 - scale
start_y = WindowHeight / 2 - scale - offset


L = ['......',
     '..X...',
     '..X...',
     '..XX..'
     '......',
     '......']

O = ['......',
     '..XX..',
     '..XX..',
     '......',
     '......',
     '......']

Z = ['......',
     '..X...',
     '..XX..',
     '...X..',
     '......',
     '......']

T = ['......',
     '..X...',
     '..XX..',
     '..X...',
     '......',
     '......']

I = ['......',
     '..X...',
     '..X...',
     '..X...',
     '..X...',
     '......']

S = ['......',
     '...X..',
     '..XX..',
     '..X...',
     '......',
     '......']

piece = [L, O, Z, T, I, S]


def reset_game():
    global frame_rate, game_over, tetris_lines, level
    tetris_lines = 0
    game_over = False
    frame_rate = 1
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

def draw_piece(surface, select, x, y, start):
    if start:
        sx = top_left_x
        sy = top_left_y
    else:
        sx = x
        sy = y
    for i in (range(5)):
        for j in (range(5)):
            if piece[select][j][i] == "X":
                pygame.draw.rect(surface, BLUE, (sx + i * scale / 3, sy + j * scale / 3, scale / 3 - 2, scale / 3 - 2))
    # Update the screen
    pygame.display.flip()

def update_play_field(surface, font, font2):
    # Update screen
    tetris_surface.fill(BLACK)
    # Redraw Grid
    play_field_grid(10, 20, tetris_surface)
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

def main():
    reset_game()
    loop = True
    # Declare Global Vars
    pygame.init()
    pygame.display.set_caption("Tetris " + MY_VERSION)

    # Initialise fonts we will use
    font = pygame.font.SysFont('Arial', 50, False, False)
    font2 = pygame.font.SysFont('Arial', 25, False, False)
    count = 0

    # Initialise the display
    x = start_x
    y = start_y
    update_play_field(tetris_surface, font, font2)
    draw_piece(tetris_surface, select_piece(), x, y, False)



    while loop:
        # Control FPS
        clock.tick(frame_rate)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    update_play_field(tetris_surface, font, font2)
                    draw_piece(tetris_surface, select_piece(), x, y, False)

                if event.key == pygame.K_RIGHT:
                        x = x + scale / 3
                        update_play_field(tetris_surface, font, font2)
                        draw_piece(tetris_surface, count, x, y, False)
                if event.key == pygame.K_LEFT:
                        x = x - scale / 3
                        update_play_field(tetris_surface, font, font2)
                        draw_piece(tetris_surface, count, x, y, False)
                if event.key == pygame.K_DOWN:
                        y = y + scale / 3
                        update_play_field(tetris_surface, font, font2)
                        draw_piece(tetris_surface, count, x, y, False)



# Call main
main()
