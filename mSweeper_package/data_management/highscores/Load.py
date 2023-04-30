import os.path

import mSweeper_package.data_management.highscores as here

import mSweeper_package as mSweeper
import mSweeper_package.data_management.Verify as Verify


def default_score_book() -> here.Score_book_t:
    return {
        mSweeper.Difficulty.EASY:   [],
        mSweeper.Difficulty.MEDIUM: [],
        mSweeper.Difficulty.HARD:   []
    }


def load_score_book() -> here.Score_book_t:
    if not os.path.isfile(here.SCORE_FILE) or not Verify.check_hash(here.SCORE_FILE):
        print("DEFAULT SCORES")
        return default_score_book()

    assert False
