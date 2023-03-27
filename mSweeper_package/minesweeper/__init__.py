from enum import Enum


Cell_t = int
Cell_value_t = int
Cell_state_t = int


# Masks
MINES_MASK = 0b1111
STATE_MASK = 0b11_0000

# Constants for cell values
MINE = 0b1111
UNKNOWN = 0b1110

# Cell_state_t constants
COVERED, FLAG, SHOWN = 0b11_0000, 0b10_0000, 0b01_0000


class Sweeper_state_t(Enum):
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
