from typing import Dict, List

import json
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


def map_to_enum_diff(
        diff_str: str
) -> mSweeper.Difficulty:
    for diff_enum in mSweeper.Difficulty:
        if diff_str == diff_enum.value:
            return diff_enum
    assert False


def enumerate_dict(
        str_dict: Dict[str, List[here.Score_record_t]]
) -> here.Score_book_t:
    enum_dict: here.Score_book_t = dict()

    for diff, scores in str_dict.items():
        diff_enum = map_to_enum_diff(diff)
        enum_dict[diff_enum] = []

        for score in scores:
            time, date, nick = score
            h, m, s, u = time
            enum_dict[diff_enum].append(((h, m, s, u), date, nick))

    return enum_dict


def load_score_book() -> here.Score_book_t:
    if not os.path.isfile(here.SCORE_FILE) or not Verify.check_hash(here.SCORE_FILE):
        print("default scores used")
        return default_score_book()

    with open(here.SCORE_FILE, 'r') as f:
        enum_dict = enumerate_dict(json.load(f))

    return enum_dict
