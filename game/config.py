"""Shared game settings, colors, and tetromino definitions."""

import sys
from pathlib import Path


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 30
BOARD_LEFT = (WINDOW_WIDTH - BOARD_WIDTH * CELL_SIZE) // 2
BOARD_TOP = 20
VERSION = "1.11"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)

COLORS = (BLUE, ORANGE, YELLOW, RED, PURPLE, CYAN, GREEN)
SHAPES = (
    (("....", ".X..", ".X..", ".XX."),
     ("....", "XXX.", "X...", "...."),
     ("....", ".XX.", "..X.", "..X."),
     ("....", "...X", ".XXX", "....")),
    (("..X.", "..X.", ".XX.", "...."),
     ("....", "X...", "XXX.", "...."),
     ("....", ".XX.", ".X..", ".X.."),
     ("....", ".XXX", "...X", "....")),
    (("....", ".XX.", ".XX.", "...."),) * 4,
    (("....", ".X..", ".XX.", "..X."),
     ("....", ".XX.", "..XX", "...."),
     ("....", ".X..", ".XX.", "..X."),
     ("....", ".XX.", "..XX", "....")),
    (("....", ".X..", ".XX.", ".X.."),
     ("....", ".XXX", "..X.", "...."),
     ("...X", "..XX", "...X", "...."),
     ("....", "..X.", ".XXX", "....")),
    ((".X..", ".X..", ".X..", ".X.."),
     ("....", "XXXX", "....", "...."),
     (".X..", ".X..", ".X..", ".X.."),
     ("....", "XXXX", "....", "....")),
    (("....", "..X.", ".XX.", ".X.."),
     ("....", "..XX", ".XX.", "...."),
     ("....", "..X.", ".XX.", ".X.."),
     ("....", "..XX", ".XX.", "....")),
)


def application_directory():
    """Return the directory containing the game and its external assets."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent
