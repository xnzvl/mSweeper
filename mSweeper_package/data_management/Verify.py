import json
import os.path

import mSweeper_package.data_management as here


def check_signature(filename: str) -> bool:
    if not os.path.isfile(filename):
        return False


def sign_file(filename: str) -> bool:
    pass
