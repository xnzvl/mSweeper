from typing import Tuple, Callable, List, Any


mTime_tuple_t = Tuple[int, int, int, int]
mDifficulty_t = int
mScore_record_t = Tuple[mTime_tuple_t, str, str]

mCell_t = int
mPosition_t = Tuple[int, int]
mDimensions_t = Tuple[int, int]
mCell_state_t = int
mMinesweeper_t = List[List[mCell_t]]
mClick_t = Callable[[mPosition_t], None]
mAI_player_t = Any  # TODO


# used as indices, don't change ._.
EASY, MEDIUM, HARD = 0, 1, 2


DIFFICULTY_VALUES: Tuple[
    mDifficulty_t, mDifficulty_t, mDifficulty_t
] = EASY, MEDIUM, HARD

DIMENSIONS: List[mDimensions_t] = [
    (8, 8),  # ---- easy
    (16, 16),  # -- medium
    (30, 16)  # --- hard
]


# ======================================================

# feel free to change these two
DEFAULT_DIFFICULTY = EASY  # has to be EASY/MEDIUM/HARD tho b-><-d
HIGHSCORE_FILE = ".mSweeper_highscores.txt"

# ======================================================


ALL_CHARS = set(
        [chr(i) for i in range(ord(' '), ord('~') + 1)]
    )

ALLOWED_CHARS = set(
        [chr(i) for i in range(ord('A'), ord('z') + 1) if chr(i).isalnum()]
    ) | set([' ', '-', '_', ':', '.'])

SPACE_REPLACEMENT = '~'
assert SPACE_REPLACEMENT not in ALLOWED_CHARS
