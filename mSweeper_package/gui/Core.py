import tkinter as tk

import gui as here

import contexts

import mSweeper_package as mSweeper


class Gui:
    def __init__(
            self,
            session: mSweeper.Session,
            is_interactive: bool
    ) -> None:
        here.init_shapes()

        self.session = session
        self.is_interactive = is_interactive

        self.hor_margin = here.Margins.LEFT + here.Margins.RIGHT
        self.ver_margin = here.Margins.TOP + here.Margins.BOTTOM

        max_config = mSweeper.DIFFICULTY_DICT[mSweeper.Difficulty.HARD]
        self.max_width = max_config["width"] * here.CELL_SIZE + self.hor_margin
        self.max_height = max_config["height"] * here.CELL_SIZE + self.ver_margin + here.GAP_SIZE + here.BOX_A

        self.root = tk.Tk()
        self.root.title(SW_TITLE)  # TODO
        self.root.resizable(False, False)
        self.root.bind_all("q", lambda _: self.root.destroy())

        self.change_context(contexts.Context.MAIN_MENU)
        self.root.mainloop()

    def change_context(
            self,
            new_context: contexts.Context
    ) -> None:
        if new_context == contexts.Context.MAIN_MENU:
            contexts.Context_main_menu(
                self,
                self.max_width,
                self.max_height
            )
        elif new_context == contexts.Context.MINESWEEPER:
            contexts.Context_minesweeper(
                self,
                self.session.deets["width"] * here.CELL_SIZE + self.hor_margin,
                self.session.deets["height"] * here.CELL_SIZE + self.ver_margin + here.GAP_SIZE + here.BOX_A
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
