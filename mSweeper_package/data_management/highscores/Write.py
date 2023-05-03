from typing import Dict, List

import json

import mSweeper_package.data_management.highscores as here

import mSweeper_package.data_management as data
import mSweeper_package.data_management.Verify as Verify


def stringify_keys(
        score_book: here.Score_book_t
) -> Dict[str, List[here.Score_record_t]]:
    stringified: Dict[str, List[here.Score_record_t]] = {}

    for diff, scores in score_book.items():
        stringified[diff.value] = scores

    return stringified


def write_score_book(
        score_book: here.Score_book_t
) -> None:
    data.assert_dir()

    with open(here.SCORE_FILE, 'w') as f:
        json.dump(
            stringify_keys(score_book),
            f,
            indent=4
        )

    Verify.hash_file(here.SCORE_FILE)
