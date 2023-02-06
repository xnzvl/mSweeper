import tkinter as tk
from typing import Optional, Tuple, Dict, List

import main
import minesweeper as ms

import uber as u


WINDOW_TITLE = ":: mSweeper _"
WINDOW_PREFIXES = {
    ms.UNINITIALIZED: "",
    ms.PLAYING:       "Game in progress - ",
    ms.GAME_LOST:     "Game lost - ",
    ms.GAME_WON:      "Game won! - "
}

CONTEXT_MAIN_MENU = 0
CONTEXT_SWEEPER = 1
CONTEXT_SWEEPER_HS = 2
CONTEXT_HIGHSCORES = 3
CONTEXT_HELP = 4

CELL_SIZE = 40
GAP_SIZE = 25
DEFAULT_MARGIN = 25

MARGINS: Dict[str, int] = {
    "top":    DEFAULT_MARGIN,
    "right":  DEFAULT_MARGIN,
    "bottom": DEFAULT_MARGIN,
    "left":   DEFAULT_MARGIN
}

COLOUR_RED = "#ff0839"
COLOUR_BLACK = "#000000"
COLOUR_FLAG = COLOUR_RED
COLOUR_BAD_FLAG = "#633840"

NUM_FONT = ('system', 16)
NUM_COLOUR = COLOUR_BLACK

DEFAULT_DICT_KEY = -1

COLOUR_CELLS: Dict[u.mCell_state_t, Dict[u.mCell_value_t, Tuple[str, str]]] = {
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
        ms.MINE: (COLOUR_RED, "#ffffff")
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

SIGN_A = CELL_SIZE // 13
assert CELL_SIZE % 13 == 1

SHAPE_MINE: List[int] = []
SHAPE_FLAG: List[int] = []
SHAPE_STAND: List[int] = []


def from_template(
    shape: List[int],
    template: List[int],
    x: int,
    y: int
) -> None:
    even = True

    shape.append(x)
    shape.append(y)

    for coord in template:
        x += coord if even else 0
        y += coord if not even else 0

        shape.append(x)
        shape.append(y)

        even = not even


def init_shapes() -> None:
    mine_template: List[int] = [
        1, 2, 3, -1, -1, 3, 2, 1, -2, 3, 1, -1, -3, 2,
        -1, -2, -3, 1, 1, -3, -2, -1, 2, -3, -1, 1, 3
    ]
    flag_template: List[int] = [
        1, 1, 3, -1, 1, 5, -1, 1, -3, -1, -1, -5
    ]
    stand_template: List[int] = [
        3, -1, 1, 1, 3, 1, -3, 6, 1, 1, -3, -1, 1, -6, -3
    ]

    from_template(SHAPE_MINE, mine_template, 4, 0)
    from_template(SHAPE_FLAG, flag_template, 2, 1)
    from_template(SHAPE_STAND, stand_template, 1, 1)


class Gui:
    def __init__(
        self,
        session: main.Session,
        is_interactive: bool
    ) -> None:
        init_shapes()

        self.session = session
        self.is_interactive = is_interactive

        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        self.root.bind_all("q", lambda _: self.root.destroy())

        self.change_context(CONTEXT_MAIN_MENU)
        self.root.mainloop()

    def change_context(
        self,
        new_context: u.mContext_t
    ) -> None:
        if new_context == CONTEXT_MAIN_MENU:
            pass
        elif new_context == CONTEXT_MAIN_MENU:
            C_minesweeper(self)
        elif new_context == CONTEXT_HIGHSCORES:
            pass


class Context:
    def __init__(
        self,
        gui_root: Gui,
        width: int,
        height: int
    ) -> None:
        self.gui_root = gui_root
        self.session = gui_root.session
        self.press_position: Optional[u.mPosition_t] = 0, 0

        self.canvas = tk.Canvas(width=width, height=height)
        self.canvas.pack()

    def quit_context_for(
        self,
        new_context: u.mContext_t
    ) -> None:
        self.canvas.destroy()
        self.gui_root.change_context(new_context)


class C_minesweeper(Context):
    def __init__(
        self,
        gui_root: Gui
    ) -> None:
        self.deets = gui_root.session.deets
        self.root = gui_root.root

        super().__init__(
            gui_root,
            self.deets["width"] * CELL_SIZE + MARGINS["left"]
                                            + MARGINS["right"],
            self.deets["width"] * CELL_SIZE + MARGINS["top"]
                                            + MARGINS["bottom"]
        )

        self.reset()

    def draw_cell(
        self,
        cell: u.mCell_t,
        cx: int,
        cy: int
    ) -> None:
        def get_colours(
            state: u.mCell_state_t,
            value: u.mCell_value_t
        ) -> Tuple[str, str]:
            colours = COLOUR_CELLS[state].get(value)

            if colours is None:
                colours = COLOUR_CELLS[state][DEFAULT_DICT_KEY]

            return colours

        def adapt_coords(
            template: List[int]
        ) -> List[int]:
            adapted_coords: List[int] = []
            for i, coord in enumerate(template):
                adapted_coords.append(coord * SIGN_A + 2 * SIGN_A + 1 +
                                      (cx if i % 2 == 0 else cy))
            return adapted_coords

        def draw_flag() -> None:
            ms_state = self.session.ms_state
            flag_colour = COLOUR_FLAG \
                if (ms_state != ms.GAME_WON and ms_state != ms.GAME_LOST) or \
                value == ms.MINE \
                else COLOUR_BAD_FLAG

            self.canvas.create_polygon(
                adapt_coords(SHAPE_STAND),
                fill=COLOUR_BLACK,
                state="disabled"
            )

            self.canvas.create_polygon(
                adapt_coords(SHAPE_FLAG),
                fill=flag_colour,
                state="disabled"
            )

        def draw_mine() -> None:
            self.canvas.create_polygon(
                adapt_coords(SHAPE_MINE),
                fill=COLOUR_BLACK,
                state="disabled"
            )

            self.canvas.create_rectangle(
                cx + 5 * SIGN_A, cy + 5 * SIGN_A,
                cx + 6 * SIGN_A + 1, cy + 6 * SIGN_A + 1,
                fill="#ffffff",
                state="disabled"
            )

        state, value = ms.get_cell_state(cell), ms.get_cell_value(cell)
        main_clr, active_clr = get_colours(state, value)

        self.canvas.create_rectangle(
            cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
            fill=main_clr,
            activefill=active_clr
        )

        if state == ms.FLAG:
            draw_flag()
        elif value == ms.MINE:
            draw_mine()
        elif value == 0 or state == ms.COVERED:
            return
        else:
            self.canvas.create_text(
                cx + CELL_SIZE // 2, cy + CELL_SIZE // 2,
                text=str(value),
                font=NUM_FONT,
                state="disabled"
            )

    def refresh(
        self
    ) -> None:
        ms_state = self.session.ms.get_state()
        self.root.title(WINDOW_PREFIXES[ms_state] + WINDOW_TITLE)

        self.canvas.delete(tk.ALL)
        for y, row in enumerate(self.ms_data):
            for x, cell in enumerate(row):
                cy = y * CELL_SIZE + MARGINS["top"] + 1
                cx = x * CELL_SIZE + MARGINS["left"] + 1

                self.draw_cell(cell, cx, cy)

    def reset(
        self
    ) -> None:  # reset()/init()
        self.session.get_new_ms()

        assert self.session.ms is not None
        self.ms_data: u.mMinesweeper_t = self.session.ms.get_data()

        if self.gui_root.is_interactive:
            self.bind_actions()

        self.refresh()

    def bind_actions(
        self
    ) -> None:
        self.canvas.bind_all("r", lambda _: self.reset())

        self.canvas.bind(
            "<Button-1>",
            lambda event: self.click(self.session.ms_lmb, event)
        )

        self.canvas.bind(
            "<Button-3>",
            lambda event: self.click(self.session.ms_rmb, event)
        )

    def get_position(
        self,
        x: int,
        y: int
    ) -> Optional[u.mPosition_t]:
        x_pos = (x - MARGINS["left"] - 1) // CELL_SIZE
        y_pos = (y - MARGINS["top"] - 1) // CELL_SIZE

        return (x_pos, y_pos) \
            if 0 <= x_pos < self.deets["width"] \
            and 0 <= y_pos < self.deets["height"] \
            else None

    def click(
        self,
        click_fun: u.mClick_t,
        event: tk.Event  # type: ignore
    ) -> None:
        position = self.get_position(event.x, event.y)

        if position is None:
            return

        click_fun(position)
        self.refresh()
