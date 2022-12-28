from typing import List, Callable
import datetime

import uber


Score_record_t = uber.mScore_record_t
Difficult_t = uber.mDifficulty_t
Time_tuple_t = uber.mTime_tuple_t


ALLOWED_CHARS = uber.ALLOWED_CHARS
HIGHSCORE_FILE = ".mSweeper_highscores.txt"
INVALID_RECORD = ValueError("Highscore record is invalid")
INVALID_FORMAT = ValueError("Highscore file has invalid format")

SPLIT_CHAR = '^'
assert SPLIT_CHAR not in ALLOWED_CHARS and SPLIT_CHAR != uber.SPACE_REPLACEMENT
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
        self._filename = hfile
        self._cypher = cypher

        self._difficulties: List[List[Score_record_t]] = [
            [],  # easy   difficulty
            [],  # medium difficulty
            []   # hard   difficulty
        ]

        self._load_hfile()

    def _should_be_recorded(
        self,
        score: Score_record_t,
        difficulty: Difficult_t
    ) -> bool:
        return len(self._difficulties[difficulty]) < 10 \
            or score < self._difficulties[difficulty][-1]

    def score(
        self,
        score: Score_record_t,
        difficulty: Difficult_t
    ) -> None:
        if not self._should_be_recorded(score, difficulty):
            return

        diff = self._difficulties[difficulty]
        diff.append(score)
        diff.sort()
        diff.pop()
        self._difficulties[difficulty] = diff

        self._write_hfile()

    def _check_order(
        self
    ) -> None:
        for diff in self._difficulties:
            if diff != sorted(diff):
                raise INVALID_FORMAT

    def _try_parse_line(
        self,
        line: str
    ) -> Score_record_t:
        line_parts = self._cypher.decrypt(line).split(SPLIT_CHAR)

        if len(line_parts) != 3 \
                or len(line_parts[0]) != 15 \
                or len(line_parts[1]) != 10:
            raise INVALID_RECORD

        return self._try_parse_time(line_parts[0]), \
            self._try_parse_date(line_parts[1]), \
            line_parts[2][:-1]

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
        with open(self._filename, 'r') as f:
            i = 0
            for line in f:
                if line == DEFAULT_LINE or line == "\n":
                    continue

                self._difficulties[i // 10].append(self._try_parse_line(line))
                i += 1

                if i > 30:
                    raise INVALID_FORMAT

        self._check_order()

    def _write_hfile(
        self
    ) -> None:
        with open(self._filename, 'w') as output:
            for diff in self._difficulties:
                for score in diff:
                    output.write(self._cypher.encrypt(score) + '\n')

                output.write('\n')


def create_default_hfile(
    filename: str
) -> None:
    with open(filename, 'w') as file:
        for _ in range(3):
            for _ in range(10):
                file.write(DEFAULT_LINE)

            file.write('\n')


def default_cypher_encrypt(
    input: str
) -> str:
    # TODO
    return input


def default_cypher_decrypt(
    input: str
) -> str:
    # TODO
    return input


def main() -> None:
    # create_default_hfile(HIGHSCORE_FILE)

    c = Cypher(default_cypher_encrypt, default_cypher_decrypt)
    hs = Highscores(HIGHSCORE_FILE, c)

    for diff in hs._difficulties:
        for line in diff:
            print(line)


if __name__ == "__main__":
    main()
