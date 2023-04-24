from typing import List

import minesweeper as here


class Field:
    def __init__(
            self,
            dimensions: here.Dimensions_t
    ) -> None:
        width, height = dimensions

        self.field_pointer: List[here.Field_t] = []  # TODO

        self.inner: here.Field_t = [
            [here.COVERED for _ in range(width)] for _ in range(height)
        ]
        default_cell = here.COVERED | here.UNKNOWN
        self.outer: here.Field_t = [
            [default_cell for _ in range(width)] for _ in range(height)
        ]

    def get_inner_cell(
            self,
            x: int,
            y: int
    ) -> here.Cell_t:
        return self.inner[y][x]

    def get_inner_value(
            self,
            x: int,
            y: int
    ) -> here.Cell_value_t:
        return self.inner[y][x] & here.MINES_MASK

    def get_inner_state(
            self,
            x: int,
            y: int
    ) -> here.Cell_state_t:
        return self.inner[y][x] & here.STATE_MASK

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
            state: here.Cell_state_t
    ) -> None:
        self.inner[y][x] = (self.inner[y][x] & ~here.STATE_MASK) | state
        self.outer[y][x] = self.inner[y][x] \
            if state == here.SHOWN \
            else (state | here.UNKNOWN)

    def project_inner(
            self
    ) -> None:
        for y, row in enumerate(self.inner):
            for x, cell in enumerate(row):
                self.outer[y][x] = cell
