from typing import Optional
import tkinter as tk

import mSweeper_package.gui.contexts as here

import mSweeper_package as mSweeper
import mSweeper_package.Details as Details
import mSweeper_package.gui as gui
import mSweeper_package.gui.Context as Context
import mSweeper_package.gui.Core as Core
import mSweeper_package.minesweeper as ms
import mSweeper_package.minesweeper.Proxy as Proxy


class Context_minesweeper(Context.Context):
    def __init__(
            self,
            info_blob: Details.Info_blob,
            gui_root: Core.Gui,
            width: int,
            height: int
    ) -> None:
        super().__init__(info_blob, gui_root, width, height)

        self.width = width
        self.height = height
        self.ms_proxy = Proxy.Minesweeper_proxy(info_blob)

        self.reset()

    def draw_cell(
            self,
            cell: ms.Cell_t,
            x: int,
            y: int
    ) -> None:
        main_clr, active_clr = here.get_colours(cell)
        state, value = ms.get_cell_state(cell), ms.get_cell_value(cell)

        self.canvas.create_rectangle(
            x, y, x + gui.CELL_SIZE, y + gui.CELL_SIZE,
            fill=main_clr,
            activefill=active_clr
        )

        if state == ms.FLAG:
            here.draw_flag(
                self.canvas, x, y, gui.CELL_SIZE,
                value == ms.MINE
                or self.info_blob.ms_state == ms.Minesweeper_state.UNINITIALIZED
                or self.info_blob.ms_state == ms.Minesweeper_state.PLAYING
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
            assert self.ms_proxy.ms is not None

            width = effective_width - gui.GAP_SIZE - gui.BOX_A if special_case else b_width
            flag_str = f"{self.ms_proxy.ms.flags:0>2d}" + (  # TODO
                f" / {self.ms_proxy.ms.mines}" if not special_case else ""
            )  # TODO

            self.canvas.create_rectangle(
                gui.Margins.LEFT.value, gui.Margins.TOP.value,
                gui.Margins.LEFT.value + width, gui.Margins.TOP.value + gui.BOX_A,
                fill=here.Colour.BACKGROUND.value,
                activeoutline=here.Colour.RED.value
            )

            self.canvas.create_text(
                gui.Margins.LEFT.value + gui.GAP_SIZE // 2 + gui.BOX_A,
                gui.Margins.TOP.value + gui.BOX_A // 2,
                anchor="w",
                font=(here.FONT, here.Font_size.DEFAULT.value),
                state="disabled",
                text=flag_str
            )

            here.draw_flag(
                self.canvas,
                gui.Margins.LEFT.value, gui.Margins.TOP.value, gui.BOX_A,
                True, True
            )

        def draw_observer() -> None:
            if special_case:
                return

            x_anchor = gui.Margins.LEFT.value + gui.GAP_SIZE + b_width
            face = self.canvas.create_rectangle(
                x_anchor, gui.Margins.TOP.value,
                x_anchor + gui.BOX_A, gui.Margins.TOP.value + gui.BOX_A,
                fill=here.Colour.BACKGROUND.value,
                activeoutline=here.Colour.RED.value
            )
            self.canvas.tag_bind(face, "<Button-1>", lambda _: self.reset())

            if ms_state == ms.Minesweeper_state.UNINITIALIZED:
                here.draw_mine(
                    self.canvas, x_anchor, gui.Margins.TOP.value, gui.BOX_A, True
                )
            else:
                if self.info_blob.ms_top_ten:
                    here.draw_trophy(self.canvas, x_anchor, gui.Margins.TOP.value, gui.BOX_A)
                else:
                    here.draw_face(
                        self.canvas, x_anchor, gui.Margins.TOP.value, gui.BOX_A, ms_state
                    )

        def draw_menu_button() -> None:
            menu_width = gui.BOX_A if special_case else b_width
            x_anchor = self.width - gui.Margins.RIGHT.value - menu_width

            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    x_anchor, gui.Margins.TOP.value,
                    self.width - gui.Margins.RIGHT.value, gui.Margins.TOP.value + gui.BOX_A,
                    fill=here.Colour.BACKGROUND.value,
                    activeoutline="red"
                ),
                "<Button-1>", self.q_to_main_menu
            )

            if not special_case:
                self.canvas.create_text(
                    x_anchor + gui.BOX_A, gui.Margins.TOP.value + gui.BOX_A // 2,
                    anchor="w",
                    font=(here.FONT, here.Font_size.DEFAULT.value),
                    state="disabled",
                    text="Menu"
                )

            here.draw_menu_sign(self.canvas, x_anchor, gui.Margins.TOP.value, gui.BOX_A)

        assert self.ms_proxy.ms is not None

        ms_state: ms.Minesweeper_state = self.ms_proxy.ms.get_state()
        effective_width: int = self.width - self.gui_core.hor_margin
        special_case: bool = self.info_blob.ms_difficulty == mSweeper.Difficulty.EASY
        b_width: int = (effective_width - 2 * gui.GAP_SIZE - gui.BOX_A) // 2

        self.canvas.delete(tk.ALL)  # TODO - delete disposable?
        self.root.title(mSweeper.WINDOW_PREFIXES[ms_state] + mSweeper.SOFTWARE_TITLE)

        draw_deets()
        draw_observer()
        draw_menu_button()

        for y, row in enumerate(self.ms_field):
            for x, cell in enumerate(row):
                cx = x * gui.CELL_SIZE + gui.Margins.LEFT.value
                cy = y * gui.CELL_SIZE + gui.Margins.TOP.value + gui.GAP_SIZE + gui.BOX_A

                self.draw_cell(cell, cx, cy)

    def reset(
            self
    ) -> None:  # reset()/init()
        self.ms_proxy.new_minesweeper()

        assert self.ms_proxy.ms is not None
        self.ms_field: ms.Field_t = self.ms_proxy.ms.get_data()  # TODO

        if self.gui_core.is_interactive:  # TODO
            self.bind_actions()

        self.refresh()

    def bind_actions(
            self
    ) -> None:
        self.canvas.bind_all("r", lambda _: self.reset())

        self.canvas.bind(
            "<Button-1>",
            lambda event: self.click(self.ms_proxy.ms_lmb, event)
        )

        self.canvas.bind(
            "<Button-3>",
            lambda event: self.click(self.ms_proxy.ms_rmb, event)
        )

    def get_position(
            self,
            x: int,
            y: int
    ) -> Optional[here.Position_t]:
        x_pos = (x - gui.Margins.LEFT.value - 1) // gui.CELL_SIZE
        y_pos = (y - gui.Margins.TOP.value - gui.GAP_SIZE - gui.BOX_A - 1) // gui.CELL_SIZE

        assert self.info_blob.ms_config is not None

        return (x_pos, y_pos) \
            if 0 <= x_pos < self.info_blob.ms_config["width"] \
            and 0 <= y_pos < self.info_blob.ms_config["height"] \
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
