import tkinter as tk
from typing import Optional, Tuple, Dict, List

import main
import minesweeper as ms

import uber as u


SW_TITLE = ":: mSweeper _"
SW_VERSION = "1.10"
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

BOX_HEIGTH = 90
CELL_SIZE = 40
SIGN_A = CELL_SIZE // 13
assert CELL_SIZE % 13 == 1
GAP_SIZE = 30
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
COLOUR_BACKGROUND = "#202020"
COLOUR_FONT = "#ffffff"

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

FONT = "System"
NUM_COLOUR = COLOUR_BLACK

TEMPLATE: Dict[str, Tuple[Tuple[int, int], List[int]]] = {
    "mine":        ((4, 0), [1, 2, 3, -1, -1, 3, 2, 1, -2, 3, 1, -1, -3, 2,
                             -1, -2, -3, 1, 1, -3, -2, -1, 2, -3, -1, 1, 3]
                    ),
    "flag":        ((2, 1), [1, 1, 3, -1, 1, 5, -1, 1, -3, -1, -1, -5]),
    "stand":       ((1, 1), [3, -1, 1, 1, 3, 1, -3, 6, 1, 1, -3, -1, 1,
                             -6, -3]
                    ),
    "trophy_body": ((2, 1), [5, 1, 1, 1, -1, 2, -1, 1, -1, 2, 2, 1, -5, -1, 2,
                             -2, -1, -1, -1, -2, -1, -1, 1]
                    ),
    "trophy_ears": ((0, 0), [2, 1, 5, -1, 2, 2, -1, -1, -7, 1, -1])
}

SHAPE: Dict[str, List[int]] = {}


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
    template: List[int]
) -> List[int]:
    adapted_coords: List[int] = []

    for i, coord in enumerate(template):
        adapted_coords.append(
            coord * side + 2 * side + 1 + (x if i % 2 == 0 else y)
        )

    return adapted_coords


def draw_mine(
    canvas: tk.Canvas,
    x: int,
    y: int,
    side: int
) -> None:
    canvas.create_polygon(
        adapt_coords(x, y, side, SHAPE["mine"]),
        fill=COLOUR_BLACK,
        state="disabled"
    )

    canvas.create_rectangle(
        x + 5 * side, y + 5 * side,
        x + 6 * side + 1, y + 6 * side + 1,
        fill="#ffffff",
        state="disabled"
    )


def draw_flag(
    canvas: tk.Canvas,
    x: int,
    y: int,
    side: int,
    is_default_flag: bool
) -> None:
    canvas.create_polygon(
        adapt_coords(x, y, side, SHAPE["stand"]),
        fill=COLOUR_BLACK,
        state="disabled"
    )

    canvas.create_polygon(
        adapt_coords(x, y, side, SHAPE["flag"]),
        fill=COLOUR_FLAG if is_default_flag else COLOUR_BAD_FLAG,
        state="disabled"
    )


def draw_trophy(
    canvas: tk.Canvas,
    x: int,
    y: int,
    side: int
) -> None:
    for shape in ["trophy_body", "trophy_ears"]:
        canvas.create_polygon(
            adapt_coords(x, y, side, SHAPE[shape]),
            fill=COLOUR_BLACK,
            state="disabled"
        )

    canvas.create_rectangle(
        x + 5 * side, y + 4 * side, x + 6 * side, y + 5 * side,
        fill="#ffffff",
        state="disabled"
    )


def draw_menu_sign() -> None:
    pass


class Gui:
    def __init__(
        self,
        session: main.Session,
        is_interactive: bool
    ) -> None:
        init_shapes()

        self.session = session
        self.is_interactive = is_interactive

        self.hor_margin = MARGINS["left"] + MARGINS["right"]
        self.ver_margin = MARGINS["top"] + MARGINS["bottom"]

        self.root = tk.Tk()
        self.root.title(SW_TITLE)
        self.root.resizable(False, False)
        self.root.bind_all("q", lambda _: self.root.destroy())

        self.change_context(CONTEXT_MAIN_MENU)
        self.root.mainloop()

    def change_context(
        self,
        new_context: u.mContext_t
    ) -> None:
        if new_context == CONTEXT_MAIN_MENU:
            C_main_menu(
                self,
                main.DIFFICULTY_DICT[u.HARD]["width"] * CELL_SIZE
                + self.hor_margin,
                main.DIFFICULTY_DICT[u.HARD]["height"] * CELL_SIZE
                + self.ver_margin
            )
        elif new_context == CONTEXT_SWEEPER:
            C_minesweeper(
                self,
                self.session.deets["width"] * CELL_SIZE + self.hor_margin,
                self.session.deets["height"] * CELL_SIZE + self.ver_margin
            )
        elif new_context == CONTEXT_HIGHSCORES:
            C_highscores(self, 1, 1)


class Context:
    def __init__(
        self,
        gui_root: Gui,
        width: int,
        height: int
    ) -> None:
        self.root = gui_root.root
        self.gui_root = gui_root
        self.session = gui_root.session

        self.canvas = tk.Canvas(
            width=width, height=height,
            background=COLOUR_BACKGROUND
        )
        self.canvas.pack()

    def quit_context_for(
        self,
        new_context: u.mContext_t
    ) -> None:
        self.canvas.destroy()
        self.gui_root.change_context(new_context)


class C_main_menu(Context):
    def __init__(
        self,
        gui_root: Gui,
        width: int,
        height: int
    ) -> None:
        def draw_title() -> None:
            self.canvas.create_text(
                MARGINS["left"] + GAP_SIZE,
                (height - 3 * GAP_SIZE - BOX_HEIGTH - d_a) // 2 + 10,
                anchor="sw",
                fill=COLOUR_FONT,
                font=(FONT, 30),
                text=SW_TITLE
            )

        def draw_header() -> None:
            for i, tag in enumerate(["tbox_nick", "b_highscores"]):
                self.canvas.create_rectangle(
                    MARGINS["left"] + b_a * i + GAP_SIZE * i,
                    butts_anchor,
                    MARGINS["left"] + b_a * (i + 1) + GAP_SIZE * i,
                    butts_anchor + BOX_HEIGTH,
                    activefill="#404040",
                    tags=tag
                )

            trophy_box_a = BOX_HEIGTH // 15

            draw_trophy(
                self.canvas,
                MARGINS["left"] + b_a + GAP_SIZE + trophy_box_a,
                butts_anchor + trophy_box_a,
                BOX_HEIGTH // 15
            )

            self.canvas.create_text(
                MARGINS["left"] + b_a + GAP_SIZE + BOX_HEIGTH,
                butts_anchor + BOX_HEIGTH // 2,
                anchor="w",
                fill=COLOUR_FONT,
                font=(FONT, buttons_font_size),
                state="disabled",
                text="Highscores"
            )

        def draw_diffs() -> None:
            def create_ctext(
                x_anchor: int,
                y_delta: int,
                font_size: int,
                text: str
            ) -> None:
                self.canvas.create_text(
                    x_anchor + d_a // 2, diffbox_anchor + d_a // 2 + y_delta,
                    fill=COLOUR_FONT,
                    font=(FONT, font_size),
                    state="disabled",
                    text=text
                )

            e = "=="

            for i, (diff, diff_str) in enumerate([
                (u.EASY, "EASY"),
                (u.MEDIUM, "MEDIUM"),
                (u.HARD, "HARD")
            ]):
                tmp_x_anchor = MARGINS["left"] + d_a * i + GAP_SIZE * i
                diff_dict = main.DIFFICULTY_DICT[diff]

                button = self.canvas.create_rectangle(
                    tmp_x_anchor, diffbox_anchor,
                    tmp_x_anchor + d_a, diffbox_anchor + d_a,
                    fill=COLOUR_BACKGROUND,
                    outline=COLOUR_BLACK,
                    activeoutline="#ff0000",
                    activewidth=3,
                    tags=diff_str
                )

                self.canvas.tag_bind(
                    button, "<Button-1>",
                    lambda _, d=diff: self.set_diff_and_quit(d)
                )

                create_ctext(
                    tmp_x_anchor, -80, 28,
                    f'{e * 2} {diff_str} {e * 2}'
                )
                create_ctext(
                    tmp_x_anchor, 0, 42,
                    f'{diff_dict["width"]} x {diff_dict["height"]}'
                )
                create_ctext(
                    tmp_x_anchor, 80, 28,
                    f'{e} mines: {diff_dict["mines"]} {e}'
                )

        def draw_footer() -> None:
            self.canvas.create_text(
                width - MARGINS["right"] - GAP_SIZE, height - GAP_SIZE,
                anchor="se",
                fill="#484848",
                font=(FONT, 15),
                text="v" + SW_VERSION
            )

        super().__init__(gui_root, width, height)

        buttons_font_size = 24
        b_a = (width - self.gui_root.hor_margin - GAP_SIZE) // 2
        d_a = (width - self.gui_root.hor_margin - 2 * GAP_SIZE) // 3

        butts_anchor = (height - GAP_SIZE - d_a - BOX_HEIGTH) // 2
        diffbox_anchor = butts_anchor + GAP_SIZE + BOX_HEIGTH

        draw_title()
        draw_header()
        draw_diffs()
        draw_footer()

    def set_diff_and_quit(
        self,
        difficulty: u.mDifficulty_t
    ) -> None:
        self.session.set_difficulty(difficulty)
        self.quit_context_for(CONTEXT_SWEEPER)


class C_minesweeper(Context):
    def __init__(
        self,
        gui_root: Gui,
        width: int,
        height: int
    ) -> None:
        super().__init__(gui_root, width, height)

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

        state, value = ms.get_cell_state(cell), ms.get_cell_value(cell)
        main_clr, active_clr = get_colours(state, value)

        self.canvas.create_rectangle(
            cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
            fill=main_clr,
            activefill=active_clr
        )

        if state == ms.FLAG:
            draw_flag(
                self.canvas, cx, cy, SIGN_A,
                value == ms.MINE
                or self.session.ms_state == ms.UNINITIALIZED
                or self.session.ms_state == ms.PLAYING
            )
        elif value == ms.MINE:
            draw_mine(self.canvas, cx, cy, SIGN_A)
        elif value == 0 or state == ms.COVERED:
            return
        else:
            self.canvas.create_text(
                cx + CELL_SIZE // 2, cy + CELL_SIZE // 2,
                font=(FONT, 16),
                state="disabled",
                text=str(value)
            )

    def refresh(
        self
    ) -> None:
        ms_state = self.session.ms.get_state()
        self.root.title(WINDOW_PREFIXES[ms_state] + SW_TITLE)

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
            if 0 <= x_pos < self.session.deets["width"] \
            and 0 <= y_pos < self.session.deets["height"] \
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


class C_highscores(Context):
    pass
