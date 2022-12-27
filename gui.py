import tkinter as tk
# import Minesweeper from mSweeper

import uber


CELL_SIZE = uber.CELL_SIZE


class Game:
    def __init__(
        self,
        heigth: int,
        width: int
    ) -> None:
        self.root = tk.Tk()
        self.canvas = tk.Canvas(
            width=width * CELL_SIZE,
            height=heigth * CELL_SIZE
        )
        self.canvas.pack()

        self.reset()

        self.canvas.bind_all("q", lambda _: self.root.destroy())

    def reset(
        self
    ) -> None:  # resert()/init()
        pass


def main() -> None:
    a = Game(16, 16)
    a.root.mainloop()


if __name__ == "__main__":
    main()
