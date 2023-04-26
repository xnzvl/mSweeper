import os

from .. import data_management as here

from . import Verify

from ... import mSweeper_package as mSweeper


def default_score_book() -> here.Score_book_t:
    return {
        mSweeper.Difficulty.EASY: []
    }


def load_score_book() -> here.Score_book_t:
    if not os.path.isfile(here.SCORE_FILE):
        return default_score_book()

    Verify.verify_file(here.SCORE_FILE)

    assert False
