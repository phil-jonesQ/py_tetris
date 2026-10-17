"""Game controller and pygame application loop."""

import pygame

from game.config import VERSION, WINDOW_HEIGHT, WINDOW_WIDTH, application_directory
from game.models import Board, Piece, PieceQueue
from game.rendering import GameRenderer
from game.utils.audio import AudioManager
from game.utils.scores import HighScoreStore, NameEntry


class Game:
    START = "start"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    FALL_RATES = (1200, 1200, 1100, 1000, 900, 800, 700, 600, 500, 400)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(f"Tetris {VERSION}")
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score_store = HighScoreStore()
        self.audio = AudioManager(application_directory() / "game_assets")
        self.renderer = GameRenderer(self.surface, self.score_store)
        self.state = self.START
        self.running = True
        self.new_round()

    @property
    def level(self):
        return max(1, min(10, (self.score - 1) // 100 + 1))

    def new_round(self):
        self.board = Board()
        self.piece_queue = PieceQueue()
        self.active_piece = Piece(self.piece_queue.take())
        self.score = 0
        self.fall_elapsed = 0.0
        self.name_entry = None

    def start_round(self):
        self.new_round()
        self.state = self.PLAYING

    def _finish_piece(self):
        self.audio.play_freeze()
        if not self.board.lock(self.active_piece):
            self._end_game()
            return

        lines = self.board.clear_full_lines()
        if lines:
            self.score += sum(range(2, lines + 2))
            self.audio.play_line()

        self.active_piece = Piece(self.piece_queue.take())
        if not self.board.fits(self.active_piece):
            self._end_game()

    def _end_game(self):
        self.state = self.GAME_OVER
        self.active_piece = None
        self.name_entry = NameEntry(self.score)
        self.audio.set_music(False)

    def _move(self, dx, dy):
        piece = self.active_piece
        if self.board.fits(piece, x=piece.x + dx, y=piece.y + dy):
            piece.x += dx
            piece.y += dy
            return True
        return False

    def _rotate(self):
        rotation = (self.active_piece.rotation + 1) % 4
        if self.board.fits(self.active_piece, rotation=rotation):
            self.active_piece.rotation = rotation

    def _hard_drop(self):
        self.score += 2
        while self._move(0, 1):
            pass
        self._finish_piece()

    def _handle_playing_key(self, key):
        if key == pygame.K_LEFT:
            self._move(-1, 0)
        elif key == pygame.K_RIGHT:
            self._move(1, 0)
        elif key == pygame.K_DOWN:
            if not self._move(0, 1):
                self._finish_piece()
        elif key == pygame.K_UP:
            self._rotate()
        elif key == pygame.K_SPACE:
            self._hard_drop()
        elif key == pygame.K_p:
            self.state = self.PAUSED
        elif key == pygame.K_m:
            self.audio.set_music(False)
        elif key == pygame.K_n:
            self.audio.set_music(True)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return
        if event.type != pygame.KEYDOWN:
            return

        if self.state == self.START and event.key == pygame.K_s:
            self.start_round()
        elif self.state == self.PLAYING:
            self._handle_playing_key(event.key)
        elif self.state == self.PAUSED and event.key == pygame.K_p:
            self.state = self.PLAYING
        elif self.state == self.GAME_OVER:
            if self.name_entry is not None and not self.name_entry.finished:
                self.name_entry.handle_key(event.key, self.score_store)
            elif event.key == pygame.K_r:
                self.start_round()

    def update(self, elapsed):
        if self.state != self.PLAYING:
            return
        self.fall_elapsed += elapsed
        fall_interval = 0.37 * self.FALL_RATES[self.level - 1] / 1000
        while self.fall_elapsed >= fall_interval and self.state == self.PLAYING:
            self.fall_elapsed -= fall_interval
            if not self._move(0, 1):
                self._finish_piece()

    def run(self):
        try:
            while self.running:
                elapsed = self.clock.tick(60) / 1000
                for event in pygame.event.get():
                    self.handle_event(event)
                self.update(elapsed)
                self.renderer.draw(self)
                pygame.display.flip()
        finally:
            self.audio.stop()
            pygame.quit()


def main():
    Game().run()
