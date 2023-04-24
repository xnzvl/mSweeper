from typing import Callable

import tkinter as tk

import contexts
import Core


Quit_context_lambda = Callable[[tk.Event], None]


class Context:
    def __init__(
            self,
            gui_core: Core.Gui,
            width: int,
            height: int
    ) -> None:
        self.root = gui_core.root
        self.gui_core = gui_core
        self.session = gui_core.session
        self.width = width
        self.height = height

        self.canvas = tk.Canvas(
            width=width - 2, height=height - 2,  # to fix symmetry
            background=contexts.Colour.BACKGROUND.value
        )
        self.canvas.pack()

        self.q_to_main_menu: Quit_context_lambda = \
            lambda _: self.quit_context_for(contexts.Context.MAIN_MENU)
        self.q_to_sweeper: Quit_context_lambda = \
            lambda _: self.quit_context_for(contexts.Context.MINESWEEPER)
        self.q_to_highscores: Quit_context_lambda = \
            lambda _: self.quit_context_for(contexts.Context.HIGHSCORES)
        self.q_to_help: Quit_context_lambda = \
            lambda _: self.quit_context_for(contexts.Context.HELP)

    def quit_context_for(
            self,
            new_context: contexts.Context
    ) -> None:
        self.canvas.destroy()
        self.gui_core.change_context(new_context)
