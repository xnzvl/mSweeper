from typing import List, Optional
from random import randint

import stopwatch

import uber


Cell_state_t = uber.mCell_state_t
Cell_value_t = uber.mCell_value_t

Cell_t = uber.mCell_t
# 0bXX XXXX             (cell)
#   ├┘ └──┴─ mine-bits  (cell value)
#   └─────── state-bits (cell state)

Click_t = uber.mClick_t
Dimensions_t = uber.mDimensions_t
Minesweeper_t = uber.mMinesweeper_t
Position_t = uber.mPosition_t
Sweeper_state_t = uber.mSweeper_state_t
Time_tuple_t = uber.mTime_tuple_t


# Constants for cell values
MINE = 0b1111
UNKNOWN = 0b1110

# Masks
MINES_MASK = 0b1111
STATE_MASK = 0b11_0000

# Cell_state_t constants
COVERED, FLAG, SHOWN = 0b11_0000, 0b10_0000, 0b01_0000

# Minesweeper states
UNINITIALIZED = 0
PLAYING = 1
GAME_WON = 2
GAME_LOST = 3


def get_cell_value(
    cell: Cell_value_t
) -> int:
    return cell & MINES_MASK


def get_cell_state(
    cell: Cell_state_t
) -> Cell_state_t:
    return cell & STATE_MASK


class Field:
    def __init__(
        self,
        dimensions: Dimensions_t
    ) -> None:
        width, height = dimensions

        self.inner: Minesweeper_t = [
            [COVERED for _ in range(width)] for _ in range(height)
        ]
        default_cell = COVERED | UNKNOWN
        self.outer: Minesweeper_t = [
            [default_cell for _ in range(width)] for _ in range(height)
        ]

    def get_inner_cell(
        self,
        x: int,
        y: int
    ) -> Cell_t:
        return self.inner[y][x]

    def get_inner_value(
        self,
        x: int,
        y: int
    ) -> Cell_value_t:
        return self.inner[y][x] & MINES_MASK

    def get_inner_state(
        self,
        x: int,
        y: int
    ) -> Cell_state_t:
        return self.inner[y][x] & STATE_MASK

    def set_inner_value(
        self,
        x: int,
        y: int,
        value: int
    ) -> None:
        self.inner[y][x] |= value

    def set_inner_state(
        self,
        x: int,
        y: int,
        state: Cell_state_t
    ) -> None:
        self.inner[y][x] = (self.inner[y][x] & ~STATE_MASK) | state
        self.outer[y][x] = self.inner[y][x] \
            if state == SHOWN \
            else (state | UNKNOWN)

    def project_inner(
        self
    ) -> None:
        for y, row in enumerate(self.inner):
            for x, cell in enumerate(row):
                self.outer[y][x] = cell


class Minesweeper:
    def __init__(
        self,
        dimensions: Dimensions_t,
        number_of_mines: int
    ) -> None:
        width, height = dimensions

        if height < 5 or width < 5:
            raise ValueError("invalid dimensions")
        if number_of_mines >= height * width - 9 or number_of_mines < 1:
            raise ValueError("invalid number of mines")

        self.height = height
        self.width = width
        self.mines = number_of_mines
        self.flags = 0
        self._to_uncover = height * width - self.mines

        self._field = Field(dimensions)
        self._state = UNINITIALIZED

        self._stopwatch = stopwatch.Stopwatch()
        self._time: Optional[Time_tuple_t] = None

    def _in_proximity(
        self,
        position: Position_t
    ) -> List[Position_t]:
        x, y = position
        result: List[Position_t] = []

        for tmp_x in range(
            max(x - 1, 0), min(x + 1, self.width - 1) + 1
        ):
            for tmp_y in range(
                max(y - 1, 0), min(y + 1, self.height - 1) + 1
            ):
                if not (tmp_x == x and tmp_y == y):
                    result.append((tmp_x, tmp_y))

        return result

    def _plant_mines(
        self,
        skip_origin: Position_t
    ) -> None:
        cells_to_skip = set(self._in_proximity(skip_origin))
        cells_to_skip.add(skip_origin)

        mines_planted = 0
        while mines_planted < self.mines:
            rand_x = randint(0, self.width - 1)
            rand_y = randint(0, self.height - 1)

            if not self._is_mine(self._field.get_inner_value(rand_x, rand_y)) \
                    and (rand_x, rand_y) not in cells_to_skip:
                self._field.set_inner_value(rand_x, rand_y, MINE)
                mines_planted += 1

    def _fill_numbers(
        self
    ) -> None:
        for x in range(self.width):
            for y in range(self.height):
                mines = self._count_around((x, y), MINES_MASK, MINE)
                self._field.set_inner_value(x, y, mines)

    def _field_init(
        self,
        position: Position_t
    ) -> None:
        self._plant_mines(position)
        self._fill_numbers()
        self._stopwatch.start()
        self._set_ms_state(PLAYING)

    ###########################################################################

    def _is_mine(
        _,
        cell: Cell_t
    ) -> bool:
        return (cell & MINES_MASK) == MINE

    def _set_ms_state(
        self,
        ms_state: Sweeper_state_t
    ) -> None:
        if self._state != GAME_LOST:
            self._state = ms_state

        if ms_state == GAME_LOST or ms_state == GAME_WON:
            self._field.project_inner()

            if ms_state == GAME_WON:
                self._time = self._stopwatch.get_time_tuple()

    def _set_cell_state(
        self,
        position: Position_t,
        state: Cell_state_t
    ) -> None:
        x, y = position
        old_state = self._field.get_inner_state(x, y)
        self._field.set_inner_state(x, y, state)

        if old_state == FLAG:
            self.flags -= 1
        if state == FLAG:
            self.flags += 1

        elif state == SHOWN:
            self._to_uncover -= 1

            if self._to_uncover == 0:
                self._set_ms_state(GAME_WON)

        if self._is_mine(self._field.get_inner_value(x, y)) and state == SHOWN:
            self._set_ms_state(GAME_LOST)

    def _flood_reveal(
        self,
        position: Position_t
    ) -> None:
        rec_stack = [position]

        while len(rec_stack) > 0:
            popped = rec_stack.pop()
            pop_x, pop_y = popped

            if self._field.get_inner_state(pop_x, pop_y) == SHOWN:
                continue

            self._set_cell_state(popped, SHOWN)

            if self._field.get_inner_value(pop_x, pop_y) == 0:
                for x, y in self._in_proximity(popped):
                    if (self._field.get_inner_state(x, y)) != SHOWN:
                        rec_stack.append((x, y))

    def _count_around(
        self,
        position: Position_t,
        mask: int,
        to_count: int  # MINES/flags
    ) -> int:
        counter = 0

        for x, y in self._in_proximity(position):
            if (self._field.get_inner_cell(x, y) & mask) == to_count:
                counter += 1

        return counter

    def _special_move(
        self,
        position: Position_t
    ) -> None:
        x, y = position
        if self._count_around(position, STATE_MASK, FLAG) \
                != self._field.get_inner_value(x, y):
            return

        for p_x, p_y in self._in_proximity(position):
            if self._field.get_inner_state(p_x, p_y) == COVERED:
                self._flood_reveal((p_x, p_y))

    def _is_playable(
        self
    ) -> bool:
        return self._state != GAME_LOST and self._state != GAME_WON

    ###########################################################################

    def _click_wrapper(
        self,
        position: Position_t,
        button: Click_t
    ) -> None:
        if not self._is_playable():
            return

        self._stopwatch.stop()
        button(position)
        self._stopwatch.resume()

    def _lmb(  # PRESS
        self,
        position: Position_t
    ) -> None:
        x, y = position
        c_state = self._field.get_inner_state(x, y)

        if self._state == UNINITIALIZED and c_state != FLAG:
            self._field_init(position)

        if c_state == COVERED:
            self._flood_reveal(position)
        elif c_state == SHOWN:
            self._special_move(position)

    def _rmb(  # FLAG
        self,
        position: Position_t
    ) -> None:
        x, y = position
        c_state = self._field.get_inner_state(x, y)

        if c_state != SHOWN:
            self._set_cell_state(
                position,
                FLAG if c_state != FLAG else COVERED
            )

    ###########################################################################

    def get_time(
        self
    ) -> Time_tuple_t:
        if self._time is None:
            raise ValueError("time is not set")
        return self._time

    def get_data(
        self
    ) -> Minesweeper_t:
        return self._field.outer

    def get_state(
        self
    ) -> Sweeper_state_t:
        return self._state

    def lmb(
        self,
        position: Position_t
    ) -> None:
        self._click_wrapper(position, self._lmb)

    def rmb(
        self,
        position: Position_t
    ) -> None:
        self._click_wrapper(position, self._rmb)
