from typing import Callable, Union, Tuple, List, Dict, Any
from enum import Enum


mTime_tuple_t = Tuple[int, int, int, int]
mScore_record_t = Tuple[mTime_tuple_t, str, str]

mCell_t = int
mPosition_t = Tuple[int, int]
mDimensions_t = Tuple[int, int]
mCell_state_t = int
mCell_value_t = int
mMinesweeper_t = List[List[mCell_t]]
mClick_t = Callable[[mPosition_t], None]
mSweeper_state_t = int
mAI_player_t = Any  # TODO

mConfig_dict = Dict[str, Union[str, Dict[str, Dict[str, int]]]]
mContext_t = int


CONTEXT_MAIN_MENU = 0
CONTEXT_SWEEPER = 1
CONTEXT_SWEEPER_HS = 2
CONTEXT_HIGHSCORES = 3
CONTEXT_HELP = 4

# used as indices, don't change pls ._.
EASY, MEDIUM, HARD = 0, 1, 2

ALL_CHARS = set(
        [chr(i) for i in range(ord(' '), ord('~') + 1)]
    )

ALLOWED_CHARS = set(
        [chr(i) for i in range(ord('A'), ord('z') + 1) if chr(i).isalnum()]
    ) | set([' ', '-', '_', ':', '.'])

CONFIG_FILE = ".mSweeper_cnfg.json"

DEFAULT_CONFIG: mConfig_dict = {
    "_comment":           "",
    "DEFAULT_DIFFICULTY": "MEDIUM",
    "NICK":               "cry_baby_007",

    "HIGHSCORE_FILE":     ".mSweeper_scrs.txt",

    "DIFFICULTIES": {
        "EASY": {
            "mines":  10,
            "width":   8,
            "height":  8
        },
        "MEDIUM": {
            "mines":  40,
            "width":  16,
            "height": 16
        },
        "HARD": {
            "mines":  99,
            "width":  30,
            "height": 16
        }
    }
}


class Difficulty_t(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
