from typing import List, Literal, Optional
from random import randint

import uber
import stopwatch


Cell_state_t = uber.mCell_state_t

Cell_t = uber.mCell_t
# 0bXX XXXX
#   └┤ └──┴─ mine-bits
#    └────── state-bits

Click_t = uber.mClick_t
Dimensions_t = uber.mDimensions_t
Minesweeper_t = uber.mMinesweeper_t
Position_t = uber.mPosition_t
Sweeper_state_t = Literal[0, 1, 2, 3]
Time_tuple_t = uber.mTime_tuple_t


MINE_PERCENTAGE = 0.1565

# Constant for mine
MINE = 0b1111

# Masks
MINES_MASK = 0b1111
STATE_MASK = 0b11_0000

# Cell states
COVERED, FLAG, SHOWN = 0b11_0000, 0b10_0000, 0b01_0000

# Minesweeper states
UNINITIALIZED: Literal[0] = 0
PLAYING: Literal[1] = 1
GAME_WON: Literal[2] = 2
GAME_LOST: Literal[3] = 3


def cell_to_num(
    cell: Cell_t
) -> int:
    return cell & MINES_MASK


def is_mine(
    cell: Cell_t
) -> bool:
    return (cell & MINES_MASK) == MINE


def is_shown(
    cell: Cell_t
) -> bool:
    return (cell & STATE_MASK) == SHOWN


class Minesweeper:
    def __init__(
        self,
        dimensions: Dimensions_t,
        mines: float
    ) -> None:
        width, height = dimensions

        if height < 5 or width < 5:
            raise ValueError("invalid dimensions")
        if not (0 < mines < 1
                and int(height * width * mines) > 0
                and int(height * width * (1 - mines)) > 9):
            raise ValueError("invalid mine-%")

        self.height = height
        self.width = width
        self.mines = int(height * width * mines)

        self._to_uncovered = height * width - self.mines
        self._field: Minesweeper_t = [
            [COVERED for _ in range(self.width)] for _ in range(self.height)
        ]
        self._state: Sweeper_state_t = UNINITIALIZED

        self._stopwatch = stopwatch.Stopwatch()
        self._stopwatch.start()
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
        skip_cell: Position_t
    ) -> None:
        cells_to_skip = set(self._in_proximity(skip_cell))
        cells_to_skip.add(skip_cell)

        mines_planted = 0
        while mines_planted < self.mines:
            rand_x = randint(0, self.width - 1)
            rand_y = randint(0, self.height - 1)

            if not is_mine(self._field[rand_y][rand_x]) \
                    and (rand_x, rand_y) not in cells_to_skip:
                self._field[rand_y][rand_x] |= MINE
                mines_planted += 1

    def _fill_numbers(
        self
    ) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self._field[y][x] |= \
                    self._count_around((x, y), MINES_MASK, MINE)

    def _init(
        self,
        position: Position_t
    ) -> None:
        self._stopwatch.stop()
        self._plant_mines(position)
        self._fill_numbers()
        self._state == PLAYING
        self._stopwatch.resume()

    ###########################################################################

    def _set_final_state(
        self,
        state: Sweeper_state_t
    ) -> None:
        self._state = state
        assert not self._stopwatch.is_measuring()
        self._time = self._stopwatch.get_time_tuple()

    def _set_cell_state(
        self,
        position: Position_t,
        state: Cell_state_t
    ) -> None:
        x, y = position
        self._field[y][x] = (self._field[y][x] & ~STATE_MASK) | state

    def _flood_reveal(
        self,
        position: Position_t
    ) -> None:
        self._set_cell_state(position, SHOWN)
        self._to_uncovered -= 1

        if self._to_uncovered == 0 and self._state != GAME_LOST:
            self._state = GAME_WON

        for x, y in self._in_proximity(position):
            if (self._field[y][x] & STATE_MASK) != SHOWN:
                self._flood_reveal((x, y))

    def _count_around(
        self,
        position: Position_t,
        mask: int,
        to_count: int  # MINES/flags
    ) -> int:
        counter = 0

        for x, y in self._in_proximity(position):
            if (self._field[y][x] & mask) == to_count:
                counter += 1

        return counter

    def _special_move(
        self,
        position: Position_t
    ) -> None:
        x, y = position
        if self._count_around(position, STATE_MASK, FLAG) != self._field[y][x]:
            return

        for p_x, p_y in self._in_proximity(position):
            if self._field[p_y][p_x] & STATE_MASK == COVERED:
                self._set_cell_state((p_x, p_y), SHOWN)

    def _is_playable(
        self
    ) -> bool:
        return self._state != GAME_LOST and self._state != GAME_WON

    def _click_wrap(
        self,
        position: Position_t,
        button: Click_t
    ) -> None:
        self._stopwatch.stop()
        button(position)
        self._stopwatch.resume()

    ###########################################################################

    def _lmb(  # PRESS
        self,
        position: Position_t
    ) -> None:
        if not self._is_playable():
            return

        if self._state == UNINITIALIZED:
            self._init

        cell = self._field[position[1]][position[0]]
        c_state = cell & STATE_MASK

        if c_state == COVERED:
            if is_mine(cell):
                self._set_cell_state(position, SHOWN)
                self._state == GAME_LOST
            else:
                self._flood_reveal(position)
        elif c_state == SHOWN:
            self._special_move(position)

    def _rmb(  # FLAG
        self,
        position: Position_t
    ) -> None:
        if not self._is_playable():
            return

        x, y = position
        c_state = self._field[y][x] & STATE_MASK

        if c_state != SHOWN:
            new_state = FLAG if c_state != FLAG else COVERED
            self._set_cell_state(position, new_state)

    ###########################################################################

    def get_data(
        self
    ) -> Minesweeper_t:
        return self._field

    def get_state(
        self
    ) -> Sweeper_state_t:
        return self._state

    def lmb(
        self,
        position: Position_t
    ) -> None:
        self._click_wrap(position, self._lmb)

    def rmb(
        self,
        position: Position_t
    ) -> None:
        self._click_wrap(position, self._rmb)
