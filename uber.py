from typing import Tuple, List


mTime_tuple_t = Tuple[int, int, int, int]
mDifficulty_t = int
mScore_record_t = Tuple[mTime_tuple_t, str, str]

mCell_t = int
mPosition_t = Tuple[int, int]
mCell_state_t = int
mMinesweeper_t = List[List[mCell_t]]


CELL_SIZE = 20
EASY, MEDIUM, HARD = 0, 1, 2

# feel free to change these
DIFFICULTY = EASY  # has to be EASY/MEDIUM/HARD tho
HIGHSCORE_FILE = ".mSweeper_highscores.txt"

ALLOWED_CHARS = set(
        [chr(i) for i in range(ord('a') - 1, ord('z') + 1) if chr(i).isalnum()]
    ) | set([' ', '-', '<', '>'])

