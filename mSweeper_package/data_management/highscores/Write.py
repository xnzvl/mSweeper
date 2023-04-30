from typing import Dict, List

import json
import os

import mSweeper_package.data_management.highscores as here

import mSweeper_package as mSweeper
import mSweeper_package.data_management.Verify as Verify


def stringify_keys(
        score_book: here.Score_book_t
) -> Dict[str, List[here.Score_record_t]]:
    stringified: Dict[str, List[here.Score_record_t]] = {}

    for diff, scores in score_book.items():
        stringified[diff.value] = scores

    return stringified


def assert_dir() -> None:
    if os.path.isdir(mSweeper.DATA_FOLDER):
        return

    os.mkdir(mSweeper.DATA_FOLDER)


def write_score_book(
        score_book: here.Score_book_t
) -> None:
    assert_dir()

    json.dump(
        stringify_keys(score_book),
        open(here.SCORE_FILE, 'w'),
        indent=4
    )

    Verify.sign_file(here.SCORE_FILE)
