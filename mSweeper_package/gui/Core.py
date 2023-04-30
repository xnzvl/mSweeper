import tkinter as tk

from .. import gui as here

from . import contexts

import mSweeper_package as mSweeper


class Gui:
    def __init__(
            self,
            session: mSweeper.Session.Session,
            is_interactive: bool
    ) -> None:
        here.init_shapes()

        self.session = session
        self.is_interactive = is_interactive

        self.hor_margin = here.Margins.LEFT.value + here.Margins.RIGHT.value
        self.ver_margin = here.Margins.TOP.value + here.Margins.BOTTOM.value

        max_config = mSweeper.DIFFICULTY_DICT[mSweeper.Difficulty.HARD]
        self.max_width = max_config["width"] * here.CELL_SIZE + self.hor_margin
        self.max_height = max_config["height"] * here.CELL_SIZE + self.ver_margin + here.GAP_SIZE + here.BOX_A

        self.root = tk.Tk()
        self.root.title(mSweeper.SOFTWARE_TITLE)
        self.root.resizable(False, False)
        self.root.bind_all("q", lambda _: self.root.destroy())

        self.change_context(contexts.Context.MAIN_MENU)
        self.root.mainloop()

    def change_context(
            self,
            new_context: contexts.Context
    ) -> None:
        assert self.session.ms_deets is not None

        if new_context == contexts.Context.MAIN_MENU:
            contexts.Context_main_menu(
                self,
                self.max_width,
                self.max_height
            )
        elif new_context == contexts.Context.MINESWEEPER:
            contexts.Context_minesweeper(
                self,
                self.session.ms_deets["width"] * here.CELL_SIZE + self.hor_margin,
                self.session.ms_deets["height"] * here.CELL_SIZE + self.ver_margin + here.GAP_SIZE + here.BOX_A
            )
        elif new_context == contexts.Context.HIGHSCORES:
            contexts.Context_highscores(
                self,
                self.max_width,
                self.max_height
            )
        elif new_context == contexts.Context.HELP:
            assert False, "WIP"
            contexts.Context_help(self, 1, 1)  # TODO
