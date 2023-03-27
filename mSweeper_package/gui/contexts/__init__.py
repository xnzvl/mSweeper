from enum import Enum
from typing import Dict, List, Tuple
import tkinter as tk

from ... import minesweeper as ms


class Colour_t(Enum):
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


class Context_t(Enum):
    MAIN_MENU = "Main menu"
    MINESWEEPER = "Minesweeper"
    HIGHSCORES = "Highscore"
    HELP = "Help"


class Font_size_t(Enum):
    DEFAULT = 28


class Shape_t(Enum):
    MINE = "mine_shape"
    FLAG = "flag_shape"
    STAND = "stand_shape"
    TROPHY_BODY = "trophy_body_shape"
    TROPHY_EARS = "trophy_ears_shape"
    SMILE = "smile_shape"


WINDOW_PREFIXES = {
    ms.Sweeper_state_t.UNINITIALIZED: "",
    ms.Sweeper_state_t.PLAYING:       "Game in progress - ",
    ms.Sweeper_state_t.GAME_LOST:     "Game lost - ",
    ms.Sweeper_state_t.GAME_WON:      "Game won! - "
}

DISPOSABLE_FLAG = "disposable_flag"

FONT = "System"

BUTTON_HEIGHT = 90
CELL_SIZE = 40
GAP_SIZE = 30

ICON_PARTS = 13
ICON_INDENT = 1  # from one side
assert CELL_SIZE % ICON_PARTS == 1

DEFAULT_MARGIN = 25
MARGINS: Dict[str, int] = {
    "top":    DEFAULT_MARGIN,
    "right":  DEFAULT_MARGIN,
    "bottom": DEFAULT_MARGIN,
    "left":   DEFAULT_MARGIN
}

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
        ms.MINE: (Colour_t.RED, "#ffffff")
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

SHAPE: Dict[Shape_t, List[int]] = {}
TEMPLATE: Dict[Shape_t, Tuple[Tuple[int, int], List[int]]] = {
    Shape_t.MINE:        ((6, 2), [1, 2, 3, -1, -1, 3, 2, 1, -2, 3, 1, -1, -3, 2, -1, -2, -3, 1, 1, -3, -2, -1, 2, -3, -1, 1, 3]),
    Shape_t.FLAG:        ((4, 3), [1, 1, 3, -1, 1, 5, -1, 1, -3, -1, -1, -5]),
    Shape_t.STAND:       ((3, 3), [3, -1, 1, 1, 3, 1, -3, 6, 1, 1, -3, -1, 1, -6, -3]),
    Shape_t.TROPHY_BODY: ((4, 3), [5, 1, 1, 1, -1, 2, -1, 1, -1, 2, 2, 1, -5, -1, 2, -2, -1, -1, -1, -2, -1, -1, 1]),
    Shape_t.TROPHY_EARS: ((2, 2), [2, 1, 5, -1, 2, 2, -1, -1, -7, 1, -1]),
    Shape_t.SMILE:       ((2, 7), [2, 1, 5, -1, 2, 2, -2, 1, -5, -1, -2])
}


# UTILS

def init_shapes() -> None:
    def from_template(
        template: List[int],
        x: int,
        y: int
    ) -> List[int]:
        even = True
        shape = []

        shape.append(x)
        shape.append(y)

        for coord in template:
            x += coord if even else 0
            y += coord if not even else 0

            shape.append(x)
            shape.append(y)

            even = not even

        return shape

    global TEMPLATE

    for shape, ((x0, y0), template) in TEMPLATE.items():
        SHAPE[shape] = from_template(template, x0, y0)

    del TEMPLATE


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


def get_colour(
        cell: ms.Cell_t
) -> Tuple[Colour_t, Colour_t]:
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
        adapt_coords(n_x, n_y, side, SHAPE["mine"]),
        fill=COLOUR_BLACK,
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
        adapt_coords(n_x, n_y, side, SHAPE["stand"]),
        fill=COLOUR_BLACK,
        state="disabled"
    )

    canvas.create_polygon(
        adapt_coords(n_x, n_y, side, SHAPE["flag"]),
        fill=COLOUR_FLAG if is_default_flag else COLOUR_BAD_FLAG,
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

    for shape in ["trophy_body", "trophy_ears"]:
        canvas.create_polygon(
            adapt_coords(n_x, n_y, side, SHAPE[shape]),
            fill=COLOUR_BLACK,
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
            fill=COLOUR_BLACK,
            state="disabled"
        )


def draw_face(
        canvas: tk.Canvas,
        x: int,
        y: int,
        whole_side: int,
        ms_state: ms.Sweeper_state_t
) -> None:
    side = whole_side // (ICON_PARTS + 2 * ICON_INDENT)
    n_x, n_y = x + side * ICON_INDENT, y + side * ICON_INDENT

    for i in [3, 8]:
        canvas.create_rectangle(
            n_x + i * side, n_y + 3 * side,
            n_x + (i + 2) * side, n_y + 6 * side,
            fill=COLOUR_BLACK, state="disabled"
        )

    if ms_state == ms.PLAYING:
        canvas.create_rectangle(
            n_x + 2 * side, n_y + 8 * side,
            n_x + 11 * side, n_y + 10 * side,
            fill=COLOUR_BLACK, state="disabled"
        )
    else:
        canvas.create_polygon(
            adapt_coords(
                n_x, n_y if ms_state == ms.GAME_WON else n_y + 4 * side,
                #    ^^ flip -> realign
                side, SHAPE["smile"], flip_y=ms_state != ms.GAME_WON
            ),
            fill=COLOUR_BLACK, state="disabled"
        )
