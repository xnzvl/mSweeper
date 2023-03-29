from enum import Enum
from typing import Dict


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


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
