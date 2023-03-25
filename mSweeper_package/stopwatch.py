import time

import uber


Time_tuple_t = uber.mTime_tuple_t


MEASURING, STOPPED = 0, 1


class Stopwatch:
    def __init__(
        self
    ) -> None:
        self._measured_t: float = 0
        self._last_start: float = 0
        self._state = STOPPED

    def start(
        self
    ) -> None:
        self._state = STOPPED
        self._last_start = 0

    def resume(
        self
    ) -> None:
        if self._state != STOPPED:
            return

        self._state = MEASURING
        self._last_start = time.time()

    def stop(
        self
    ) -> None:
        if self._state != MEASURING:
            return

        self._measured_t += time.time() - self._last_start
        self._state = STOPPED

    def is_measuring(
        self
    ) -> bool:
        return self._state == MEASURING

    def get_time(
        self
    ) -> float:
        if self._state != STOPPED:
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
