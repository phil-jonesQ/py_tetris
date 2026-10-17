# py_tetris

A Tetris clone written in Python with pygame.

## Run

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then sync
the project dependencies and run the game:

```powershell
uv sync
uv run py-tetris
```

The game expects the files in `game_assets/` and `high_score.json` beside the
application. Use `build.ps1` to create the packaged Windows build.

## Test and build

```powershell
uv sync --extra dev
uv run pytest
.\build.ps1
```

The build script runs the test suite, packages the game with PyInstaller, and
creates `dist/py_tetris.zip`.

## Controls

- `S`: start from the title screen
- Arrow keys: move and rotate
- `Space`: hard drop
- `P`: pause or resume
- `N` / `M`: enable or disable music
- `R`: restart after game over
- On the game-over screen, use the arrow keys to enter a three-letter name and
  `Space` or `Enter` to save it

## Structure

`py_tetris.py` is a small compatibility entry point. The `game/` package contains
the game controller, rendering, shared configuration, board, and piece models;
reusable audio and high-score helpers live in `game/utils/`.

The bundled music and sound effects are original, softly synthesized mono WAV
assets kept under their existing filenames in `game_assets/`.
