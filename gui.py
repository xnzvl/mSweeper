import tkinter as tk
from typing import Optional, Dict

import main
import minesweeper as ms

import uber


Click_t = uber.mClick_t
Position_t = uber.mPosition_t
Cell_t = uber.mCell_t
Cell_state_t = uber.mCell_state_t
Cell_value_t = uber.mCell_value_t


WINDOW_TITLE = "[GAME] :: mSweeper _"
WINDOW_ADDS = {
    ms.UNINITIALIZED: "",
    ms.PLAYING: "Game in progress - ",
    ms.GAME_LOST: " Game lost - ",
    ms.GAME_WON: "Game won! - "
}

CELL_SIZE = 40

DEFAULT_MARGIN = 25
MARGINS: Dict[str, int] = {
    "top": DEFAULT_MARGIN,
    "right": DEFAULT_MARGIN,
    "bottom": DEFAULT_MARGIN,
    "left": DEFAULT_MARGIN
}

NUM_FONT = ('system', 16)
NUM_COLOUR = "#000000"

DEFAULT_DICT_KEY = -1


# ===============================
#  TODO activefills alternatives
# ===============================

CELL_COLOURS: Dict[Cell_state_t, Dict[Cell_value_t, str]] = {
    ms.SHOWN: {
        0: "#faf3e1",
        1: "#b4db81",
        2: "#dbd281",
        3: "#dbb381",
        4: "#db8f81",
        5: "#bf81db",
        6: "#a081db",
        7: "#8183db",
        8: "#595aa8",
        ms.MINE: "#ff0839"
    },
    ms.FLAG: {
        ms.MINE: "#a39676",
        ms.UNKNOWN: "#a39676",
        DEFAULT_DICT_KEY: "#a67e6f"  # misplaced flag
    },
    ms.COVERED: {
        ms.MINE: "#a39676",
        DEFAULT_DICT_KEY: "#dbcead"
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
        self.width, self.height = session.dimensions

        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.canvas = tk.Canvas(
            width=self.width * CELL_SIZE + MARGINS["right"] + MARGINS["left"],
            height=self.height * CELL_SIZE + MARGINS["top"] + MARGINS["bottom"]
        )
        self.canvas.pack()

        self.canvas.bind_all("q", lambda _: self.root.destroy())

        self._reset()
        self.root.mainloop()

    def _draw_cell(
        self,
        cell: Cell_t,
        cx: int,
        cy: int
    ) -> None:
        def get_colour() -> str:
            colour = CELL_COLOURS[state].get(value)

            if colour is None:
                colour = CELL_COLOURS[state][DEFAULT_DICT_KEY]

            return colour

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

        self.canvas.create_rectangle(
            cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
            fill=get_colour()
        )

        self.canvas.create_text(
            cx + CELL_SIZE // 2, cy + CELL_SIZE // 2,
            text=get_txt(),
            font=NUM_FONT
        )

    def _refresh(
        self
    ) -> None:
        ms_state = self.session.ms.get_state()
        self.root.title(WINDOW_ADDS[ms_state] + WINDOW_TITLE)

        self.canvas.delete("all")
        for y, row in enumerate(self.ms_data):
            for x, cell in enumerate(row):
                cy = y * CELL_SIZE + MARGINS["top"] + 1
                cx = x * CELL_SIZE + MARGINS["left"] + 1

                self._draw_cell(cell, cx, cy)

    def _reset(
        self
    ) -> None:  # reset()/init()
        self.session.get_new_ms()
        assert self.session.ms is not None
        self.ms_data = self.session.ms.get_data()

        if self.is_interactive:
            self._bind_actions()

        self._refresh()

    def _bind_actions(
        self
    ) -> None:
        self.canvas.bind_all("r", lambda _: self._reset())
        # TODO button for menu?
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
            if 0 <= x_pos < self.width and 0 <= y_pos < self.height \
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
        self._refresh()
