import time
from datetime import datetime
from typing import Optional

import uber


Time_tuple_t = uber.mTime_tuple_t


MEASURING, STOPPED = 0, 1


class Stopwatch:
    def __init__(
        self
    ) -> None:
        self._measured_t: float = 0
        self._last_start: float = 0
        self._state: Optional[int] = None

    def start(
        self
    ) -> None:
        self.reset()
        self._state = STOPPED
        self.resume()

    def resume(
        self
    ) -> None:
        if self._state is None or self._state != STOPPED:
            raise RuntimeError(
                "attempt to resume measuring, but measuring isn't stopped"
            )

        self._state = MEASURING
        self._last_start = time.time()

    def stop(
        self
    ) -> None:
        if self._state is None or self._state != MEASURING:
            raise RuntimeError(
                "attempt to stop Stopwatch, which isn't measuring"
            )

        self._measured_t += time.time() - self._last_start
        self._state = STOPPED

    def reset(
        self
    ) -> None:
        self._measured_t = 0
        self._last_start = 0
        self._state = None

    def is_measuring(
        self
    ) -> bool:
        return self._state is not None and self._state == MEASURING

    def get_time(
        self
    ) -> float:
        if self._state is None and self._state != STOPPED:
            raise ValueError("stopwatch is in an unstable state")
        return round(self._measured_t, 6)

    def get_time_tuple(
        self
    ) -> Time_tuple_t:
        dt = datetime.fromtimestamp(self.get_time())
        return (dt.hour, dt.minute, dt.second, dt.microsecond) \
            if dt.day < 1 \
            else (24, 0, 0, 0)


def timetuple_to_str(
    t_tuple: Time_tuple_t
) -> str:
    hours, minutes, seconds, _ = t_tuple
    return f"{hours:02}:{minutes:02}:{seconds:02}"
