import tkinter as tk

from . import contexts
from .. import gui as here
from ... import mSweeper_package as mSweeper


class Gui:
    def __init__(
        self,
        session: main.Session,
        is_interactive: bool
    ) -> None:
        here.init_shapes()

        self.session = session
        self.is_interactive = is_interactive

        self.hor_margin = here.MARGINS["left"] + here.MARGINS["right"]
        self.ver_margin = here.MARGINS["top"] + here.MARGINS["bottom"]

        self.max_width = mSweeper.DIFFICULTY_DICT[mSweeper.Difficulty_t.HARD]["width"] * here.CELL_SIZE \
            + self.hor_margin
        self.max_height = mSweeper.DIFFICULTY_DICT[mSweeper.Difficulty_t.HARD]["height"] * here.CELL_SIZE \
            + self.ver_margin + here.GAP_SIZE + here.BOX_A

        self.root = tk.Tk()
        self.root.title(SW_TITLE)
        self.root.resizable(False, False)
        self.root.bind_all("q", lambda _: self.root.destroy())

        self.change_context(contexts.Context_t.MAIN_MENU)
        self.root.mainloop()

    def change_context(
        self,
        new_context: contexts.Context_t
    ) -> None:
        if new_context == contexts.Context_t.MAIN_MENU:
            contexts.Main_menu(
                self,
                self.max_width,
                self.max_height
            )
        elif new_context == contexts.Context_t.MINESWEEPER:
            contexts.Minesweeper(
                self,
                self.session.deets["width"] * CELL_SIZE + self.hor_margin,
                self.session.deets["height"] * CELL_SIZE + self.ver_margin
                + GAP_SIZE + BOX_A
            )
        elif new_context == contexts.Context_t.HIGHSCORES:
            contexts.Highscores(
                self,
                self.max_width,
                self.max_height
            )
        elif new_context == contexts.Context_t.HELP:
            assert False, "WIP"
            C_help(self, 1, 1)  # TODO
