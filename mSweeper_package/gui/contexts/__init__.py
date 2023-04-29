from enum import Enum
from typing import Callable, Dict, List, Tuple
import tkinter as tk

from ... import gui
from ... import minesweeper as ms

from .Context_help import Context_help as C_help_alias
from .Context_highscores import Context_highscores as C_highscores_alias
from .Context_main_menu import Context_main_menu as C_main_menu_alias
from .Context_minesweeper import Context_minesweeper as C_minesweeper_alias


Context_help = C_help_alias
Context_highscores = C_highscores_alias
Context_main_menu = C_main_menu_alias
Context_minesweeper = C_minesweeper_alias


class Colour(Enum):
    BLACK = "#000000"
    RED = "#ff0839"
    WHITE = "#ffffff"

    FLAG = RED
    BAD_FLAG = "#633840"

    BACKGROUND = "#202020"

    FONT = WHITE
    NUMBER = BLACK

    OUTLINE = BLACK
    ACTIVE_OUTLINE = "#ff0000"


class Context(Enum):
    MAIN_MENU = "Main menu"
    MINESWEEPER = "Minesweeper"
    HIGHSCORES = "Highscore"
    HELP = "Help"


class Font_size(Enum):
    DEFAULT = 28


Position_t = Tuple[int, int]
Click_t = Callable[[Position_t], None]


WINDOW_PREFIXES = {
    ms.Minesweeper_state.UNINITIALIZED: "",
    ms.Minesweeper_state.PLAYING:       "Game in progress - ",
    ms.Minesweeper_state.GAME_LOST:     "Game lost - ",
    ms.Minesweeper_state.GAME_WON:      "Game won! - "
}

DISPOSABLE_FLAG = "disposable_flag"

FONT = "System"

BUTTON_HEIGHT = 90


ICON_PARTS = 13
ICON_INDENT = 1  # from one side
assert gui.CELL_SIZE % ICON_PARTS == 1


DEFAULT_DICT_KEY = -1
COLOUR_CELLS: Dict[ms.Cell_state_t, Dict[ms.Cell_value_t, Tuple[str, str]]] = {
    ms.SHOWN: {
        0:       ("#faf3e1", "#ffffff"),
        1:       ("#b4db81", "#ffffff"),
        2:       ("#dbd281", "#ffffff"),
        3:       ("#dbb381", "#ffffff"),
        4:       ("#db8f81", "#ffffff"),
        5:       ("#bf81db", "#ffffff"),
        6:       ("#a081db", "#ffffff"),
        7:       ("#8183db", "#ffffff"),
        8:       ("#595aa8", "#ffffff"),
        ms.MINE: (Colour.RED.value, "#ffffff")
    },
    ms.FLAG: {
        ms.MINE:          ("#a39676", "#ffffff"),
        ms.UNKNOWN:       ("#a39676", "#ffffff"),
        DEFAULT_DICT_KEY: ("#a67e6f", "#ffffff")
        # ^ misplaced flag ^
    },
    ms.COVERED: {
        ms.MINE:          ("#a39676", "#ffffff"),
        DEFAULT_DICT_KEY: ("#dbcead", "#ffffff")
    }
}


# UTILS

def adapt_coords(
        x: int,
        y: int,
        side: int,
        shape: List[int],
        flip_x: bool = False,
        flip_y: bool = False
) -> List[int]:
    even = True
    adapted_coords: List[int] = []

    x0 = (0 if not flip_x else ICON_PARTS * side) + x + 1
    y0 = (0 if not flip_y else ICON_PARTS * side) + y + 1

    for coord in shape:
        polarity = -1 if (even and flip_x) or (not even and flip_y) else 1
        adapted_coords.append(coord * side * polarity + (x0 if even else y0))

        even = not even

    return adapted_coords


def get_colours(
        cell: ms.Cell_t
) -> Tuple[str, str]:
    state = ms.get_cell_state(cell)
    value = ms.get_cell_value(cell)

    return COLOUR_CELLS[state].get(value, COLOUR_CELLS[state][DEFAULT_DICT_KEY])


# DRAWERS

def draw_mine(
        canvas: tk.Canvas,
        x: int,
        y: int,
        whole_side: int,
        indent: bool = False
) -> None:
    side = whole_side // (ICON_PARTS + (2 * ICON_INDENT if indent else 0))
    n_x, n_y = (x + side * ICON_INDENT, y + side * ICON_INDENT) \
        if indent else (x, y)

    canvas.create_polygon(
        adapt_coords(n_x, n_y, side, gui.SHAPE[gui.Shape.MINE]),
        fill=Colour.BLACK.value,
        state="disabled"
    )

    canvas.create_rectangle(
        n_x + 5 * side, n_y + 5 * side,
        n_x + 6 * side + 1, n_y + 6 * side + 1,
        fill="#ffffff",
        state="disabled"
    )


def draw_flag(
        canvas: tk.Canvas,
        x: int,
        y: int,
        whole_side: int,
        is_default_flag: bool,
        indent: bool = False
) -> None:
    side = whole_side // (ICON_PARTS + (2 * ICON_INDENT if indent else 0))
    n_x, n_y = (x + side * ICON_INDENT, y + side * ICON_INDENT) \
        if indent else (x, y)

    canvas.create_polygon(
        adapt_coords(n_x, n_y, side, gui.SHAPE[gui.Shape.STAND]),
        fill=Colour.BLACK.value,
        state="disabled"
    )

    canvas.create_polygon(
        adapt_coords(n_x, n_y, side, gui.SHAPE[gui.Shape.FLAG]),
        fill=(Colour.FLAG if is_default_flag else Colour.BAD_FLAG).value,
        state="disabled"
    )


def draw_trophy(
        canvas: tk.Canvas,
        x: int,
        y: int,
        whole_side: int
) -> None:
    side = whole_side // (ICON_PARTS + 2 * ICON_INDENT)
    n_x, n_y = x + side * ICON_INDENT, y + side * ICON_INDENT

    for shape in [gui.Shape.TROPHY_BODY, gui.Shape.TROPHY_EARS]:
        canvas.create_polygon(
            adapt_coords(n_x, n_y, side, gui.SHAPE[shape]),
            fill=Colour.BLACK.value,
            state="disabled"
        )

    canvas.create_rectangle(
        n_x + 5 * side, n_y + 4 * side, n_x + 6 * side, n_y + 5 * side,
        fill="#ffffff",
        state="disabled"
    )


def draw_menu_sign(
        canvas: tk.Canvas,
        x: int,
        y: int,
        whole_side: int
) -> None:
    side = whole_side // (ICON_PARTS + 2 * ICON_INDENT)
    n_x, n_y = x + side * ICON_INDENT, y + side * ICON_INDENT

    for i in range(3):
        canvas.create_rectangle(
            n_x + 3 * side + 1, n_y + (3 + i * 3) * side + 1,
            n_x + 10 * side, n_y + (4 + i * 3) * side,
            fill=Colour.BLACK.value,
            state="disabled"
        )


def draw_face(
        canvas: tk.Canvas,
        x: int,
        y: int,
        whole_side: int,
        ms_state: ms.Minesweeper_state
) -> None:
    side = whole_side // (ICON_PARTS + 2 * ICON_INDENT)
    n_x, n_y = x + side * ICON_INDENT, y + side * ICON_INDENT

    for i in [3, 8]:
        canvas.create_rectangle(
            n_x + i * side, n_y + 3 * side,
            n_x + (i + 2) * side, n_y + 6 * side,
            fill=Colour.BLACK.value, state="disabled"
        )

    if ms_state == ms.Minesweeper_state.PLAYING:
        canvas.create_rectangle(
            n_x + 2 * side, n_y + 8 * side,
            n_x + 11 * side, n_y + 10 * side,
            fill=Colour.BLACK.value, state="disabled"
        )
    else:
        canvas.create_polygon(
            adapt_coords(
                n_x, n_y if ms_state == ms.Minesweeper_state.GAME_WON else n_y + 4 * side,
                #    ^^ flip -> realign
                side, gui.SHAPE[gui.Shape.SMILE], flip_y=ms_state != ms.Minesweeper_state.GAME_WON
            ),
            fill=Colour.BLACK.value, state="disabled"
        )
