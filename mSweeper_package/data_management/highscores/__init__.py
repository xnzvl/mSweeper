from typing import Dict, List, Tuple

import os.path

import mSweeper_package as mSweeper
import mSweeper_package.Stopwatch as Stopwatch


Score_record_t = Tuple[Stopwatch.Time_tuple_t, str, str]  # time, date, nick
Score_book_t = Dict[mSweeper.Difficulty, List[Score_record_t]]

SCORE_FILE = os.path.join(mSweeper.DATA_FOLDER, "scores")

ALLOWED_CHARS = set(
    [chr(i) for i in range(ord('A'), ord('Z') + 1)] +
    [chr(i) for i in range(ord('a'), ord('z') + 1)] +
    [chr(i) for i in range(ord('0'), ord('9') + 1)] +
    ["_", "-", " ", ":", "/", "\\", ".", "(", ")", "[", "]"]
)
