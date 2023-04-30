import os

import mSweeper_package.data_management.highscores as here

import mSweeper_package as mSweeper
import mSweeper_package.data_management.Verify as Verify


def default_score_book() -> here.Score_book_t:
    return {
        mSweeper.Difficulty.EASY: []
    }


def load_score_book() -> here.Score_book_t:
    if not os.path.isfile(here.SCORE_FILE):
        return default_score_book()

    Verify.verify_file(here.SCORE_FILE)

    assert False
