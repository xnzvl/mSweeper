import os.path

import mSweeper_package.data_management as data_management
import mSweeper_package.data_management.Verify as Verify


def load_nickname() -> str:
    if os.path.isfile(data_management.NICK_FILE) and Verify.check_hash(data_management.NICK_FILE):
        with open(data_management.NICK_FILE, 'r') as f:
            return f.read().strip()

    return "Nobody"


def write_nickname(
        nickname: str
) -> None:
    with open(data_management.NICK_FILE, 'w') as f:
        f.write(nickname + "\n" if nickname != "" else "")
        f.write("\n")

    Verify.hash_file(data_management.NICK_FILE)
