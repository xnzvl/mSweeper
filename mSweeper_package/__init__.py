from enum import Enum
from typing import Dict

from . import Session
from . import minesweeper as ms


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


DATA_FOLDER = "something/"  # + some file/directory?

SOFTWARE_TITLE = ":: mSweeper _"
SOFTWARE_VERSION = "??"

WINDOW_PREFIXES = {
    ms.Minesweeper_state.UNINITIALIZED: "",
    ms.Minesweeper_state.PLAYING:       "Game in progress - ",
    ms.Minesweeper_state.GAME_LOST:     "Game lost - ",
    ms.Minesweeper_state.GAME_WON:      "Game won! - "
}


DIFFICULTY_DICT: Dict[Difficulty, Dict[str, int]] = {
    Difficulty.EASY: {
        "mines":  10,
        "width":   8,
        "height":  8
    },
    Difficulty.MEDIUM: {
        "mines":  40,
        "width":  16,
        "height": 16
    },
    Difficulty.HARD: {
        "mines":  99,
        "width":  30,
        "height": 16
    }
}


def new_session() -> Session.Session:
    return Session.Session()
