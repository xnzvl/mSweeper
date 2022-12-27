from typing import List, Callable
import datetime

import uber


Score_record_t = uber.mScore_record_t
Difficult_t = uber.mDifficulty_t
Time_tuple_t = uber.mTime_tuple_t


ALLOWED_CHARS = uber.ALLOWED_CHARS
HIGHSCORE_FILE = ".mSweeper_highscores.txt"
INVALID_RECORD = ValueError("Highscore record is invalid")

SPLIT_CHAR = '_'
assert SPLIT_CHAR not in ALLOWED_CHARS
DEFAULT_LINE = SPLIT_CHAR.join(["##:##:##.######", "####-##-##", "#"]) + '\n'


class Cypher:
    def __init__(
        self,
        encrypt_f: Callable[[str], str],
        decrypt_f: Callable[[str], str]
    ) -> None:
        self._encrypt_f = encrypt_f
        self._decrypt_f = decrypt_f

        self._check()

    def encrypt(
        self,
        string: str
    ) -> str:
        return self._encrypt_f(string)

    def decrypt(
        self,
        string: str
    ) -> str:
        return self._decrypt_f(string)

    def _check(
        self
    ) -> str:
        for char in ALLOWED_CHARS:
            if char != self.decrypt(self.encrypt(char)):
                raise ValueError("Invalid cypher (1:1 requested)")


class Highscores:
    def __init__(
        self,
        hfile: str,
        cypher: Cypher
    ) -> None:
        self.filename = hfile
        self.cypher = cypher

        self.scores_easy: List[Score_record_t] = []
        self.scores_medium: List[Score_record_t] = []
        self.scores_hard: List[Score_record_t] = []

        self._load_hfile()

    def should_be_recorded(
        self,
        score: Score_record_t,
        difficultry: Difficult_t
    ) -> bool:
        assert False  # TODO

    def add_highscore(
        self,
        score: Score_record_t,
        difficulty: Difficult_t
    ) -> None:
        assert False  # TODO

    def _check_order(
        self
    ) -> None:
        for diff in [self.scores_easy, self.scores_medium, self.scores_hard]:
            continue  # TODO

    def _try_parse_line(
        self,
        line: str
    ) -> Score_record_t:
        line_parts = self.cypher.decrypt(line).split(SPLIT_CHAR)

        if len(line_parts) != 3 \
                or len(line_parts[0]) != 15 \
                or len(line_parts[1]) != 10:
            raise INVALID_RECORD

        return self._try_parse_time(line_parts[0]), \
            self._try_parse_date(line_parts[1]), \
            line_parts[2]

    def _try_parse_time(
        self,
        time_str: str
    ) -> Time_tuple_t:
        time_parts = time_str.replace('.', ':').split(':')

        if len(time_parts) != 4 \
                or len(time_parts[0]) != 2 \
                or len(time_parts[1]) != 2 \
                or len(time_parts[2]) != 2 \
                or len(time_parts[3]) != 6:
            raise INVALID_RECORD

        return int(time_parts[0]), \
            int(time_parts[1]), \
            int(time_parts[2]), \
            int(time_parts[3])

    def _try_parse_date(
        self,
        date_str: str
    ) -> str:
        datetime.date.fromisoformat(date_str)
        return date_str

    def _load_hfile(
        self
    ) -> None:
        diffs = [
            self.scores_easy,
            self.scores_medium,
            self.scores_hard
        ]

        with open(self.filename, 'r') as f:
            i = 0
            for line in f:
                if line == DEFAULT_LINE or line == "\n":
                    continue

                diffs[i // 10].append(self._try_parse_line(line))
                i += 1

                if i > 30:
                    raise ValueError("Highscore file has invalid format")

        self._check_order()

    def _write_hfile(
        self
    ) -> None:
        assert False  # TODO


def create_default_hfile(
    filename: str
) -> None:
    with open(filename, 'w') as f:
        for i in range(3):
            for _ in range(10):
                f.write(DEFAULT_LINE)

            if i != 2:
                f.write('\n')


def main() -> None:
    # create_default_hfile(HIGHSCORE_FILE)

    c = Cypher(lambda x: x, lambda x: x)
    hs = Highscores(HIGHSCORE_FILE, c)

    print(sorted(hs.scores_easy))
    print(hs.scores_easy)


if __name__ == "__main__":
    main()
