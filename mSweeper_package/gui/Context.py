import tkinter as tk

import mSweeper_package.gui as here

import mSweeper_package.Details as Details
import mSweeper_package.gui.contexts as contexts
import mSweeper_package.gui.Core as Core


class Context:
    def __init__(
            self,
            info_blob: Details.Info_blob,
            gui_core: Core.Gui,
            width: int,
            height: int
    ) -> None:
        self.root = gui_core.root
        self.gui_core = gui_core
        self.info_blob = info_blob
        self.width = width
        self.height = height

        self.canvas = tk.Canvas(
            width=width - 2, height=height - 2,  # to fix symmetry
            background=contexts.Colour.BACKGROUND.value
        )
        self.canvas.pack()

        self.q_to_main_menu: here.Quit_context_lambda = \
            lambda _: self.quit_context_for(contexts.Context.MAIN_MENU)
        self.q_to_sweeper: here.Quit_context_lambda = \
            lambda _: self.quit_context_for(contexts.Context.MINESWEEPER)
        self.q_to_highscores: here.Quit_context_lambda = \
            lambda _: self.quit_context_for(contexts.Context.HIGHSCORES)
        self.q_to_help: here.Quit_context_lambda = \
            lambda _: self.quit_context_for(contexts.Context.HELP)

    def quit_context_for(
            self,
            new_context: contexts.Context
    ) -> None:
        self.canvas.destroy()
        self.gui_core.change_context(new_context)
