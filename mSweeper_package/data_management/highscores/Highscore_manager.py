from typing import List, Optional, Tuple

import mSweeper_package.data_management.highscores as here

import mSweeper_package as mSweeper
import mSweeper_package.Stopwatch as Stopwatch
import mSweeper_package.data_management.highscores.Load as Load


class Highscore_manager:
    def __init__(self) -> None:
        self.score_book: here.Score_book_t = Load.load_score_book()

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
        return self.score_book[difficulty]
