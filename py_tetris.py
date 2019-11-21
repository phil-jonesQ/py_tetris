""" Version 1.00 - simple version of the tetris game.. The game uses pygame to handle the graphics and is desinged on a grid
Phil Jones September 2019 - phil.jones.24.4@gmail.com
October 28 - Can now control pieces and freeze them, this stores them in the master array as block and colour
This should make collision detection and line detection easier etc
V1.01 November 11 2019
Working version of the game - to do
* Next piece preview - V1.02
* Detect when die - v1.03
* Start splash screen
* Game over splash screen - V1.04
* Improve random number generator algorithm - V1.05
* Fire piece down - V1.08
* Increase speed with level - V.1.11
* Fix rotational collision detection and add sounds - V1.06
* Fix Tetromino colours - V1.07
* Add Music with on / off control - V1.09
* Add pause feature - V1.09
* Add High Score System ((harder than I thought)) - V1.10
"""

import pygame
import random
import json
from operator import itemgetter

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
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
tetris_surface = pygame.display.set_mode((WindowWidth, WindowHeight))
clock = pygame.time.Clock()
MY_VERSION = "1.11"
top_left_x = (WindowWidth - play_width) // 2
top_left_y = WindowHeight - play_height - 80
scale = 30
offset = 45
start_x = WindowWidth / 2
start_y = WindowHeight / 2 - scale * 11

# Load Sound effects
pygame.mixer.init()
freeze_piece_sound = pygame.mixer.Sound("game_assets/freeze.wav")
got_line_sound = pygame.mixer.Sound("game_assets/got_line.wav")
bg_music = pygame.mixer.music.load("game_assets/Tetris.mp3")

# High Score Letter Lists
abc0 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
abc1 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
abc2 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


# Load Up High Score Data
def load():
    try:
        with open('high_score.json', 'r') as file:
            highscores = json.load(file)  # Read the json file.
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist.
    # Sorted by the score.
    return sorted(highscores, key=itemgetter(1), reverse=True)


# Function to save high score data

def save(highscores):
    with open('high_score.json', 'w') as file:
        json.dump(highscores, file)  # Write the list to the json file.

# Define multi dimensional array assets
# All rotations defined
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

# Define each asset group as a piece array
piece = [L, J, O, Z, T, I, S]
piece1 = [L1, J1, O1, Z1, T1, I1, S1]
piece2 = [L2, J2, O2, Z2, T2, I2, S2]
piece3 = [L3, J3, O3, Z3, T3, I3, S3]


# Function to reset all of the games variables
def reset_game():
    global frame_rate, game_over, tetris_lines, level, next_piece, fall, grid2, piece_sequence, next_piece_index,\
        letter_index0, letter_index1, letter_index2, col_index, done, active, highscores, fall_speed
    # Generate the initial random sequence of 17
    piece_sequence = generate_sequence()
    next_piece_index = 0
    # The main game play area grid - pieces are frozen into this when they have settled
    grid2 = [[(0, 0, 0) for x in range(10)] for x in range(21)]
    tetris_lines = 0
    game_over = False
    frame_rate = 5
    level = 1
    next_piece = False
    fall = True
    fall_speed = 0.37
    play_music(False)
    play_music(True)
    letter_index0 = 0
    letter_index1 = 0
    letter_index2 = 0
    col_index = 0
    done = False
    active = True
    highscores = load()


# Simple switch to map the level to fall rate
def map_speed_to_level(level_on):
    level_fall_rate = 1200
    if level_on > 2:
        level_fall_rate = 1100
    if level_on > 3:
        level_fall_rate = 1000
    if level_on > 4:
        level_fall_rate = 900
    if level_on > 5:
        level_fall_rate = 800
    if level_on > 6:
        level_fall_rate = 700
    if level_on > 7:
        level_fall_rate = 600
    if level_on > 8:
        level_fall_rate = 500
    if level_on > 9:
        level_fall_rate = 400
    if level_on > 10:
        level_fall_rate = 350
    return level_fall_rate


# Simple switch to map the level to how many lines you've got
def score_to_level_map(tetris_lines):
    global level
    if tetris_lines > 3:
        level = 2
    if tetris_lines > 6:
        level = 3
    if tetris_lines > 9:
        level = 4
    if tetris_lines > 12:
        level = 5
    if tetris_lines > 15:
        level = 6
    if tetris_lines > 18:
        level = 7
    if tetris_lines > 21:
        level = 8
    if tetris_lines > 25:
        level = 9
    if tetris_lines > 30:
        level = 10
    return level


# Map the pieces to colours
def colour_map(piece):
    if piece == 0:
        colour = BLUE
    if piece == 1:
        colour = ORANGE
    if piece == 2:
        colour = YELLOW
    if piece == 3:
        colour = RED
    if piece == 4:
        colour = PURPLE
    if piece == 5:
        colour = CYAN
    if piece == 6:
        colour = GREEN
    return colour


# Draw our multi dimensional shape to the screen (all 4 rotations)
def draw_piece(surface, select, x, y, start, rotater):
    colour = colour_map(select)

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


# Function to take care of displaying and updating the high score table
def high_score(surface, font, font2):
    global letter_index0, letter_index1, letter_index2, col_index, active, done
    clock.tick(150)
    header = font2.render("HIGH SCORES", True, RED)
    surface.blit(header, [10, 20])
    offset_high = 35
    # Sort the highscores list by score - and only show the top 15
    highscores_sorted = sorted(highscores, key=itemgetter(1), reverse=True)
    for y, (hi_name, hi_score) in enumerate(highscores_sorted):
        if y == 0:
            colour = GREEN
        else:
            colour = WHITE
        if y > 15:
            break
        display_name = str(hi_name)
        display_score = str(hi_score)
        col1 = font2.render(display_name, True, colour)
        col2 = font2.render(display_score, True, colour)
        # Look for the place holder in the high score list, when found edit at this point
        # Note, if you're less than 15th place then you won't make it on there
        if hi_name == "ZZZ_PLACE_HOLDER":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_UP:
                            if col_index == 0:
                                letter_index0 += 1
                            if col_index == 1:
                                letter_index1 += 1
                            if col_index == 2:
                                letter_index2 += 1
                        if event.key == pygame.K_DOWN:
                            if col_index == 0:
                                letter_index0 -= 1
                            if col_index == 1:
                                letter_index1 -= 1
                            if col_index == 2:
                                letter_index2 -= 1
                        if event.key == pygame.K_RIGHT:
                            col_index += 1
                        if event.key == pygame.K_LEFT:
                            col_index -= 1
                        if event.key == pygame.K_SPACE:
                            done = True
            # Wrap around the selections
            if col_index > 2:
                col_index = 0
            if col_index < 0:
                col_index = 2
            if letter_index0 > 25:
                letter_index0 = 0
            if letter_index1 > 25:
                letter_index1 = 0
            if letter_index2 > 25:
                letter_index2 = 0
            if letter_index0 < 0:
                letter_index0 = 25
            if letter_index1 < 0:
                letter_index1 = 25
            if letter_index2 < 0:
                letter_index2 = 25
            # if save has been triggered save the data and make it white
            if done:
                active = False
                colour = WHITE
                hi_name = abc0[letter_index0] + abc1[letter_index1] + abc2[letter_index2]
                col_1 = font2.render(abc0[letter_index0], True, colour)
                col_2 = font2.render(abc1[letter_index1], True, colour)
                col_3 = font2.render(abc2[letter_index2], True, colour)
                #print(highscores)
                #print(hi_name, hi_score)
                highscores.append([hi_name, hi_score])
                for y, (hi_name, hi_score) in enumerate(highscores):
                    if hi_name == "ZZZ_PLACE_HOLDER":
                        del highscores[y]
                save(sorted(highscores, key=itemgetter(1), reverse=True))
                done = False
            else:
                if col_index == 0:
                    colour = RED
                    col_1 = font2.render(abc0[letter_index0], True, colour)
                else:
                    colour = BLUE
                    col_1 = font2.render(abc0[letter_index0], True, colour)
                if col_index == 1:
                    colour = RED
                    col_2 = font2.render(abc1[letter_index1], True, colour)
                else:
                    colour = BLUE
                    col_2 = font2.render(abc1[letter_index1], True, colour)
                if col_index == 2:
                    colour = RED
                    col_3 = font2.render(abc2[letter_index2], True, colour)
                else:
                    colour = BLUE
                    col_3 = font2.render(abc2[letter_index2], True, colour)

            surface.blit(col_1, [offset_high, 55 + y * scale])
            surface.blit(col_2, [offset_high + 15, 55 + y * scale])
            surface.blit(col_3, [offset_high + 30 , 55 + y * scale])
            surface.blit(col2, [offset_high + scale * 3, 55 + y * scale])
        else:
            surface.blit(col1, [offset_high, 55 + y * scale])
            surface.blit(col2, [offset_high + scale * 3, 55 + y * scale])


# Update the Game's play field
def update_play_field(surface, font, font2, next_up):
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

    # Map level
    level = score_to_level_map(tetris_lines)
    # Update Display for user
    text = font.render("SCORE " + str(tetris_lines), True, WHITE)
    text2 = font.render("LEVEL " + str(level), True, WHITE)
    text3 = font.render("NEXT", True, WHITE)
    text4 = font2.render("PAUSE", True, WHITE)
    if game_over:
        text = font.render("SCORE " + str(tetris_lines), True, RED)
        text2 = font.render("LEVEL " + str(level), True, RED)
        text_game_over1 = font2.render("GAME OVER!!", True, RED)
        text_game_over2 = font2.render("R TO RESTART...", True, WHITE)
        tetris_surface.blit(text_game_over1, [WindowWidth / 2 - 90, WindowHeight - scale * 2])
        tetris_surface.blit(text_game_over2, [WindowWidth / 2 - 90, WindowHeight - scale])
        high_score(surface, font, font2)
    if pause:
        tetris_surface.blit(text4, [WindowWidth / 2 - 30, WindowHeight - scale * 2])
    pygame.draw.line(tetris_surface, WHITE, (0, WindowHeight - 65), (WindowWidth, WindowHeight - 65))
    tetris_surface.blit(text, [20, WindowHeight - 60])
    tetris_surface.blit(text2, [WindowWidth - 190, WindowHeight - 60])
    tetris_surface.blit(text3, [WindowWidth - 190, WindowHeight / 2 - 80])
    draw_piece(tetris_surface, next_up, WindowWidth - 200, WindowHeight / 2, False, 1)
    # Update the screen
    pygame.display.flip()


def generate_sequence():
    # generates a list of 17 random numbers
    seq1 = random.sample(range(0, 7), 7)
    seq2 = random.sample(range(0, 7), 7)
    seq3 = random.sample(range(4, 7), 3)
    piece_sequence = seq1 + seq2 + seq3
    return piece_sequence


# Check if lines have been completed
def check_line():
    global tetris_lines
    row = 20
    col = 10
    factor = 1
    lines_to_remove = 0
    for i in (range(row, 1, -1)):
        for j in (range(col)):
            if grid2[i][j] != (0, 0, 0):
                hit_count = 0
                for b in (range(10)):
                    if grid2[i][b] != (0, 0, 0):
                        hit_count += 1
                if hit_count == 10:
                    lines_to_remove += 1
                    factor += 1
                    tetris_lines += 1 * factor
                    remove_line(i)
                    shift_down(i)
                    pygame.mixer.Sound.play(got_line_sound)


# Remove out a row
def remove_line(remove_row):
    col = 10
    visualiser_count = 0
    visualiser = 255
    ## Clear row
    for j in (range(col)):
        # This was supposed to make the line fade out - but doesn't work ## TO DO
        while visualiser_count > 1000:
            visualiser_count += 1
            while visualiser > 0:
                grid2[remove_row][j] = (visualiser, visualiser, visualiser)
                visualiser = visualiser - 1
        grid2[remove_row][j] = (0, 0, 0)


# Shift all pieces down above from the row that has been cleared
def shift_down(remove_row):
    start_row = remove_row
    row = 20
    end_row = 1
    col = 10

    for i in (range(start_row, end_row, -1)):
        for j in (range(col)):
            if grid2[i][j] != (0, 0, 0):
                # print("Moving row " + str(i) + " coloumn " + str(j) + " to row " + str(i + 1) + " column " + str(j))
                grid2[i + 1][j] = grid2[i][j]
                grid2[i][j] = (0, 0, 0)


# Freeze the settled piece into the background preserving it's coordinates and colour
def freeze_piece(current_piece, x, y, rotater):
    pygame.mixer.Sound.play(freeze_piece_sound)
    global game_over, fall, tetris_lines
    # Convert the x / y to row col
    col = int(((x - start_x) // scale) + 5)
    row = int(((y - start_y) // scale))

    # Handle game over
    if row < -1:
        game_over = True
        fall = False
        ## Save score into highscore table as place holder ready to be edited
        highscores.append(["ZZZ_PLACE_HOLDER", tetris_lines])

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


# Collision detection function
def does_piece_fit2(current_piece, x, y, rotater, dir):
    # Convert the x / y to row col
    global next_piece
    row = 20
    col = 10

    # Piece boundary and hit floor
    for i in (range(4)):
        for j in (range(4)):
            if rotater == 1:
                if piece[current_piece][i][j] == "X":
                    # print("In check " + str(i), str(j))
                    current_col = int((x // scale) - 8) + j
                    current_row = int((y // scale)) + i
                    # Handle the first piece
                    if current_row > 19:
                        if not dir:
                            next_piece = True
                            return False
                    if current_col == -1:
                        return False
                    if current_col == 10:
                        return False
            if rotater == 2:
                if piece1[current_piece][i][j] == "X":
                    # print("In check " + str(i), str(j))
                    current_col = int((x // scale) - 8) + j
                    current_row = int((y // scale)) + i
                    if current_row > 19:
                        if not dir:
                            next_piece = True
                            return False
                    if current_col == -1:
                        return False
                    if current_col == 10:
                        return False
            if rotater == 3:
                if piece2[current_piece][i][j] == "X":
                    # print("In check " + str(i), str(j))
                    current_col = int((x // scale) - 8) + j
                    current_row = int((y // scale)) + i
                    if current_row > 19:
                        if not dir:
                            next_piece = True
                            return False
                    if current_col == -1:
                        return False
                    if current_col == 10:
                        return False
            if rotater == 4:
                if piece3[current_piece][i][j] == "X":
                    # print("In check " + str(i), str(j))
                    current_col = int((x // scale) - 8) + j
                    current_row = int((y // scale)) + i
                    if current_row > 19:
                        if not dir:
                            next_piece = True
                            return False
                    if current_col == -1:
                        return False
                    if current_col == 10:
                        return False
    # Detect piece can fit
    for r in (range(row)):
        for c in (range(col)):
            if grid2[r][c] != (0, 0, 0):
                for i in (range(4)):
                    for j in (range(4)):
                        if rotater == 1:
                            if piece[current_piece][i][j] == "X":
                                current_col = int((x // scale) - 8) + j
                                current_row = int((y // scale)) + i
                                #print("Checking background piece (r, c) " + str(r), str(c) + "Against The Falling " + str(current_row), str(current_col))
                                if r == current_row and c == current_col:
                                    if not dir:
                                        next_piece = True
                                    return False

                        if rotater == 2:
                            if piece1[current_piece][i][j] == "X":
                                current_col = int((x // scale) - 8) + j
                                current_row = int((y // scale)) + i
                                # print("In check " + str(i), str(j))
                                if r == current_row and c == current_col:
                                    # print (r, c, current_row, current_col)
                                    if not dir:
                                        next_piece = True
                                    return False

                        if rotater == 3:
                            if piece2[current_piece][i][j] == "X":
                                current_col = int((x // scale) - 8) + j
                                current_row = int((y // scale)) + i
                                # print("In check " + str(i), str(j))
                                if r == current_row and c == current_col:
                                    # print (r, c, current_row, current_col)
                                    if not dir:
                                        next_piece = True
                                    return False

                        if rotater == 4:
                            if piece3[current_piece][i][j] == "X":
                                current_col = int((x // scale) - 8) + j
                                current_row = int((y // scale)) + i
                                # print("In check " + str(i), str(j))
                                if r == current_row and c == current_col:
                                    # print (r, c, current_row, current_col)
                                    if not dir:
                                        next_piece = True
                                    return False

    return True


def play_music(control):
    if control:
        pygame.mixer.music.play(loops = -1)
    else:
        pygame.mixer.music.stop()


def paused():
    global pause
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p] and pause:
                pause = False


def main():

    # Declare Global Vars
    global next_piece, fall, game_over, piece_sequence, next_piece_index, music, pause, letter_index, col_index

    # Call reset of main variables
    reset_game()
    loop = True

    # Local vars
    directional = False
    rotate = 1
    fall_time = 0
    level_time = 0
    music = True
    pause = False

    # Pygame stuff
    pygame.init()
    pygame.display.set_caption("Tetris " + MY_VERSION)

    # Initialise fonts we will use
    font = pygame.font.SysFont('Arial', 50, False, False)
    font2 = pygame.font.SysFont('Arial', 25, False, False)

    # Initialise the display
    x = start_x - scale * 2
    y = start_y - scale * 2
    current_piece = piece_sequence[next_piece_index]
    next_up = piece_sequence[next_piece_index + 1]

    update_play_field(tetris_surface, font, font2, next_up)
    draw_piece(tetris_surface, current_piece, x, y, False, 1)

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
        if next_piece and not game_over:
            # Set the next piece flag to false
            next_piece = False

            # Freeze current piece
            freeze_piece(current_piece, x, y, rotate)

            # Handle the random sequence index and reset back to 0 after sequence 15 and generate a new batch of numbers
            next_piece_index += 1
            if next_piece_index > 15:
                next_piece_index = 0
                # Store the old sequence before generating a new one
                piece_sequence_old = piece_sequence
                piece_sequence = generate_sequence()
                # start on the 2nd number of new seq so we can..
                next_up = piece_sequence[next_piece_index + 1]
                # recall back the last number in previous seq
                current_piece = piece_sequence_old[16]
            else:
                next_up = piece_sequence[next_piece_index + 1]
                current_piece = piece_sequence[next_piece_index]

            rotate = 1
            x = start_x
            y = start_y - scale * 2

        # Update the display
        update_play_field(tetris_surface, font, font2, next_up)
        draw_piece(tetris_surface, current_piece, x, y, False, rotate)

        # Make piece fall
        if fall_time / map_speed_to_level(level) > fall_speed:
            fall_time = 0
            if fall:
                directional = False
                if does_piece_fit2(current_piece, x, y + scale, rotate, directional):
                    y = y + scale

        # Check for a line
        check_line()

        # Check if piece fits
        does_piece_fit2(current_piece, x, y, rotate, directional)

        # Check if we've been paused
        if pause:
            paused()

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    directional = False
                    if does_piece_fit2(current_piece, x, y + scale, rotate, directional):
                        while does_piece_fit2(current_piece, x, y + scale, rotate, directional):
                            y = y + scale

                if event.key == pygame.K_RIGHT and not game_over:
                    directional = True
                    if does_piece_fit2(current_piece, x + scale, y, rotate, directional):
                        x = x + scale
                if event.key == pygame.K_LEFT and not game_over:
                    directional = True
                    if does_piece_fit2(current_piece, x - scale, y, rotate, directional):
                        x = x - scale
                if event.key == pygame.K_DOWN and not game_over:
                    directional = False
                    if does_piece_fit2(current_piece, x, y + scale, rotate, directional):
                        y = y + scale
                if event.key == pygame.K_UP and not game_over:
                    # Check the rotation will be valid
                    if does_piece_fit2(current_piece, x, y, 1, False) and\
                        does_piece_fit2(current_piece, x, y, 1, True) and\
                        does_piece_fit2(current_piece, x, y, 1, True) and\
                        does_piece_fit2(current_piece, x, y, 2, False) and\
                        does_piece_fit2(current_piece, x, y, 2, True) and\
                        does_piece_fit2(current_piece, x, y, 2, True) and\
                        does_piece_fit2(current_piece, x, y, 3, False) and\
                        does_piece_fit2(current_piece, x, y, 3, True) and\
                        does_piece_fit2(current_piece, x, y, 3, True) and\
                        does_piece_fit2(current_piece, x, y, 4, False) and\
                        does_piece_fit2(current_piece, x, y, 4, True) and\
                            does_piece_fit2(current_piece, x, y, 4, True):
                        rotate += 1
                        if rotate > 4:
                            rotate = 1
                # Restart on Game over condition only
                if event.key == pygame.K_r and game_over:
                    reset_game()
                    current_piece = piece_sequence[next_piece_index]
                    next_up = piece_sequence[next_piece_index + 1]
                    update_play_field(tetris_surface, font, font2, next_up)
                    draw_piece(tetris_surface, current_piece, x, y, False, 1)
                # Control Music
                if event.key == pygame.K_m and not game_over and music:
                    music = False
                    play_music(False)
                if event.key == pygame.K_n and not game_over and not music:
                    music = True
                    play_music(True)
                # Pause Game
                if event.key == pygame.K_p and not pause and not game_over:
                    pause = True


# Call main
main()
