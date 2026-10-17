from array import array
import json
import wave

import pygame
import pytest

from game.app import Game
from game.config import SHAPES, application_directory
from game.models import Board, Piece, PieceQueue
from game.utils.scores import HighScoreStore, NameEntry


def test_piece_has_four_cells_in_each_rotation():
    for kind in range(len(SHAPES)):
        for rotation in range(4):
            assert len(tuple(Piece(kind).cells(rotation))) == 4


def test_board_rejects_wall_floor_and_locked_cell_collisions():
    board = Board(width=4, height=4)
    piece = Piece(2, x=-2, y=0)
    assert not board.fits(piece)

    piece.x = 0
    piece.y = 2
    assert not board.fits(piece)

    piece.y = 0
    board.cells[1][1] = 3
    assert not board.fits(piece)


def test_board_locks_piece_and_clears_complete_lines():
    board = Board(width=4, height=4)
    board.cells[3] = [0, 1, None, None]
    piece = Piece(2, x=1, y=1)
    assert board.lock(piece)

    assert board.clear_full_lines() == 1
    assert board.cells[0] == [None, None, None, None]
    assert board.cells[1] == [None, None, None, None]
    assert board.cells[2] == [None, None, None, None]
    assert board.cells[3] == [None, None, 2, 2]


def test_board_does_not_lock_piece_above_visible_field():
    board = Board()
    assert not board.lock(Piece(0, y=-2))
    assert all(cell is None for row in board.cells for cell in row)


def test_piece_queue_yields_seven_piece_bags():
    queue = PieceQueue()
    first_bag = [queue.take() for _ in range(7)]
    second_bag = [queue.take() for _ in range(7)]

    assert sorted(first_bag) == list(range(len(SHAPES)))
    assert sorted(second_bag) == list(range(len(SHAPES)))
    assert queue.preview in range(len(SHAPES))


def test_name_entry_wraps_letters_and_saves_on_confirmation(tmp_path):
    store = HighScoreStore(tmp_path / "scores.json")
    entry = NameEntry(42)

    entry.handle_key(pygame.K_DOWN, store)
    entry.handle_key(pygame.K_RIGHT, store)
    entry.handle_key(pygame.K_UP, store)
    assert entry.name == "ZBA"

    entry.handle_key(pygame.K_RETURN, store)
    assert entry.finished
    assert json.loads((tmp_path / "scores.json").read_text(encoding="utf-8")) == [["ZBA", 42]]


def test_high_scores_are_sorted_by_score(tmp_path):
    store = HighScoreStore(tmp_path / "scores.json")
    store.add("LOW", 12)
    store.add("TOP", 99)

    assert store.load() == [["TOP", 99], ["LOW", 12]]


def test_missing_high_score_file_is_an_empty_table(tmp_path):
    assert HighScoreStore(tmp_path / "missing.json").load() == []


@pytest.mark.parametrize(
    ("score", "expected_level"),
    [(0, 1), (100, 1), (101, 2), (900, 9), (901, 10), (2000, 10)],
)
def test_level_progression_uses_score_thresholds(score, expected_level):
    game = Game.__new__(Game)
    game.score = score
    assert game.level == expected_level


@pytest.mark.parametrize(
    ("width", "height"),
    [(4, 4), (10, 20)],
)
def test_new_board_is_empty(width, height):
    board = Board(width=width, height=height)
    assert len(board.cells) == height
    assert all(len(row) == width for row in board.cells)
    assert all(cell is None for row in board.cells for cell in row)


@pytest.mark.parametrize(
    ("filename", "expected_duration"),
    [("Tetris.wav", 24.0), ("freeze.wav", 0.19), ("got_line.wav", 0.82)],
)
def test_sound_assets_are_valid_quiet_mono_wav_files(filename, expected_duration):
    asset_path = application_directory() / "game_assets" / filename
    with wave.open(str(asset_path), "rb") as sound:
        assert sound.getnchannels() == 1
        assert sound.getsampwidth() == 2
        assert sound.getframerate() == 22050
        assert sound.getnframes() / sound.getframerate() == pytest.approx(expected_duration, abs=0.01)
        samples = array("h", sound.readframes(sound.getnframes()))

    assert samples
    assert 0.05 < max(abs(sample) for sample in samples) / 32768 < 0.35


def test_legacy_script_still_exposes_game_entry_point():
    import py_tetris

    assert callable(py_tetris.main)
