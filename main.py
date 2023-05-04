import sys

import mSweeper_package as mSweeper
import project_wrapper.super_user as su


def main() -> None:
    if len(sys.argv) != 1 and len(sys.argv) != 2:
        return

    if len(sys.argv) == 2:
        su.init_super_user()

    mSweeper.new_session()


if __name__ == '__main__':
    main()
