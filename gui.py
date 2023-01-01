import tkinter as tk

from typing import Optional
import main

import uber


Click_t = uber.mClick_t
Position_t = uber.mPosition_t


CELL_SIZE = 20

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
        width, height = session.dimensions

        self.root = tk.Tk()
        self.canvas = tk.Canvas(
            width=width * CELL_SIZE,
            height=height * CELL_SIZE
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

    def start_mainloop(
        self
    ) -> None:
        self._reset()
        self.root.mainloop()

    def _refresh(
        self
    ) -> None:
        print("refresh\n")

        self.canvas.delete("all")
        for y, row in enumerate(self.ms_data):
            for x, tile in enumerate(row):
                continue
                # cy = y * CELL_SIZE + 1
                # cx = x * CELL_SIZE + 1
                # self.canvas.create_rectangle(
                #     cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
                #     fill=TILE_COLOUR.get(tile, BACKGROUND)
                # )
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
        self.ms_data = self.session._get_new_ms().get_data()

        self._refresh()

    def _get_position(
        self,
        x: int,
        y: int
    ) -> Optional[Position_t]:
        return x, y

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
