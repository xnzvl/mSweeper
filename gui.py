import tkinter as tk
from typing import Optional, Tuple, Dict

import main
import minesweeper as ms

import uber


Cell_t = uber.mCell_t
Cell_state_t = uber.mCell_state_t
Cell_value_t = uber.mCell_value_t
Click_t = uber.mClick_t
Context_t = uber.mContext_t
Difficulty_t = uber.mDifficulty_t
Minesweeper_t = uber.mMinesweeper_t
Position_t = uber.mPosition_t


EASY = uber.EASY
MEDIUM = uber.MEDIUM
HARD = uber.HARD

WINDOW_TITLE = ":: mSweeper _"
WINDOW_PREFIXES = {
    ms.UNINITIALIZED: "",
    ms.PLAYING:       "Game in progress - ",
    ms.GAME_LOST:     "Game lost - ",
    ms.GAME_WON:      "Game won! - "
}

CONTEXT_MAIN_MENU = uber.CONTEXT_MAIN_MENU
CONTEXT_SWEEPER = uber.CONTEXT_SWEEPER
CONTEXT_SWEEPER_HS = uber.CONTEXT_SWEEPER_HS
CONTEXT_HIGHSCORES = uber.CONTEXT_HIGHSCORES
CONTEXT_HELP = uber.CONTEXT_HELP

CELL_SIZE = 40
GAP_SIZE = 25
DEFAULT_MARGIN = 25

MARGINS: Dict[str, int] = {
    "top":    DEFAULT_MARGIN,
    "right":  DEFAULT_MARGIN,
    "bottom": DEFAULT_MARGIN,
    "left":   DEFAULT_MARGIN
}

NUM_FONT = ('system', 16)
NUM_COLOUR = "#000000"

DEFAULT_DICT_KEY = -1

CELL_COLOURS: Dict[Cell_state_t, Dict[Cell_value_t, Tuple[str, str]]] = {
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
        ms.MINE: ("#ff0839", "#ffffff")
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

STR_FLAG = "!!"
STR_MINE_SHOWN = "X"
STR_MINE = "x"


class Gui:
    def __init__(
        self,
        session: main.Session,
        is_interactive: bool
    ) -> None:
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
        new_context: Context_t
    ) -> None:
        if new_context == CONTEXT_MAIN_MENU:
            C_minesweeper(self)


class Context:
    def __init__(
        self,
        gui_root: Gui,
        width: int,
        height: int
    ) -> None:
        self.gui_root = gui_root
        self.session = gui_root.session
        self.canvas = tk.Canvas(width=width, height=height)
        self.canvas.pack()

    def quit_context_for(
        self,
        new_context: Context_t
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

        self._sweeper_reset()

    def _draw_cell(
        self,
        cell: Cell_t,
        cx: int,
        cy: int
    ) -> None:
        def get_colours() -> Tuple[str, str]:
            colours = CELL_COLOURS[state].get(value)

            if colours is None:
                colours = CELL_COLOURS[state][DEFAULT_DICT_KEY]

            return colours

        def get_txt() -> str:
            if state == ms.FLAG:
                return STR_FLAG
            elif value == ms.MINE:
                return STR_MINE_SHOWN if state == ms.SHOWN else STR_MINE
            elif value == 0 or state == ms.COVERED:
                return ""
            else:
                return str(value)

        state, value = ms.get_cell_state(cell), ms.get_cell_value(cell)
        main_clr, active_clr = get_colours()

        self.canvas.create_rectangle(
            cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
            fill=main_clr,
            activefill=active_clr
        )

        self.canvas.create_text(
            cx + CELL_SIZE // 2, cy + CELL_SIZE // 2,
            text=get_txt(),
            font=NUM_FONT,
            activefill="#ffffff",
            state="disabled"
        )

    def _sweeper_refresh(
        self
    ) -> None:
        ms_state = self.session.ms.get_state()
        self.root.title(WINDOW_PREFIXES[ms_state] + WINDOW_TITLE)

        self.canvas.delete(tk.ALL)
        for y, row in enumerate(self.ms_data):
            for x, cell in enumerate(row):
                cy = y * CELL_SIZE + MARGINS["top"] + 1
                cx = x * CELL_SIZE + MARGINS["left"] + 1

                self._draw_cell(cell, cx, cy)

    def _sweeper_reset(
        self
    ) -> None:  # reset()/init()
        self.session.get_new_ms()

        assert self.session.ms is not None
        self.ms_data: Minesweeper_t = self.session.ms.get_data()

        if self.gui_root.is_interactive:
            self._bind_actions()

        self._sweeper_refresh()

    def _bind_actions(
        self
    ) -> None:
        self.canvas.bind_all("r", lambda _: self._sweeper_reset())

        # TODO button for menu?
        # TODO <ButtonRelease-1>

        self.canvas.bind(
            "<Button-1>",
            lambda event: self._click(self.session.ms_lmb, event)
        )
        self.canvas.bind(
            "<Button-3>",
            lambda event: self._click(self.session.ms_rmb, event)
        )

    def _get_position(
        self,
        x: int,
        y: int
    ) -> Optional[Position_t]:
        x_pos = (x - MARGINS["left"] - 1) // CELL_SIZE
        y_pos = (y - MARGINS["top"] - 1) // CELL_SIZE

        return (x_pos, y_pos) \
            if 0 <= x_pos < self.deets["width"] \
            and 0 <= y_pos < self.deets["height"] \
            else None

    def _click(
        self,
        click_fun: Click_t,
        event: tk.Event  # type: ignore
    ) -> None:
        x, y = event.x, event.y
        position = self._get_position(x, y)

        if position is None:
            return

        click_fun(position)
        self._sweeper_refresh()
