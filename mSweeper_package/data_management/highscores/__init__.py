from typing import Dict, List, Tuple

from ... import Stopwatch

import mSweeper_package as mSweeper


Score_record_t = Tuple[Stopwatch.Time_tuple_t, str, str]  # time, date, nick
Score_book_t = Dict[mSweeper.Difficulty, List[Score_record_t]]


SCORE_FILE = mSweeper.DATA_FOLDER + "scores"

INVALID_HASH = ValueError("Corrupted file")
INVALID_FORMAT = ValueError("Score record has invalid format")
INVALID_RECORD = ValueError("Score record is invalid")

ALLOWED_CHARS = set(
    [chr(i) for i in range(ord('A'), ord('Z') + 1)] +
    [chr(i) for i in range(ord('a'), ord('z') + 1)] +
    [chr(i) for i in range(ord('0'), ord('9') + 1)] +
    ["_", "-"]
)

SPLIT_CHAR = ","
END_CHAR = "<"
assert SPLIT_CHAR not in ALLOWED_CHARS and \
    END_CHAR not in ALLOWED_CHARS

BLANK_RECORD = SPLIT_CHAR.join(["##:##:##.######", "####-##-##", END_CHAR])
