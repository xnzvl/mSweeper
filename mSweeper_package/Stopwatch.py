from enum import Enum
from typing import Tuple
import time


Time_tuple_t = Tuple[int, int, int, int]


class Stopwatch:

    class State(Enum):
        MEASURING = 0
        STOPPED = 1

    def __init__(
        self
    ) -> None:
        self._measured_t: float = 0
        self._last_start: float = 0
        self._state = Stopwatch.State.STOPPED

    def start(
        self
    ) -> None:
        self._state = Stopwatch.State.STOPPED
        self._last_start = 0

    def resume(
        self
    ) -> None:
        if self._state != Stopwatch.State.STOPPED:
            return

        self._state = Stopwatch.State.MEASURING
        self._last_start = time.time()

    def stop(
        self
    ) -> None:
        if self._state != Stopwatch.State.MEASURING:
            return

        self._measured_t += time.time() - self._last_start
        self._state = Stopwatch.State.STOPPED

    def is_measuring(
        self
    ) -> bool:
        return self._state == Stopwatch.State.MEASURING

    def get_time(
        self
    ) -> float:
        if self._state != Stopwatch.State.STOPPED:
            raise ValueError("stopwatch is in an unstable state")
        return self._measured_t

    def get_time_tuple(
        self
    ) -> Time_tuple_t:
        measured = int(self.get_time() * 1000000)

        micro = measured % 1000000
        measured //= 1000000

        second = measured % 60
        measured //= 60

        minute = measured % 60
        measured //= 60

        hour = measured % 24
        measured //= 24

        return (hour, minute, second, micro) \
            if measured < 1 \
            else (24, 0, 0, 0)
