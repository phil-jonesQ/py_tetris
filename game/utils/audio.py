"""Pygame audio loading and playback."""

from pathlib import Path

import pygame


class AudioManager:
    def __init__(self, asset_directory):
        asset_directory = Path(asset_directory)
        pygame.mixer.init()
        self._freeze_sound = pygame.mixer.Sound(str(asset_directory / "freeze.wav"))
        self._line_sound = pygame.mixer.Sound(str(asset_directory / "got_line.wav"))
        pygame.mixer.music.load(str(asset_directory / "Tetris.wav"))
        self.music_enabled = False

    def play_freeze(self):
        self._freeze_sound.play()

    def play_line(self):
        self._line_sound.play()

    def set_music(self, enabled):
        self.music_enabled = enabled
        if enabled:
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.stop()

    def stop(self):
        pygame.mixer.music.stop()
