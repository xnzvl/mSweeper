from typing import List, Optional, Tuple

from .. import highscores as here

from ... import Stopwatch

import mSweeper_package as mSweeper


class Highscore_manager:
    def __init__(self) -> None:
        pass

    def score(
            self,
            time: Stopwatch.Time_tuple_t,
            nick: str,
            difficulty: mSweeper.Difficulty
    ) -> Tuple[Optional[here.Score_record_t], Optional[here.Score_record_t]]:
        return None, None

    def get_diff_scores(
            self,
            difficulty: mSweeper.Difficulty
    ) -> List[here.Score_record_t]:
        pass
