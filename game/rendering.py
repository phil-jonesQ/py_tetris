"""Pygame rendering for the board and game screens."""

import pygame

from game.config import (
    BLACK,
    BOARD_LEFT,
    BOARD_TOP,
    CELL_SIZE,
    COLORS,
    GREEN,
    GREY,
    RED,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from game.models import Piece


class GameRenderer:
    def __init__(self, surface, score_store):
        self.surface = surface
        self.score_store = score_store
        self.ui_font = pygame.font.SysFont("Arial", 25)

    def _text(self, text, font, color, position):
        self.surface.blit(font.render(text, True, color), position)

    def _draw_cell(self, column, row, color, left=BOARD_LEFT, top=BOARD_TOP):
        pygame.draw.rect(
            self.surface,
            color,
            (left + column * CELL_SIZE, top + row * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2),
        )

    def _draw_piece(self, piece, left, top):
        for column, row in piece.cells():
            if row >= 0:
                self._draw_cell(column, row, COLORS[piece.kind], left, top)

    def _draw_board(self, game):
        for row in range(game.board.height):
            for column in range(game.board.width):
                kind = game.board.cells[row][column]
                self._draw_cell(column, row, GREY if kind is None else COLORS[kind])
        if game.active_piece is not None and game.state == game.PLAYING:
            self._draw_piece(game.active_piece, BOARD_LEFT, BOARD_TOP)

    def _draw_preview(self, kind):
        self._text("NEXT", self.ui_font, WHITE, (WINDOW_WIDTH - 190, WINDOW_HEIGHT // 2 - 80))
        self._draw_piece(Piece(kind, 0, 0), WINDOW_WIDTH - 200, WINDOW_HEIGHT // 2)

    def _draw_scores(self, name_entry=None):
        self._text("HIGH SCORES", self.ui_font, RED, (10, 20))
        scores = self.score_store.load()
        if name_entry is not None and not name_entry.finished:
            scores.append([name_entry.name, name_entry.score])
            scores.sort(key=lambda entry: entry[1], reverse=True)
        for row, (name, score) in enumerate(scores[:16]):
            color = GREEN if row == 0 else WHITE
            y = 55 + row * CELL_SIZE
            if name_entry is not None and name == name_entry.name and score == name_entry.score and not name_entry.finished:
                for index, letter in enumerate(name):
                    letter_color = RED if index == name_entry.selected else (0, 0, 255)
                    self._text(letter, self.ui_font, letter_color, (45 + index * 15, y))
                self._text(str(score), self.ui_font, color, (45 + CELL_SIZE * 3, y))
            else:
                self._text(name, self.ui_font, color, (45, y))
                self._text(str(score), self.ui_font, color, (45 + CELL_SIZE * 3, y))

    def draw(self, game):
        self.surface.fill(BLACK)
        self._draw_board(game)
        pygame.draw.line(self.surface, WHITE, (0, WINDOW_HEIGHT - 65), (WINDOW_WIDTH, WINDOW_HEIGHT - 65))
        score_color = RED if game.state in (game.START, game.GAME_OVER) else WHITE
        self._text(f"SCORE {game.score}", self.ui_font, score_color, (20, WINDOW_HEIGHT - 60))
        self._text(f"LEVEL {game.level}", self.ui_font, score_color, (WINDOW_WIDTH - 210, WINDOW_HEIGHT - 60))
        self._draw_preview(game.piece_queue.preview)

        if game.state == game.START:
            self._text("RETRO TETRO", self.ui_font, GREEN, (WINDOW_WIDTH // 2 - 90, WINDOW_HEIGHT - CELL_SIZE * 2))
            self._text("S TO START", self.ui_font, GREEN, (WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT - CELL_SIZE))
            self._draw_scores()
        elif game.state == game.PAUSED:
            self._text("PAUSED - P TO RESUME", self.ui_font, WHITE, (WINDOW_WIDTH // 2 - 130, WINDOW_HEIGHT - CELL_SIZE * 2))
        elif game.state == game.GAME_OVER:
            self._text("GAME OVER!!", self.ui_font, RED, (WINDOW_WIDTH // 2 - 90, WINDOW_HEIGHT - CELL_SIZE * 2))
            if game.name_entry is None or game.name_entry.finished:
                self._text("R TO RESTART", self.ui_font, WHITE, (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT - CELL_SIZE))
            else:
                self._text("ENTER NAME - SPACE TO SAVE", self.ui_font, WHITE, (WINDOW_WIDTH // 2 - 165, WINDOW_HEIGHT - CELL_SIZE))
            self._draw_scores(game.name_entry)
