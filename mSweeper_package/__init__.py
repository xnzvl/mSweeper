from enum import Enum
from typing import Dict

import os

import mSweeper_package.minesweeper as here


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


DATA_FOLDER: str = os.path.join(os.getcwd(), ".mSweeper")

SOFTWARE_TITLE = ":: mSweeper _"
SOFTWARE_VERSION = "2.10"

WINDOW_PREFIXES = {
    here.Minesweeper_state.UNINITIALIZED: "",
    here.Minesweeper_state.PLAYING:       "Game in progress - ",
    here.Minesweeper_state.GAME_LOST:     "Game lost - ",
    here.Minesweeper_state.GAME_WON:      "Game won! - "
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

import mSweeper_package.Session as Session

def new_session() -> Session.Session:
    return Session.Session()
