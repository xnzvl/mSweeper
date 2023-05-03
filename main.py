import sys

import mSweeper_package as mSweeper
import project_wrapper.superuser as su


def main() -> None:
    if len(sys.argv) != 1 and len(sys.argv) != 3:
        return

    if len(sys.argv) == 3:
        su.print_args()

    mSweeper.new_session()


if __name__ == '__main__':
    main()
