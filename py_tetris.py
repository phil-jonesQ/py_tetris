""" Version 1.00 - simple version of the tetris game.. The game uses pygame to handle the graphics and is desinged on a grid
Phil Jones September 2019 - phil.jones.24.4@gmail.com
October 28 - Can now control pieces and freeze them, this stores them in the master array as block and colour
This should make collision detection and line detection easier etc
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
scale = 30
offset = 45
start_x = WindowWidth / 2
start_y = WindowHeight / 2 - scale * 11

grid2 = [[(0,0,0) for x in range(10)] for x in range(21)]

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


def reset_game():
    global frame_rate, game_over, tetris_lines, level
    tetris_lines = 0
    game_over = False
    frame_rate = 10
    level = 1


def colour_map(piece):
    if piece == 0:
        colour = BLUE
    if piece == 1:
        colour = GREEN
    if piece == 2:
        colour = RED
    if piece == 3:
        colour = WHITE
    if piece == 4:
        colour = YELLOW
    if piece == 5:
        colour = MAGENTA
    return colour


def draw_piece(surface, select, x, y, start, rotater):
    colour = colour_map(select)

    print(rotater)

    if start:
        sx = start_x
        sy = start_y
    else:
        sx = x
        sy = y


    if rotater == 1:
        for i in (range(4)):
            for j in (range(4)):
                if piece[select][j][i] == "X":
                    pygame.draw.rect(surface, colour, (sx + i * scale, sy + j * scale, scale - 2, scale - 2))

    if rotater == 2:
        for i in (range(4)):
            for j in (range(4)):
                if piece[select][i][j] == "X":
                    pygame.draw.rect(surface, colour, (sx + i * scale, sy + j * scale, scale - 2, scale - 2))

    if rotater == 3:
        for i in (range(3,-1,-1)):
            for j in (range(3, -1, -1)):
                print(i,j)
                if piece[select][i][j] == "X":
                    pygame.draw.rect(surface, colour, (sx + i * scale, sy + j * scale, scale - 2, scale - 2))

    # Update the screen
    pygame.display.flip()


def update_play_field(surface, font, font2):
    # Update screen
    tetris_surface.fill(BLACK)

    # Draw historic pieces and grid space
    row = 20
    col = 10
    for i in (range(row)):
        for j in (range(col)):
            if grid2[i][j] != (0, 0, 0):
                sx = ((start_x - (5 * scale)) + (j * scale))
                sy = (start_y + (i * scale))
                pygame.draw.rect(surface, grid2[i][j], (sx, sy, scale - 2, scale - 2))
            else:
                sx = ((start_x - (5 * scale)) + (j * scale))
                sy = (start_y + (i * scale))
                pygame.draw.rect(surface, GREY, (sx, sy, scale - 2, scale - 2))

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
    piece_select = random.randrange(0, 6)
    #piece_select = 1
    return piece_select


def check_line():
    row = 20
    col = 10
    for i in (range(row)):
        for j in (range(col)):
            if grid2[i][j] != (0, 0, 0):
                hit_count = 0
                for b in (range(10)):
                    if grid2[i][b] != (0, 0, 0):
                        hit_count += 1
                if hit_count == 10:
                    print ("Calling remove row on " + str(i))
                    remove_line(i)


def remove_line(remove_row):
    col = 10
    ## Clear row
    for j in (range(col)):
        grid2[remove_row][j] = (0, 0, 0)
    row = 4
    col = 10
    ## Move all blocks down if space if free
    for i in (range(row)):
        for j in (range(col)):
                if grid2[remove_row - i][j] != (0, 0, 0):
                    grid2[remove_row][j] = grid2[remove_row - i][j]
                    grid2[remove_row - i][j] = (0, 0, 0)


def freeze_piece(current_piece, x, y):
    # Convert the x / y to row col
    col = int(((x - start_x) // scale) + 5)
    row = int(((y - start_y) // scale))
    # Freeze the piece in the master grid array recording it's colour
    for i in (range(4)):
        for j in (range(4)):
            if piece[current_piece][i][j] == "X":
                grid2[row + i][col + j] = (colour_map(current_piece))

def does_piece_fit2(current_piece, x, y):
    # Convert the x / y to row col
    global bound, next_piece
    overlap = False
    row = 20
    col = 10

    # Piece boundary and hit floor
    for i in (range(4)):
        for j in (range(4)):
            if piece[current_piece][i][j] == "X":
                # print("In check " + str(i), str(j))
                current_col = int(((x) // scale) - 8) + j
                current_row = int(((y) // scale)) + i
                # Handle the first piece
                if current_row == 19:
                    next_piece = True
                if current_col == 0:
                    # print ("Edge")
                    bound = "L"
                if current_col == 9:
                    # print ("Edge")
                    bound = "R"
    # Detect piece can fit
    for r in (range(row)):
        for c in (range(col)):
            if grid2[r][c] != (0, 0, 0):
                for i in (range(4)):
                    for j in (range(4)):
                        if piece[current_piece][i][j] == "X":
                            current_col = int(((x) // scale) - 8) + j
                            current_row = int(((y) // scale)) + i
                            #print("In check " + str(i), str(j))
                            if r == current_row and c == current_col:
                                #print (r, c, current_row, current_col)
                                overlap = True
                                next_piece = True
                            else:
                                overlap = False


    #print ("End check")
    if overlap is True or bound == "R" or bound == "L":
        return False
    else:
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
    x = start_x - scale * 2
    y = start_y - scale * 2
    current_piece = select_piece()
    update_play_field(tetris_surface, font, font2)
    draw_piece(tetris_surface, current_piece, x, y, False, 1)

    global bound, next_piece, fall
    bound = "N"
    next_piece = False
    fall = True
    rotate = 1

    while loop:
        # Control FPS
        clock.tick(frame_rate)

        # Spawn next piece
        if next_piece:
            next_piece = False
            rotate = 1
            freeze_piece(current_piece, x, y)
            current_piece = select_piece()
            x = start_x
            y = start_y - scale * 2
            draw_piece(tetris_surface, current_piece, x, y, False, rotate)

        # Update the display
        update_play_field(tetris_surface, font, font2)
        draw_piece(tetris_surface, current_piece, x, y, False, rotate)

        # Make piece fall
        if fall:
            if does_piece_fit2(current_piece, x, y) or bound == "N" or bound == "R" or bound == "L" or fall:
                y = y + scale

        # Check for a line

        check_line()

        # Check if lost

        # Check if piece fits
        does_piece_fit2(current_piece, x, y)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    next_piece = False
                    freeze_piece(current_piece, x, y)
                    current_piece = select_piece()
                    x = start_x
                    y = start_y - scale * 2
                    draw_piece(tetris_surface, current_piece, x, y, False, rotate)
                    #print(grid)

                if event.key == pygame.K_RIGHT:
                        #x = x + scale
                    if does_piece_fit2(current_piece, x, y) or bound != "R":
                        bound = "N"
                        x = x + scale
                    #update_play_field(tetris_surface, font, font2)
                    #draw_piece(tetris_surface, current_piece, x, y, False, rotate)
                if event.key == pygame.K_LEFT:
                    #x = x - scale
                    if does_piece_fit2(current_piece, x, y) or bound != "L":
                        bound = "N"
                        x = x - scale
                    #does_piece_fit(current_piece, x, y)
                    #update_play_field(tetris_surface, font, font2)
                    #draw_piece(tetris_surface, current_piece, x, y, False, rotate)
                if event.key == pygame.K_DOWN:
                    #y = y + scale
                    if does_piece_fit2(current_piece, x, y) or bound == "N" or bound == "R" or bound == "L" or fall:
                        y = y + scale
                    #update_play_field(tetris_surface, font, font2)
                    #draw_piece(tetris_surface, current_piece, x, y, False, rotate)
                if event.key == pygame.K_UP:
                    #y = y - scale
                    #if does_piece_fit2(current_piece, x, y):
                    #    y = y - scale
                    rotate += 1
                    if rotate > 3:
                        rotate = 1
                    #update_play_field(tetris_surface, font, font2)
                    #draw_piece(tetris_surface, current_piece, x, y, False, rotate)




# Call main
main()
