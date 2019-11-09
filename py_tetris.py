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
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
tetris_surface = pygame.display.set_mode((WindowWidth, WindowHeight))
clock = pygame.time.Clock()
MY_VERSION = "1.0"
top_left_x = (WindowWidth - play_width) // 2
top_left_y = WindowHeight - play_height - 80
scale = 30
offset = 45
start_x = WindowWidth / 2
start_y = WindowHeight / 2 - scale * 11

grid2 = [[(0, 0, 0) for x in range(10)] for x in range(21)]

L = ['....',
     '.X..',
     '.X..',
     '.XX.']
L1 = ['....',
      'XXX.',
      'X...',
      '....']
L2 = ['....',
      '.XX.',
      '..X.',
      '..X.']
L3 = ['....',
      '...X',
      '.XXX',
      '....']

J = ['..X.',
     '..X.',
     '.XX.',
     '....']
J1 = ['....',
      'X...',
      'XXX.',
      '....']
J2 = ['....',
      '.XX.',
      '.X..',
      '.X..']
J3 = ['....',
      '.XXX',
      '...X',
      '....']

O = ['....',
     '.XX.',
     '.XX.',
     '....']
O1 = ['....',
      '.XX.',
      '.XX.',
      '....']
O2 = ['....',
      '.XX.',
      '.XX.',
      '....']
O3 = ['....',
      '.XX.',
      '.XX.',
      '....']

T = ['....',
     '.X..',
     '.XX.',
     '.X..']
T1 = ['....',
      '.XXX',
      '..X.',
      '....']
T2 = ['...X',
      '..XX',
      '...X',
      '....']
T3 = ['....',
      '..X.',
      '.XXX',
      '....']

I = ['.X..',
     '.X..',
     '.X..',
     '.X..']
I1 = ['....',
      'XXXX',
      '....',
      '....']
I2 = ['.X..',
      '.X..',
      '.X..',
      '.X..']
I3 = ['....',
      'XXXX',
      '....',
      '....']

S = ['....',
     '..X.',
     '.XX.',
     '.X..']
S1 = ['....',
      '..XX',
      '.XX.',
      '....']
S2 = ['....',
      '..X.',
      '.XX.',
      '.X..']
S3 = ['....',
      '..XX',
      '.XX.',
      '....']

Z = ['....',
     '.X..',
     '.XX.',
     '..X.']
Z1 = ['....',
      '.XX.',
      '..XX',
      '....']
Z2 = ['....',
      '.X..',
      '.XX.',
      '..X.']
Z3 = ['....',
      '.XX.',
      '..XX',
      '....']


piece = [L, J, O, Z, T, I, S]
piece1 = [L1, J1, O1, Z1, T1, I1, S1]
piece2 = [L2, J2, O2, Z2, T2, I2, S2]
piece3 = [L3, J3, O3, Z3, T3, I3, S3]


def reset_game():
    global frame_rate, game_over, tetris_lines, level
    tetris_lines = 0
    game_over = False
    frame_rate = 5
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
    if piece == 6:
        colour = ORANGE
    return colour


def draw_piece(surface, select, x, y, start, rotater):
    colour = colour_map(select)

    #print(rotater)

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
                if piece1[select][j][i] == "X":
                    pygame.draw.rect(surface, colour, (sx + i * scale, sy + j * scale, scale - 2, scale - 2))

    if rotater == 3:
        for i in (range(4)):
            for j in (range(4)):
                if piece2[select][j][i] == "X":
                    pygame.draw.rect(surface, colour, (sx + i * scale, sy + j * scale, scale - 2, scale - 2))

    if rotater == 4:
        for i in (range(4)):
            for j in (range(4)):
                if piece3[select][j][i] == "X":
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
    piece_select = random.randrange(0, 7)
    #piece_select = 6
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
    row = 8
    col = 10
    ## Move all blocks down if space if free
    for i in (range(row)):
        for j in (range(col)):
            if grid2[remove_row - i][j] != (0, 0, 0):
                grid2[remove_row][j] = grid2[remove_row - i][j]
                grid2[remove_row - i][j] = (0, 0, 0)


def freeze_piece(current_piece, x, y, rotater):
    #print (rotater)
    # Convert the x / y to row col
    col = int(((x - start_x) // scale) + 5)
    row = int(((y - start_y) // scale))
    # Freeze the piece in the master grid array recording it's colour
    if rotater == 1:
        for i in (range(4)):
            for j in (range(4)):
                if piece[current_piece][i][j] == "X":
                    grid2[row + i][col + j] = (colour_map(current_piece))
    if rotater == 2:
        for i in (range(4)):
            for j in (range(4)):
                if piece1[current_piece][i][j] == "X":
                    grid2[row + i][col + j] = (colour_map(current_piece))
    if rotater == 3:
        for i in (range(4)):
            for j in (range(4)):
                if piece2[current_piece][i][j] == "X":
                    grid2[row + i][col + j] = (colour_map(current_piece))
    if rotater == 4:
        for i in (range(4)):
            for j in (range(4)):
                if piece3[current_piece][i][j] == "X":
                    grid2[row + i][col + j] = (colour_map(current_piece))


def does_piece_fit2(current_piece, x, y, rotater):
    # Convert the x / y to row col
    global bound, next_piece
    overlap = False
    row = 20
    col = 10

    # Piece boundary and hit floor
    for i in (range(4)):
        for j in (range(4)):
            if rotater == 1:
                if piece[current_piece][i][j] == "X":
                    # print("In check " + str(i), str(j))
                    current_col = int(((x) // scale) - 8) + j
                    current_row = int(((y) // scale)) + i
                    # Handle the first piece
                    print (current_col)
                    if current_row == 20:
                        next_piece = True
                    if current_col == -2:
                        return False
                    if current_col == 11:
                        return False
            if rotater == 2:
                if piece1[current_piece][i][j] == "X":
                    # print("In check " + str(i), str(j))
                    current_col = int(((x) // scale) - 8) + j
                    current_row = int(((y) // scale)) + i
                    if current_row == 20:
                        next_piece = True
                    if current_col == -2:
                        return False
                    if current_col == 11:
                        return False
            if rotater == 3:
                if piece2[current_piece][i][j] == "X":
                    # print("In check " + str(i), str(j))
                    current_col = int(((x) // scale) - 8) + j
                    current_row = int(((y) // scale)) + i
                    if current_row == 20:
                        next_piece = True
                    if current_col == -2:
                        return False
                    if current_col == 11:
                        return False
            if rotater == 4:
                if piece3[current_piece][i][j] == "X":
                    # print("In check " + str(i), str(j))
                    current_col = int(((x) // scale) - 8) + j
                    current_row = int(((y) // scale)) + i
                    if current_row == 20:
                        next_piece = True
                    if current_col == -2:
                        return False
                    if current_col == 11:
                        return False
    # Detect piece can fit
    for r in (range(row)):
        for c in (range(col)):
            if grid2[r][c] != (0, 0, 0):
                for i in (range(4)):
                    for j in (range(4)):
                        if rotater == 1:
                            if piece[current_piece][i][j] == "X":
                                current_col = int(((x) // scale) - 8) + j
                                current_row = int(((y) // scale)) + i
                                #print("Checking background piece (r, c) " + str(r), str(c) + "Against The Falling " + str(current_row), str(current_col))
                                if r == current_row and c == current_col:
                                    #print (r, c, current_row, current_col)
                                    overlap = True
                                    next_piece = True
                                else:
                                    overlap = False
                        if rotater == 2:
                            if piece1[current_piece][i][j] == "X":
                                current_col = int(((x) // scale) - 8) + j
                                current_row = int(((y) // scale)) + i
                                # print("In check " + str(i), str(j))
                                if r == current_row and c == current_col:
                                    # print (r, c, current_row, current_col)
                                    overlap = True
                                    next_piece = True
                                else:
                                    overlap = False
                        if rotater == 3:
                            if piece2[current_piece][i][j] == "X":
                                current_col = int(((x) // scale) - 8) + j
                                current_row = int(((y) // scale)) + i
                                # print("In check " + str(i), str(j))
                                if r == current_row and c == current_col:
                                    # print (r, c, current_row, current_col)
                                    overlap = True
                                    next_piece = True
                                else:
                                    overlap = False

                        if rotater == 4:
                            if piece3[current_piece][i][j] == "X":
                                current_col = int(((x) // scale) - 8) + j
                                current_row = int(((y) // scale)) + i
                                # print("In check " + str(i), str(j))
                                if r == current_row and c == current_col:
                                    # print (r, c, current_row, current_col)
                                    overlap = True
                                    next_piece = True
                                else:
                                    overlap = False



    #print ("End check")
    if overlap is True:
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
    fall_time = 0
    fall_speed = 0.27
    level_time = 0

    #pygame.key.set_repeat(100, 10)  # use 10 as interval to speed things up.
    while loop:
        # Control FPS
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        # Control fall rate
        if level_time / 1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005


        # Spawn next piece
        if next_piece:
            next_piece = False
            freeze_piece(current_piece, x, y, rotate)
            current_piece = select_piece()
            rotate = 1
            x = start_x
            y = start_y - scale * 2
            draw_piece(tetris_surface, current_piece, x, y, False, rotate)

        # Update the display
        update_play_field(tetris_surface, font, font2)
        draw_piece(tetris_surface, current_piece, x, y, False, rotate)

        # Make piece fall
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            if fall:
                if does_piece_fit2(current_piece, x, y + scale * 2, rotate):
                    y = y + scale

        # Check for a line
        check_line()

        # Check if lost

        # Check if piece fits
        does_piece_fit2(current_piece, x, y, rotate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_SPACE:
                    next_piece = False
                    freeze_piece(current_piece, x, y, rotate)
                    current_piece = select_piece()
                    x = start_x
                    y = start_y - scale * 2
                    draw_piece(tetris_surface, current_piece, x, y, False, rotate)

                if event.key == pygame.K_RIGHT:
                    if does_piece_fit2(current_piece, x + scale * 2, y, rotate):
                        x = x + scale
                if event.key == pygame.K_LEFT:
                    if does_piece_fit2(current_piece, x - scale * 2, y, rotate):
                        x = x - scale
                if event.key == pygame.K_DOWN:
                    if does_piece_fit2(current_piece, x, y + scale * 2, rotate):
                        y = y + scale
                if event.key == pygame.K_UP:
                    if x > 220 and x < 460:
                        rotate += 1
                        if rotate > 4:
                            rotate = 1


# Call main
main()
