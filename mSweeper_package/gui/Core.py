
class Gui:
    def __init__(
        self,
        session: main.Session,
        is_interactive: bool
    ) -> None:
        init_shapes()

        self.session = session
        self.is_interactive = is_interactive

        self.hor_margin = MARGINS["left"] + MARGINS["right"]
        self.ver_margin = MARGINS["top"] + MARGINS["bottom"]

        self.max_width = main.DIFFICULTY_DICT[u.Difficulty.HARD]["width"] * CELL_SIZE \
            + self.hor_margin
        self.max_height = main.DIFFICULTY_DICT[u.Difficulty.HARD]["height"] * CELL_SIZE \
            + self.ver_margin + GAP_SIZE + BOX_A

        self.root = tk.Tk()
        self.root.title(SW_TITLE)
        self.root.resizable(False, False)
        self.root.bind_all("q", lambda _: self.root.destroy())

        self.change_context(CONTEXT_MAIN_MENU)
        self.root.mainloop()

    def change_context(
        self,
        new_context: u.mContext_t
    ) -> None:
        if new_context == CONTEXT_MAIN_MENU:
            C_main_menu(
                self,
                self.max_width,
                self.max_height
            )
        elif new_context == CONTEXT_SWEEPER:
            C_minesweeper(
                self,
                self.session.deets["width"] * CELL_SIZE + self.hor_margin,
                self.session.deets["height"] * CELL_SIZE + self.ver_margin
                + GAP_SIZE + BOX_A
            )
        elif new_context == CONTEXT_HIGHSCORES:
            C_highscores(
                self,
                self.max_width,
                self.max_height
            )
        elif new_context == CONTEXT_HELP:
            assert False, "WIP"
            C_help(self, 1, 1)  # TODO
