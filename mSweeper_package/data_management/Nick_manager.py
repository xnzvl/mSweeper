import os.path

import mSweeper_package.data_management as here

import mSweeper_package.data_management.Verify as Verify


def load_nickname() -> str:
    if os.path.isfile(here.NICK_FILE) and Verify.check_hash(here.NICK_FILE):
        with open(here.NICK_FILE, 'r') as f:
            return f.read().strip()

    return here.DEFAULT_NICKNAME


def write_nickname(
        nickname: str
) -> None:
    nickname = nickname.strip()

    here.assert_dir()
    with open(here.NICK_FILE, 'w') as f:
        f.write(nickname + "\n" if nickname != "" else "")
        f.write("\n")

    Verify.hash_file(here.NICK_FILE)
