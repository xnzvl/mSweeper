import tkinter as tk

import mSweeper_package.gui as here

import mSweeper_package as mSweeper
import mSweeper_package.Details as Details
import mSweeper_package.gui.contexts as contexts


class Gui:
    def __init__(
            self,
            info_blob: Details.Info_blob,
            is_interactive: bool
    ) -> None:
        here.init_shapes()

        self.info_blob = info_blob
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
        if new_context == contexts.Context.MAIN_MENU:
            import mSweeper_package.gui.contexts.Context_main_menu as C_main_menu
            C_main_menu.Context_main_menu(
                self.info_blob,
                self,
                self.max_width,
                self.max_height
            )

        elif new_context == contexts.Context.MINESWEEPER:
            import mSweeper_package.gui.contexts.Context_minesweeper as C_minesweeper
            C_minesweeper.Context_minesweeper(
                self.info_blob,
                self,
                self.info_blob.ms_config["width"] * here.CELL_SIZE + self.hor_margin,
                self.info_blob.ms_config["height"] * here.CELL_SIZE + self.ver_margin + here.GAP_SIZE + here.BOX_A
            )

        elif new_context == contexts.Context.HIGHSCORES:
            import mSweeper_package.gui.contexts.Context_highscores as C_highscores
            C_highscores.Context_highscores(
                self.info_blob,
                self,
                self.max_width,
                self.max_height
            )

        elif new_context == contexts.Context.HELP:
            import mSweeper_package.gui.contexts.Context_help as C_help
            assert False, "WIP"
            C_help.Context_help(self, 1, 1)  # TODO
