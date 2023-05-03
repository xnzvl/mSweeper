import os
import os.path

import mSweeper_package as mSweeper

HASH_FILE = os.path.join(mSweeper.DATA_FOLDER, ".verify_hashes")
NICK_FILE = os.path.join(mSweeper.DATA_FOLDER, "nick")

DEFAULT_NICKNAME = "Nobody"


def assert_dir() -> None:
    if not os.path.isdir(mSweeper.DATA_FOLDER):
        os.mkdir(mSweeper.DATA_FOLDER)
