import tkinter as tk
from typing import Callable, Optional, Tuple, Dict, List

import main
import minesweeper as ms

import uber as u


Context_t = int
Quit_context_lambda = Callable[[tk.Event], None]


SW_TITLE = ":: mSweeper _"
SW_VERSION = "1.30"
WINDOW_PREFIXES = {
    ms.UNINITIALIZED: "",
    ms.PLAYING:       "Game in progress - ",
    ms.GAME_LOST:     "Game lost - ",
    ms.GAME_WON:      "Game won! - "
}

CONTEXT_MAIN_MENU = 0
CONTEXT_SWEEPER = 1
CONTEXT_HIGHSCORES = 2
CONTEXT_HELP = 3

BOX_A = 90
CELL_SIZE = 40
GAP_SIZE = 30
DEFAULT_MARGIN = 25

ICON_PARTS = 13
ICON_INDENT = 1  # from one side
assert CELL_SIZE % ICON_PARTS == 1

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
COLOUR_OUTLINE = "#000000"

DEFAULT_DICT_KEY = -1
DISPOSABLE = "disposable"

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

DEF_FONT = "System"
DEF_FONT_SIZE = 28
NUM_COLOUR = COLOUR_BLACK

TEMPLATE: Dict[str, Tuple[Tuple[int, int], List[int]]] = {
    "mine":        ((6, 2), [1, 2, 3, -1, -1, 3, 2, 1, -2, 3, 1, -1, -3, 2,
                             -1, -2, -3, 1, 1, -3, -2, -1, 2, -3, -1, 1, 3]
                    ),
    "flag":        ((4, 3), [1, 1, 3, -1, 1, 5, -1, 1, -3, -1, -1, -5]),
    "stand":       ((3, 3), [3, -1, 1, 1, 3, 1, -3, 6, 1, 1, -3, -1, 1, -6, -3]
                    ),
    "trophy_body": ((4, 3), [5, 1, 1, 1, -1, 2, -1, 1, -1, 2, 2, 1, -5, -1, 2,
                             -2, -1, -1, -1, -2, -1, -1, 1]
                    ),
    "trophy_ears": ((2, 2), [2, 1, 5, -1, 2, 2, -1, -1, -7, 1, -1]),
    "smile":       ((2, 7), [2, 1, 5, -1, 2, 2, -2, 1, -5, -1, -2])
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
    ms_state: u.mSweeper_state_t
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

        self.max_width = main.DIFFICULTY_DICT[u.HARD]["width"] * CELL_SIZE \
            + self.hor_margin
        self.max_height = main.DIFFICULTY_DICT[u.HARD]["height"] * CELL_SIZE \
            + self.ver_margin + GAP_SIZE + BOX_A

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
                self.max_width,
                self.max_height
            )
        elif new_context == CONTEXT_SWEEPER:
            C_minesweeper(
                self,
                self.session.deets["width"] * CELL_SIZE + self.hor_margin,
                self.session.deets["height"] * CELL_SIZE + self.ver_margin
                + GAP_SIZE + BOX_A
            )
        elif new_context == CONTEXT_HIGHSCORES:
            C_highscores(
                self,
                self.max_width,
                self.max_height
            )
        elif new_context == CONTEXT_HELP:
            assert False, "WIP"
            C_help(self, 1, 1)  # TODO


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
        self.width = width
        self.height = height

        self.canvas = tk.Canvas(
            width=width - 2, height=height - 2,  # to fix symmetry
            background=COLOUR_BACKGROUND
        )
        self.canvas.pack()

        self.q_to_main_menu: Quit_context_lambda = \
            lambda _: self.quit_context_for(CONTEXT_MAIN_MENU)
        self.q_to_sweeper: Quit_context_lambda = \
            lambda _: self.quit_context_for(CONTEXT_SWEEPER)
        self.q_to_highscores: Quit_context_lambda = \
            lambda _: self.quit_context_for(CONTEXT_HIGHSCORES)
        self.q_to_help: Quit_context_lambda = \
            lambda _: self.quit_context_for(CONTEXT_HELP)

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
        def draw_title(
            y: int
        ) -> int:
            self.canvas.create_text(
                MARGINS["left"] + GAP_SIZE, y,
                anchor="sw",
                fill=COLOUR_FONT,
                font=(DEF_FONT, 64),
                text=SW_TITLE
            )
            return 0

        def draw_header(
            y: int
        ) -> int:
            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    MARGINS["left"] + header_b_width + GAP_SIZE, y,
                    MARGINS["left"] + header_b_width * 2 + GAP_SIZE, y + BOX_A,
                    activeoutline="red",
                    activewidth=3,
                    fill=COLOUR_BACKGROUND
                ),
                "<Button-1>",
                self.q_to_highscores
            )

            draw_trophy(
                self.canvas,
                MARGINS["left"] + header_b_width + GAP_SIZE, y,
                BOX_A
            )

            self.canvas.create_text(
                MARGINS["left"] + header_b_width + GAP_SIZE + BOX_A,
                y + BOX_A // 2,
                anchor="w",
                fill=COLOUR_FONT,
                font=(DEF_FONT, DEF_FONT_SIZE),
                state="disabled",
                text="Highscores"
            )

            return BOX_A

        def draw_diffs(
            y: int
        ) -> int:
            def create_ctext(
                x_anchor: int,
                y_delta: int,
                font_size: int,
                text: str
            ) -> None:
                self.canvas.create_text(
                    x_anchor + diff_b_a // 2,
                    y + diff_b_a // 2 + y_delta,
                    fill=COLOUR_FONT,
                    font=(DEF_FONT, font_size),
                    state="disabled",
                    text=text
                )

            e = "=="

            for i, (diff, diff_str) in enumerate([
                (u.EASY, "EASY"),
                (u.MEDIUM, "MEDIUM"),
                (u.HARD, "HARD")
            ]):
                tmp_x_anchor = MARGINS["left"] + diff_b_a * i + GAP_SIZE * i
                diff_dict = main.DIFFICULTY_DICT[diff]

                self.canvas.tag_bind(
                    self.canvas.create_rectangle(
                        tmp_x_anchor, y,
                        tmp_x_anchor + diff_b_a, y + diff_b_a,
                        fill=COLOUR_BACKGROUND,
                        outline=COLOUR_BLACK,
                        activeoutline="#ff0000",
                        activewidth=3,
                        tags=diff_str
                    ),
                    "<Button-1>",
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

            return diff_b_a

        def draw_footer(
            y: int
        ) -> int:
            qm_box_a = round(BOX_A * (2 / 3))

            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    MARGINS["left"], y,
                    MARGINS["left"] + qm_box_a, y + qm_box_a,
                    activeoutline="red",
                    fill=COLOUR_BACKGROUND
                ),
                "<Button-1>",
                self.q_to_help
            )

            self.canvas.create_text(
                MARGINS["left"] + qm_box_a / 2, y + qm_box_a / 2,
                fill="#484848",
                font=(DEF_FONT, 22),
                state="disabled",
                text="?"
            )

            self.canvas.create_text(
                width - MARGINS["right"] - GAP_SIZE, height,
                anchor="se",
                fill="#484848",
                font=(DEF_FONT, 15),
                state="disabled",
                text="v" + SW_VERSION
            )

            return qm_box_a

        super().__init__(gui_root, width, height)

        header_b_width = (width - self.gui_root.hor_margin - GAP_SIZE) // 2
        diff_b_a = (width - self.gui_root.hor_margin - 2 * GAP_SIZE) // 3

        y_anchor = height - (3 * GAP_SIZE + 2 * BOX_A + diff_b_a)
        y_anchor += draw_title(y_anchor) + GAP_SIZE
        y_anchor += draw_header(y_anchor) + GAP_SIZE
        y_anchor += draw_diffs(y_anchor) + GAP_SIZE
        y_anchor += draw_footer(y_anchor)

        if y_anchor > height - MARGINS["bottom"]:
            raise ValueError("Content out of bounds (margins)")

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

        self.width = width
        self.height = height

        self.reset()

    def draw_cell(
        self,
        cell: u.mCell_t,
        x: int,
        y: int
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
            x, y, x + CELL_SIZE, y + CELL_SIZE,
            fill=main_clr,
            activefill=active_clr
        )

        if state == ms.FLAG:
            draw_flag(
                self.canvas, x, y, CELL_SIZE,
                value == ms.MINE
                or self.session.ms_state == ms.UNINITIALIZED
                or self.session.ms_state == ms.PLAYING
            )
        elif value == ms.MINE:
            draw_mine(self.canvas, x, y, CELL_SIZE)
        elif value == 0 or state == ms.COVERED:
            return
        else:
            self.canvas.create_text(
                x + CELL_SIZE // 2, y + CELL_SIZE // 2,
                font=(DEF_FONT, 16),
                state="disabled",
                text=str(value)
            )

    def refresh(
        self
    ) -> None:
        def draw_deets() -> None:
            width = effective_width - GAP_SIZE - BOX_A \
                if special_case else b_width
            flag_str = f"{self.session.ms.flags:0>2d}" + (
                f" / {self.session.ms.mines}" if not special_case else ""
            )

            self.canvas.create_rectangle(
                MARGINS["left"], MARGINS["top"],
                MARGINS["left"] + width, MARGINS["top"] + BOX_A,
                fill=COLOUR_BACKGROUND,
                activeoutline="red"
            )

            self.canvas.create_text(
                MARGINS["left"] + GAP_SIZE // 2 + BOX_A,
                MARGINS["top"] + BOX_A // 2,
                anchor="w",
                font=(DEF_FONT, DEF_FONT_SIZE),
                state="disabled",
                text=flag_str
            )

            draw_flag(
                self.canvas,
                MARGINS["left"], MARGINS["top"], BOX_A,
                True, True
            )

        def draw_observer() -> None:
            if special_case:
                return

            x_anchor = b_width + MARGINS["left"] + GAP_SIZE
            face = self.canvas.create_rectangle(
                x_anchor, MARGINS["top"],
                x_anchor + BOX_A, MARGINS["top"] + BOX_A,
                fill=COLOUR_BACKGROUND,
                activeoutline="red"
            )
            self.canvas.tag_bind(face, "<Button-1>", lambda _: self.reset())

            if ms_state == ms.UNINITIALIZED:
                draw_mine(
                    self.canvas, x_anchor, MARGINS["top"], BOX_A, True
                )
            else:
                if self.session.top_ten:
                    draw_trophy(self.canvas, x_anchor, MARGINS["top"], BOX_A)
                else:
                    draw_face(
                        self.canvas, x_anchor, MARGINS["top"], BOX_A, ms_state
                    )

        def draw_menu_button() -> None:
            menu_width = BOX_A if special_case else b_width
            x_anchor = self.width - MARGINS["right"] - menu_width

            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    x_anchor, MARGINS["top"],
                    self.width - MARGINS["right"], MARGINS["top"] + BOX_A,
                    fill=COLOUR_BACKGROUND,
                    activeoutline="red"
                ),
                "<Button-1>", self.q_to_main_menu
            )

            if not special_case:
                self.canvas.create_text(
                    x_anchor + BOX_A, MARGINS["top"] + BOX_A // 2,
                    anchor="w",
                    font=(DEF_FONT, DEF_FONT_SIZE),
                    state="disabled",
                    text="Menu"
                )

            draw_menu_sign(self.canvas, x_anchor, MARGINS["top"], BOX_A)

        ms_state = self.session.ms.get_state()
        effective_width = self.width - self.gui_root.hor_margin
        special_case = self.session.difficulty == u.EASY
        b_width = (effective_width - 2 * GAP_SIZE - BOX_A) // 2

        self.canvas.delete(tk.ALL)  # TODO
        self.root.title(WINDOW_PREFIXES[ms_state] + SW_TITLE)

        draw_deets()
        draw_observer()
        draw_menu_button()

        for y, row in enumerate(self.ms_data):
            for x, cell in enumerate(row):
                cx = x * CELL_SIZE + MARGINS["left"]
                cy = y * CELL_SIZE + MARGINS["top"] + GAP_SIZE + BOX_A

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
        y_pos = (y - MARGINS["top"] - GAP_SIZE - BOX_A - 1) // CELL_SIZE

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
    def __init__(
        self,
        gui_root: Gui,
        width: int,
        height: int
    ) -> None:
        super().__init__(gui_root, width, height)

        self.subheader_h = 60
        self.rows_gap = 5

        self.row_y_anchor = MARGINS["top"] + BOX_A + GAP_SIZE + self.subheader_h + GAP_SIZE // 2 - self.rows_gap
        self.row_w = self.width - self.gui_root.hor_margin
        self.row_h = (self.height - self.row_y_anchor - MARGINS["bottom"]) // 10

        self.init_draw()

    def change_shown_diff(
            self,
            difficulty: u.Difficulty
    ) -> None:

        def text(
                row: int,
                txt: str,
                x: int,
                anchor: str = "w"
        ) -> None:
            self.canvas.create_text(
                x, self.row_y_anchor + row * self.row_h + (self.row_h - self.rows_gap) * 0.5 + self.rows_gap,
                anchor=anchor,
                fill="white",
                font=(DEF_FONT, record_font_size),
                state="disabled",
                tags=DISPOSABLE,
                text=txt
            )

        def draw_time(
                row: int,
                time: Optional[u.mTime_tuple_t]
        ) -> None:
            if time is not None:
                h, m, s, _ = time
                time_str = "{:02d}:{:02d}:{:02d}".format(h, m, s)
            else:
                time_str = "##:##:##"

            text(
                row,
                time_str,
                MARGINS["left"] + 4 * GAP_SIZE
            )

        def draw_nick(
                row: int,
                nick: Optional[str]
        ) -> None:
            text(
                row,
                nick if nick is not None else "< BLANK >",
                MARGINS["left"] + GAP_SIZE + 250
            )

        def draw_date(
                row: int,
                date: Optional[str]
        ) -> None:
            text(
                row,
                date if date is not None else "####-##-##",
                self.width - MARGINS["right"] - 2 * GAP_SIZE,
                "e"
            )

        record_font_size = 16
        self.canvas.delete(DISPOSABLE)
        diff_records = self.session.hs_manager.get_diff_scores(difficulty)

        for i in range(10):
            text(
                i,
                f"{i + 1}.",
                MARGINS["left"] + GAP_SIZE
            )

            time, date, nick = (None, None, None) \
                if i >= len(diff_records) \
                else diff_records[i]

            draw_time(i, time)
            draw_nick(i, nick)
            draw_date(i, date)

    def init_draw(
        self
    ) -> None:
        self.canvas.tag_bind(
            self.canvas.create_rectangle(
                self.width - BOX_A - MARGINS["right"], MARGINS["top"],
                self.width - MARGINS["right"], MARGINS["top"] + BOX_A,
                fill=COLOUR_BACKGROUND,
                activeoutline="red",
                activewidth=3
            ),
            "<Button-1>",
            self.q_to_main_menu
        )

        draw_menu_sign(
            self.canvas,
            self.width - BOX_A - MARGINS["right"], MARGINS["top"],
            BOX_A
        )

        self.canvas.create_rectangle(
            MARGINS["right"], MARGINS["top"],
            MARGINS["right"] + BOX_A, MARGINS["top"] + BOX_A
        )

        draw_trophy(
            self.canvas,
            MARGINS["left"], MARGINS["top"],
            BOX_A
        )

        x_anchor = MARGINS["left"] + BOX_A + GAP_SIZE
        diff_b = (self.width - 4 * GAP_SIZE - 2 * BOX_A -
                  self.gui_root.hor_margin) // 3

        for i, diff_enum in enumerate(
            [u.Difficulty.EASY, u.Difficulty.MEDIUM, u.Difficulty.HARD]
        ):
            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    x_anchor + i * (diff_b + GAP_SIZE),
                    MARGINS["top"],
                    x_anchor + (i + 1) * diff_b + i * GAP_SIZE,
                    MARGINS["top"] + BOX_A,
                    fill=COLOUR_BACKGROUND,
                    activeoutline="red",
                    activewidth=3
                ),
                "<Button-1>",
                lambda _, d=diff_enum: self.change_shown_diff(d)
            )

            self.canvas.create_text(
                x_anchor + i * (diff_b + GAP_SIZE) + diff_b // 2,
                MARGINS["top"] + BOX_A // 2,
                fill="white",
                font=(DEF_FONT, DEF_FONT_SIZE),
                state="disabled",
                text=str(diff_enum).split('.')[-1]
            )

        self.canvas.create_rectangle(
            MARGINS["left"],
            MARGINS["top"] + BOX_A + GAP_SIZE,
            self.width - MARGINS["right"],
            MARGINS["top"] + BOX_A + GAP_SIZE + self.subheader_h
        )

        self.canvas.create_text(
            MARGINS["left"] + GAP_SIZE,
            MARGINS["top"] + BOX_A + GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(DEF_FONT, DEF_FONT_SIZE),
            text="#"
        )

        self.canvas.create_text(
            MARGINS["left"] + 4 * GAP_SIZE,
            MARGINS["top"] + BOX_A + GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(DEF_FONT, DEF_FONT_SIZE),
            text="Time"
        )

        self.canvas.create_text(
            MARGINS["left"] + GAP_SIZE + 250,
            MARGINS["top"] + BOX_A + GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(DEF_FONT, DEF_FONT_SIZE),
            text="Nickname"
        )

        self.canvas.create_text(
            self.width - MARGINS["right"] - 5 * GAP_SIZE,
            MARGINS["top"] + BOX_A + GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(DEF_FONT, DEF_FONT_SIZE),
            text="Date"
        )

        for i in range(10):
            self.canvas.create_rectangle(
                MARGINS["left"],
                self.row_y_anchor + i * self.row_h + self.rows_gap,
                MARGINS["left"] + self.row_w,
                self.row_y_anchor + (i + 1) * self.row_h,
                activeoutline="red",
                fill=COLOUR_BACKGROUND
            )


class C_help(Context):
    pass
