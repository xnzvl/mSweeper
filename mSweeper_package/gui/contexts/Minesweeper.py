from typing import Optional
import tkinter as tk

from .. import contexts as here
from .. import Context, Core

from ... import gui
from ... import minesweeper as ms
from .... import mSweeper_package as mSweeper


class C_minesweeper(Context.Context):
    def __init__(
            self,
            gui_root: Core.Gui,
            width: int,
            height: int
    ) -> None:
        super().__init__(gui_root, width, height)

        self.width = width
        self.height = height

        self.reset()

    def draw_cell(
            self,
            cell: mSweeper.Cell_t,
            x: int,
            y: int
    ) -> None:
        state, value = ms.get_cell_state(cell), ms.get_cell_value(cell)
        main_clr, active_clr = here.get_colour(state, value)

        self.canvas.create_rectangle(
            x, y, x + gui.CELL_SIZE, y + gui.CELL_SIZE,
            fill=main_clr,
            activefill=active_clr
        )

        if state == ms.FLAG:
            here.draw_flag(
                self.canvas, x, y, gui.CELL_SIZE,
                value == ms.MINE
                or self.session.ms_state == ms.Minesweeper_state.UNINITIALIZED
                or self.session.ms_state == ms.Minesweeper_state.PLAYING
            )
        elif value == ms.MINE:
            here.draw_mine(self.canvas, x, y, gui.CELL_SIZE)
        elif value == 0 or state == ms.COVERED:
            return
        else:
            self.canvas.create_text(
                x + gui.CELL_SIZE // 2, y + gui.CELL_SIZE // 2,
                font=(here.FONT, 16),  # TODO
                state="disabled",
                text=str(value)
            )

    def refresh(
        self
    ) -> None:
        def draw_deets() -> None:
            width = effective_width - gui.GAP_SIZE - gui.BOX_A \
                if special_case else b_width
            flag_str = f"{self.session.ms.flags:0>2d}" + (
                f" / {self.session.ms.mines}" if not special_case else ""
            )  # TODO

            self.canvas.create_rectangle(
                gui.Margins.LEFT, gui.Margins.TOP,
                gui.Margins.LEFT + width, gui.Margins.TOP + gui.BOX_A,
                fill=here.Colour.BACKGROUND,
                activeoutline=here.Colour.RED
            )

            self.canvas.create_text(
                gui.Margins.LEFT + gui.GAP_SIZE // 2 + gui.BOX_A,
                gui.Margins.TOP + gui.BOX_A // 2,
                anchor="w",
                font=(here.FONT, here.Font_size.DEFAULT),
                state="disabled",
                text=flag_str
            )

            here.draw_flag(
                self.canvas,
                gui.Margins.LEFT, gui.Margins.TOP, gui.BOX_A,
                True, True
            )

        def draw_observer() -> None:
            if special_case:
                return

            x_anchor = b_width + gui.Margins.LEFT + gui.GAP_SIZE
            face = self.canvas.create_rectangle(
                x_anchor, gui.Margins.TOP,
                x_anchor + gui.BOX_A, gui.Margins.TOP + gui.BOX_A,
                fill=here.Colour.BACKGROUND,
                activeoutline=here.Colour.RED
            )
            self.canvas.tag_bind(face, "<Button-1>", lambda _: self.reset())

            if ms_state == ms.Minesweeper_state.UNINITIALIZED:
                here.draw_mine(
                    self.canvas, x_anchor, gui.Margins.TOP, gui.BOX_A, True
                )
            else:
                if self.session.top_ten:
                    here.draw_trophy(self.canvas, x_anchor, gui.Margins.TOP, gui.BOX_A)
                else:
                    here.draw_face(
                        self.canvas, x_anchor, gui.Margins.TOP, gui.BOX_A, ms_state
                    )

        def draw_menu_button() -> None:
            menu_width = gui.BOX_A if special_case else b_width
            x_anchor = self.width - gui.Margins.RIGHT - menu_width

            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    x_anchor, gui.Margins.TOP,
                    self.width - gui.Margins.RIGHT, gui.Margins.TOP + gui.BOX_A,
                    fill=here.Colour.BACKGROUND,
                    activeoutline="red"
                ),
                "<Button-1>", self.q_to_main_menu
            )

            if not special_case:
                self.canvas.create_text(
                    x_anchor + gui.BOX_A, gui.Margins.TOP + gui.BOX_A // 2,
                    anchor="w",
                    font=(here.FONT, here.FONT_SIZE),
                    state="disabled",
                    text="Menu"
                )

            here.draw_menu_sign(self.canvas, x_anchor, gui.Margins.TOP, gui.BOX_A)

        ms_state = self.session.ms.get_state()
        effective_width = self.width - self.gui_root.hor_margin
        special_case = self.session.difficulty == mSweeper.Difficulty.EASY
        b_width = (effective_width - 2 * gui.GAP_SIZE - gui.BOX_A) // 2

        self.canvas.delete(tk.ALL)  # TODO
        self.root.title(WINDOW_PREFIXES[ms_state] + SW_TITLE)

        draw_deets()
        draw_observer()
        draw_menu_button()

        for y, row in enumerate(self.ms_data):
            for x, cell in enumerate(row):
                cx = x * gui.CELL_SIZE + gui.Margins.LEFT
                cy = y * gui.CELL_SIZE + gui.Margins.TOP + gui.GAP_SIZE + gui.BOX_A

                self.draw_cell(cell, cx, cy)

    def reset(
        self
    ) -> None:  # reset()/init()
        self.session.get_new_ms()

        assert self.session.ms is not None
        self.ms_data: u.mMinesweeper_t = self.session.ms.get_data()

        if self.gui_root.is_interactive:
            self.bind_actions()

        self.refresh()

    def bind_actions(
        self
    ) -> None:
        self.canvas.bind_all("r", lambda _: self.reset())

        self.canvas.bind(
            "<Button-1>",
            lambda event: self.click(self.session.ms_lmb, event)
        )

        self.canvas.bind(
            "<Button-3>",
            lambda event: self.click(self.session.ms_rmb, event)
        )

    def get_position(
        self,
        x: int,
        y: int
    ) -> Optional[here.Position_t]:
        x_pos = (x - gui.Margins.LEFT - 1) // gui.CELL_SIZE
        y_pos = (y - gui.Margins.TOP - gui.GAP_SIZE - gui.BOX_A - 1) // gui.CELL_SIZE

        return (x_pos, y_pos) \
            if 0 <= x_pos < self.session.deets["width"] \
            and 0 <= y_pos < self.session.deets["height"] \
            else None

    def click(
        self,
        click_fun: here.Click_t,
        event: tk.Event  # type: ignore
    ) -> None:
        position = self.get_position(event.x, event.y)

        if position is None:
            return

        click_fun(position)
        self.refresh()
