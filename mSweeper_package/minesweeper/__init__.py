from enum import Enum
from typing import Callable, List, Tuple

from .Minesweeper import Minesweeper as Minesweeper_alias


Minesweeper = Minesweeper_alias


Cell_t = int
# 0bXX XXXX             (cell)
#   ├┘ └──┴─ here.MINE-bits  (cell value)
#   └─────── state-bits (cell state)

Cell_value_t = int
Cell_state_t = int

Position_t = Tuple[int, int]
Dimensions_t = Tuple[int, int]

Field_t = List[List[Cell_t]]

Click_t = Callable[[Position_t], None]


# Masks
MINES_MASK = 0b1111
STATE_MASK = 0b11_0000

# Constants for cell values
MINE = 0b1111
UNKNOWN = 0b1110

# Cell_state_t constants
COVERED, FLAG, SHOWN = 0b11_0000, 0b10_0000, 0b01_0000


class Minesweeper_state(Enum):
    UNINITIALIZED = "UNINITIALIZED"
    PLAYING = "PLAYING"
    GAME_LOST = "GAME_LOST"
    GAME_WON = "GAME_WON"


def get_cell_value(
        cell: Cell_value_t
) -> int:
    return cell & MINES_MASK


def get_cell_state(
        cell: Cell_state_t
) -> Cell_state_t:
    return cell & STATE_MASK


def is_mine(
        cell: Cell_t
) -> bool:
    return (cell & MINES_MASK) == MINE
