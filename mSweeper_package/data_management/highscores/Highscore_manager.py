from typing import List

import datetime

import mSweeper_package.data_management.highscores as here

import mSweeper_package as mSweeper
import mSweeper_package.Stopwatch as Stopwatch
import mSweeper_package.data_management.highscores.Load as Load
import mSweeper_package.data_management.highscores.Write as Write


class Highscore_manager:
    def __init__(self) -> None:
        self.score_book: here.Score_book_t = Load.load_score_book()

    def is_worth_recording(
            self,
            difficulty: mSweeper.Difficulty,
            score: here.Score_record_t
    ) -> bool:
        return len(self.score_book[difficulty]) < 10 or score < self.score_book[difficulty][10]

    def score(
            self,
            time: Stopwatch.Time_tuple_t,
            nick: str,
            difficulty: mSweeper.Difficulty
    ) -> bool:
        score_record = (time, datetime.date.today().strftime("%Y-%m-%d"), nick)

        if self.is_worth_recording(difficulty, score_record):
            self.score_book[difficulty].append(score_record)
            self.score_book[difficulty].sort()

            if len(self.score_book[difficulty]) > 10:
                self.score_book[difficulty].pop()

            Write.write_score_book(self.score_book)

            return True

        return False

    def get_diff_scores(
            self,
            difficulty: mSweeper.Difficulty
    ) -> List[here.Score_record_t]:
        return self.score_book[difficulty]
