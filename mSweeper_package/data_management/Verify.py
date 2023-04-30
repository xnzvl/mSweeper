from typing import Dict, Set

import hashlib
import json
import os.path

import mSweeper_package.data_management as here


def assert_file(
        filename: str
) -> None:
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            json.dump(dict(), f, indent=4)


def load_hashes() -> Dict[str, str]:
    assert_file(here.HASH_FILE)

    with open(here.HASH_FILE, 'r') as f:
        loaded = json.load(f)

    assert isinstance(loaded, dict)
    return loaded


def get_file_sha(
        filename: str
) -> str:
    sha = hashlib.sha256()
    sha.update(bytes(str(os.path.getmtime(filename)), encoding="ASCII"))

    with open(filename, 'br') as f:
        sha.update(f.read())

    sha_d = sha.hexdigest()
    return sha_d


def check_hash(
        filename: str
) -> bool:
    if not os.path.isfile(filename):
        return False

    hash_dict = load_hashes()
    desired_hash = hash_dict.get(os.path.basename(filename))
    if desired_hash is None:
        return False

    return desired_hash == get_file_sha(filename)


def hash_file(
        filename: str
) -> None:
    assert os.path.isfile(filename)

    hash_dict = load_hashes()
    hash_dict[os.path.basename(filename)] = get_file_sha(filename)

    with open(here.HASH_FILE, 'w') as f:
        json.dump(
            hash_dict,
            f,
            indent=4
        )
