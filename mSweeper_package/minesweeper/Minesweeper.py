from typing import List, Optional
import random

import mSweeper_package.minesweeper as here

import mSweeper_package.Stopwatch as Stopwatch
import mSweeper_package.minesweeper.Field as Field


class Minesweeper:
    def __init__(
            self,
            dimensions: here.Dimensions_t,
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

        self._field = Field.Field(dimensions)
        self._state = here.Minesweeper_state.UNINITIALIZED

        self._stopwatch = Stopwatch.Stopwatch()
        self._time: Optional[Stopwatch.Time_tuple_t] = None  # TODO

    def _in_proximity(
            self,
            position: here.Position_t
    ) -> List[here.Position_t]:
        x, y = position
        result: List[here.Position_t] = []

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
            skip_origin: here.Position_t
    ) -> None:
        cells_to_skip = set(self._in_proximity(skip_origin))
        cells_to_skip.add(skip_origin)

        mines_planted = 0
        while mines_planted < self.mines:
            rand_x = random.randint(0, self.width - 1)
            rand_y = random.randint(0, self.height - 1)

            if not here.is_mine(self._field.get_inner_value(rand_x, rand_y)) \
                    and (rand_x, rand_y) not in cells_to_skip:
                self._field.set_inner_value(rand_x, rand_y, here.MINE)
                mines_planted += 1

    def _fill_numbers(
            self
    ) -> None:
        for x in range(self.width):
            for y in range(self.height):
                mines = self._count_around((x, y), here.MINES_MASK, here.MINE)
                self._field.set_inner_value(x, y, mines)

    def _field_init(
            self,
            position: here.Position_t
    ) -> None:
        self._plant_mines(position)
        self._fill_numbers()
        self._stopwatch.start()
        self._set_ms_state(here.Minesweeper_state.PLAYING)

    def _set_ms_state(
            self,
            ms_state: here.Minesweeper_state
    ) -> None:
        if self._state != here.Minesweeper_state.GAME_LOST:
            self._state = ms_state

        if ms_state == here.Minesweeper_state.GAME_LOST or ms_state == here.Minesweeper_state.GAME_WON:
            self._field.project_inner()

            if ms_state == here.Minesweeper_state.GAME_WON:
                self._time = self._stopwatch.get_time_tuple()

    def _set_cell_state(
            self,
            position: here.Position_t,
            state: here.Cell_state_t
    ) -> None:
        x, y = position
        old_state = self._field.get_inner_state(x, y)
        self._field.set_inner_state(x, y, state)

        if old_state == here.FLAG:
            self.flags -= 1
        if state == here.FLAG:
            self.flags += 1

        elif state == here.SHOWN:
            self._to_uncover -= 1

            if self._to_uncover == 0:
                self._set_ms_state(here.Minesweeper_state.GAME_WON)

        if here.is_mine(self._field.get_inner_value(x, y)) and state == here.SHOWN:
            self._set_ms_state(here.Minesweeper_state.GAME_LOST)

    def _flood_reveal(
            self,
            position: here.Position_t
    ) -> None:
        rec_stack = [position]

        while len(rec_stack) > 0:
            popped = rec_stack.pop()
            pop_x, pop_y = popped

            if self._field.get_inner_state(pop_x, pop_y) == here.SHOWN:
                continue

            self._set_cell_state(popped, here.SHOWN)

            if self._field.get_inner_value(pop_x, pop_y) == 0:
                for x, y in self._in_proximity(popped):
                    if (self._field.get_inner_state(x, y)) != here.SHOWN:
                        rec_stack.append((x, y))

    def _count_around(
            self,
            position: here.Position_t,
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
            position: here.Position_t
    ) -> None:
        x, y = position
        if self._count_around(position, here.STATE_MASK, here.FLAG) \
                != self._field.get_inner_value(x, y):
            return

        for p_x, p_y in self._in_proximity(position):
            if self._field.get_inner_state(p_x, p_y) == here.COVERED:
                self._flood_reveal((p_x, p_y))

    def _is_playable(
            self
    ) -> bool:
        return self._state != here.Minesweeper_state.GAME_LOST and self._state != here.Minesweeper_state.GAME_WON

    def _click_wrapper(
            self,
            position: here.Position_t,
            button: here.Click_t
    ) -> None:
        if not self._is_playable():
            return

        self._stopwatch.stop()
        button(position)
        self._stopwatch.resume()

    def _lmb(
            self,
            position: here.Position_t
    ) -> None:
        x, y = position
        c_state = self._field.get_inner_state(x, y)

        if self._state == here.Minesweeper_state.UNINITIALIZED and c_state != here.FLAG:
            self._field_init(position)

        if c_state == here.COVERED:
            self._flood_reveal(position)
        elif c_state == here.SHOWN:
            self._special_move(position)

    def _rmb(
            self,
            position: here.Position_t
    ) -> None:
        x, y = position
        c_state = self._field.get_inner_state(x, y)

        if c_state != here.SHOWN:
            self._set_cell_state(
                position,
                here.FLAG if c_state != here.FLAG else here.COVERED
            )

    ###########################################################################

    def get_time(
            self
    ) -> Stopwatch.Time_tuple_t:  # TODO
        if self._time is None:
            raise ValueError("time is not set")
        return self._time

    def get_data(
            self
    ) -> here.Field_t:  # TODO
        return self._field.outer

    def get_state(
            self
    ) -> here.Minesweeper_state:
        return self._state

    def lmb(
            self,
            position: here.Position_t
    ) -> None:
        self._click_wrapper(position, self._lmb)

    def rmb(
            self,
            position: here.Position_t
    ) -> None:
        self._click_wrapper(position, self._rmb)
