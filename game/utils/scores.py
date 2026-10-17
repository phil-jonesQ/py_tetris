"""High-score persistence and the three-letter name-entry model."""

import json
from pathlib import Path

import pygame

from game.config import application_directory


class HighScoreStore:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else application_directory() / "high_score.json"
        self._scores = None

    def load(self):
        if self._scores is not None:
            return list(self._scores)
        try:
            with self.path.open("r", encoding="utf-8") as score_file:
                scores = json.load(score_file)
        except FileNotFoundError:
            scores = []
        self._scores = sorted(scores, key=lambda entry: entry[1], reverse=True)
        return list(self._scores)

    def save(self, scores):
        with self.path.open("w", encoding="utf-8") as score_file:
            json.dump(scores, score_file)
        self._scores = list(scores)

    def add(self, name, score):
        scores = self.load()
        scores.append([name, score])
        scores.sort(key=lambda entry: entry[1], reverse=True)
        self.save(scores)
        return scores


class NameEntry:
    def __init__(self, score):
        self.score = score
        self.letters = [0, 0, 0]
        self.selected = 0
        self.finished = False

    @property
    def name(self):
        return "".join(chr(ord("A") + letter) for letter in self.letters)

    def handle_key(self, key, store):
        if key == pygame.K_UP:
            self.letters[self.selected] = (self.letters[self.selected] + 1) % 26
        elif key == pygame.K_DOWN:
            self.letters[self.selected] = (self.letters[self.selected] - 1) % 26
        elif key == pygame.K_RIGHT:
            self.selected = (self.selected + 1) % 3
        elif key == pygame.K_LEFT:
            self.selected = (self.selected - 1) % 3
        elif key in (pygame.K_SPACE, pygame.K_RETURN):
            store.add(self.name, self.score)
            self.finished = True
