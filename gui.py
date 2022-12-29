import tkinter as tk
from typing import Tuple, Optional
from minesweeper import Minesweeper

import uber


Click_t = uber.mClick_t
Position_t = uber.mPosition_t
Dimensions_t = uber.mDimensions_t


CELL_SIZE = uber.CELL_SIZE


class Game:
    def __init__(
        self,
        dimensions: Dimensions_t,
        clicks: Optional[Tuple[Click_t, Click_t]] = None
    ) -> None:
        width, height = dimensions

        self.root = tk.Tk()
        self.canvas = tk.Canvas(
            width=width * CELL_SIZE,
            height=height * CELL_SIZE
        )
        self.canvas.pack()

        self.canvas.bind_all("q", lambda _: self.root.destroy())

        if clicks is not None:
            self._lmb, self._rmb = clicks

            self.canvas.bind_all("r", lambda _: self._reset())
            self.canvas.bind("<Button-1>", self._click_lmb)
            self.canvas.bind("<Button-3>", self._click_rmb)

        self._reset()
        self.root.mainloop()

    def _refresh(
        self
    ) -> None:
        print("refresh\n")
        return

        self.canvas.delete("all")

    def _reset(
        self
    ) -> None:  # reset()/init()
        print("reset")
        # self._refresh()

    def _get_position(
        self,
        event: tk.Event
    ) -> Optional[Position_t]:
        x = event.x - 1
        y = event.y - 1
        return x, y

    def _click(
        self,
        click_fun: Click_t,
        event: tk.Event
    ) -> None:
        position = self._get_position(event)

        if position is None:
            return

        print(position)
        click_fun(position)
        self._refresh()

    def _click_lmb(
        self,
        event: tk.Event
    ) -> None:
        self._click(self._lmb, event)

    def _click_rmb(
        self,
        event: tk.Event
    ) -> None:
        self._click(self._rmb, event)


def main() -> None:
    ms = Minesweeper()
    a = Game((16, 16), (lambda _: print("LMB"), lambda _: print("RMB")))
    print(id(a))


if __name__ == "__main__":
    main()
