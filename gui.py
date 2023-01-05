import tkinter as tk
from typing import Optional, Dict

import main
import minesweeper as ms

import uber


Click_t = uber.mClick_t
Position_t = uber.mPosition_t


CELL_SIZE = 40

DEFAULT_MARGIN = 25
MARGINS: Dict[str, int] = {
    "top": DEFAULT_MARGIN,
    "right": DEFAULT_MARGIN,
    "bottom": DEFAULT_MARGIN,
    "left": DEFAULT_MARGIN
}

NUM_FONT = ('system', 16)
BACKGROUND = '#d9d9d9'

TILE_COLOUR = {' ': '#008000', 'X': '#292929', '*': '#800000'}

NUM_COLOURS = [
    BACKGROUND,
    '#0000ff',
    '#008100',
    '#ff1300',
    '#000083',
    '#810500',
    '#2a9494',
    '#000000',
    '#808080',
]


class Gui:
    def __init__(
        self,
        session: main.Session,
        interactive: bool = True
    ) -> None:
        self.session = session
        self.width, self.height = session.dimensions

        self.root = tk.Tk()
        self.canvas = tk.Canvas(
            width=self.width * CELL_SIZE + MARGINS["right"] + MARGINS["left"],
            height=self.height * CELL_SIZE + MARGINS["top"] + MARGINS["bottom"]
        )
        self.canvas.pack()

        self.canvas.bind_all("q", lambda _: self.root.destroy())

        if interactive:
            self.canvas.bind_all("r", lambda _: self._reset())
            self.canvas.bind(
                "<Button-1>",
                lambda event: self._click(self.session.lmb, event)
            )
            self.canvas.bind(
                "<Button-3>",
                lambda event: self._click(self.session.rmb, event)
            )

        self._reset()
        self.root.mainloop()

    def _draw_cell(
        self
    ) -> None:
        pass

    def _refresh(
        self
    ) -> None:
        print("refresh\n")

        self.canvas.delete("all")
        for y, row in enumerate(self.ms_data):
            for x, cell in enumerate(row):
                cy = y * CELL_SIZE + MARGINS["top"] + 1
                cx = x * CELL_SIZE + MARGINS["left"] + 1

                # draw_cell() or smth like that
                self.canvas.create_rectangle(
                    cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
                    fill="#ffffff"
                )

                cell_state = ms.get_cell_state(cell)

                if cell_state == ms.SHOWN:
                    self.canvas.create_text(
                        cx + CELL_SIZE // 2, cy + CELL_SIZE // 2,
                        text=str(ms.get_cell_mines(cell)),
                        font=NUM_FONT
                    )

                # self._draw_cell()

                # if tile:
                #     self.canvas.create_text(
                #         cx + CELL_SIZE // 2, cy + CELL_SIZE // 2,
                #         text=tile, font=NUM_FONT,
                #         fill=NUM_COLOURS[int(tile)]
                #     )

    def _reset(
        self
    ) -> None:  # reset()/init()
        print("reset/init - (re)init")
        self.ms_data = self.session.get_new_ms().get_data()

        self._refresh()

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

        print(position)  # testing
        click_fun(position)
        self._refresh()
