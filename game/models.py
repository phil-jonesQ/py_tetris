"""Core Tetris pieces, piece queue, and board rules."""

from collections import deque
from dataclasses import dataclass
import random

from game.config import BOARD_HEIGHT, BOARD_WIDTH, SHAPES


@dataclass
class Piece:
    kind: int
    x: int = 3
    y: int = -2
    rotation: int = 0

    def cells(self, rotation=None, x=None, y=None):
        selected_rotation = self.rotation if rotation is None else rotation
        origin_x = self.x if x is None else x
        origin_y = self.y if y is None else y
        shape = SHAPES[self.kind][selected_rotation % 4]
        return (
            (origin_x + column, origin_y + row)
            for row, line in enumerate(shape)
            for column, cell in enumerate(line)
            if cell == "X"
        )


class PieceQueue:
    """A shuffled seven-piece bag with a continuously available preview."""

    def __init__(self, rng=None):
        self._rng = rng or random.Random()
        self._pieces = deque()
        self._fill()

    def _fill(self):
        while len(self._pieces) < 2:
            bag = list(range(len(SHAPES)))
            self._rng.shuffle(bag)
            self._pieces.extend(bag)

    def take(self):
        self._fill()
        piece = self._pieces.popleft()
        self._fill()
        return piece

    @property
    def preview(self):
        self._fill()
        return self._pieces[0]


class Board:
    def __init__(self, width=BOARD_WIDTH, height=BOARD_HEIGHT):
        self.width = width
        self.height = height
        self.cells = [[None for _ in range(width)] for _ in range(height)]

    def fits(self, piece, x=None, y=None, rotation=None):
        for column, row in piece.cells(rotation, x, y):
            if column < 0 or column >= self.width or row >= self.height:
                return False
            if row >= 0 and self.cells[row][column] is not None:
                return False
        return True

    def lock(self, piece):
        locations = tuple(piece.cells())
        if not self.fits(piece) or any(row < 0 for _, row in locations):
            return False
        for column, row in locations:
            self.cells[row][column] = piece.kind
        return True

    def clear_full_lines(self):
        remaining = [row for row in self.cells if any(cell is None for cell in row)]
        cleared = self.height - len(remaining)
        self.cells = [[None for _ in range(self.width)] for _ in range(cleared)] + remaining
        return cleared
