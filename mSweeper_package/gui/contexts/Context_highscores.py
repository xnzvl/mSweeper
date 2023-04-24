from typing import Optional

import contexts as here

import Context
import Core

from ... import gui

import mSweeper_package as mSweeper


class Context_highscores(Context.Context):
    def __init__(
            self,
            gui_core: Core.Gui,
            width: int,
            height: int
    ) -> None:
        super().__init__(gui_core, width, height)

        self.diff_b = (self.width - 4 * gui.GAP_SIZE - 2 * gui.BOX_A - self.gui_core.hor_margin) // 3
        self.subheader_h = 60
        self.rows_gap = 5

        self.row_y_anchor = gui.Margins.TOP + gui.BOX_A + gui.GAP_SIZE + self.subheader_h + gui.GAP_SIZE // 2 - self.rows_gap
        self.row_w = self.width - self.gui_core.hor_margin
        self.row_h = (self.height - self.row_y_anchor - gui.Margins.BOTTOM) // 10

        self.init_draw()
        self.change_shown_diff(mSweeper.Difficulty.MEDIUM)

    def change_shown_diff(
            self,
            difficulty: mSweeper.Difficulty
    ) -> None:

        def text(
                row: int,
                txt: str,
                x: int,
                anchor: str = "w"
        ) -> None:
            self.canvas.create_text(
                x, self.row_y_anchor + row * self.row_h + (self.row_h - self.rows_gap) * 0.5 + self.rows_gap,
                anchor=anchor,
                fill="white",
                font=(here.Font_size.DEFAULT, record_font_size),
                state="disabled",
                tags=here.DISPOSABLE_FLAG,
                text=txt
            )

        def draw_time(
                row: int,
                time: Optional[u.mTime_tuple_t]  # TODO
        ) -> None:
            if time is not None:
                h, m, s, _ = time
                time_str = "{:02d}:{:02d}:{:02d}".format(h, m, s)
            else:
                time_str = "##:##:##"

            text(
                row,
                time_str,
                gui.Margins.LEFT + 4 * gui.GAP_SIZE
            )

        def draw_nick(
                row: int,
                nick: Optional[str]
        ) -> None:
            text(
                row,
                nick if nick is not None else "< BLANK >",
                gui.Margins.LEFT + gui.GAP_SIZE + 250
            )

        def draw_date(
                row: int,
                date: Optional[str]
        ) -> None:
            text(
                row,
                date if date is not None else "####-##-##",
                self.width - gui.Margins.RIGHT - 2 * gui.GAP_SIZE,
                "e"
            )

        def mark_current(
                difficulty: mSweeper.Difficulty
        ) -> None:
            chop = self.diff_b // 4
            x = gui.Margins.LEFT + gui.BOX_A + gui.GAP_SIZE + chop

            if difficulty == mSweeper.Difficulty.MEDIUM:
                x += self.diff_b + gui.GAP_SIZE
            elif difficulty == mSweeper.Difficulty.HARD:
                x += 2 * (self.diff_b + gui.GAP_SIZE)

            self.canvas.create_rectangle(
                x, gui.Margins.TOP + gui.BOX_A,
                x + self.diff_b - 2 * chop, gui.Margins.TOP + gui.BOX_A - 5,
                fill="red",
                tags=here.DISPOSABLE_FLAG
            )

        record_font_size = 16

        self.canvas.delete(here.DISPOSABLE_FLAG)
        diff_records = self.session.hs_manager.get_diff_scores(difficulty)

        mark_current(difficulty)

        for i in range(10):
            text(
                i,
                f"{i + 1}.",
                gui.Margins.LEFT + gui.GAP_SIZE
            )

            time, date, nick = (None, None, None) \
                if i >= len(diff_records) \
                else diff_records[i]

            draw_time(i, time)
            draw_nick(i, nick)
            draw_date(i, date)

    def init_draw(
        self
    ) -> None:
        self.canvas.tag_bind(
            self.canvas.create_rectangle(
                self.width - gui.BOX_A - gui.Margins.RIGHT, gui.Margins.TOP,
                self.width - gui.Margins.RIGHT, gui.Margins.TOP + gui.BOX_A,
                fill=here.Colour.BACKGROUND,
                activeoutline="red",
                activewidth=3
            ),
            "<Button-1>",
            self.q_to_main_menu
        )

        here.draw_menu_sign(
            self.canvas,
            self.width - gui.BOX_A - gui.Margins.RIGHT, gui.Margins.TOP,
            gui.BOX_A
        )

        self.canvas.create_rectangle(
            gui.Margins.RIGHT, gui.Margins.TOP,
            gui.Margins.RIGHT + gui.BOX_A, gui.Margins.TOP + gui.BOX_A
        )

        here.draw_trophy(
            self.canvas,
            gui.Margins.LEFT, gui.Margins.TOP,
            gui.BOX_A
        )

        x_anchor = gui.Margins.LEFT + gui.BOX_A + gui.GAP_SIZE

        for i, diff_enum in enumerate(
            [mSweeper.Difficulty.EASY, mSweeper.Difficulty.MEDIUM, mSweeper.Difficulty.HARD]
        ):
            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    x_anchor + i * (self.diff_b + gui.GAP_SIZE),
                    gui.Margins.TOP,
                    x_anchor + (i + 1) * self.diff_b + i * gui.GAP_SIZE,
                    gui.Margins.TOP + gui.BOX_A,
                    fill=here.Colour.BACKGROUND,
                    activeoutline="red",
                    activewidth=3
                ),
                "<Button-1>",
                lambda _, d=diff_enum: self.change_shown_diff(d)
            )

            self.canvas.create_text(
                x_anchor + i * (self.diff_b + gui.GAP_SIZE) + self.diff_b // 2,
                gui.Margins.TOP + gui.BOX_A // 2,
                fill="white",
                font=(here.FONT, here.Font_size.DEFAULT),
                state="disabled",
                text=str(diff_enum).split('.')[-1]
            )

        self.canvas.create_rectangle(
            gui.Margins.LEFT,
            gui.Margins.TOP + gui.BOX_A + gui.GAP_SIZE,
            self.width - gui.Margins.RIGHT,
            gui.Margins.TOP + gui.BOX_A + gui.GAP_SIZE + self.subheader_h
        )

        self.canvas.create_text(
            gui.Margins.LEFT + gui.GAP_SIZE,
            gui.Margins.TOP + gui.BOX_A + gui.GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(here.FONT, here.Font_size.DEFAULT),
            text="#"
        )

        self.canvas.create_text(
            gui.Margins.LEFT + 4 * gui.GAP_SIZE,
            gui.Margins.TOP + gui.BOX_A + gui.GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(here.FONT, here.Font_size.DEFAULT),
            text="Time"
        )

        self.canvas.create_text(
            gui.Margins.LEFT + gui.GAP_SIZE + 250,
            gui.Margins.TOP + gui.BOX_A + gui.GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(here.FONT, here.Font_size.DEFAULT),
            text="Nickname"
        )

        self.canvas.create_text(
            self.width - gui.Margins.RIGHT - 5 * gui.GAP_SIZE,
            gui.Margins.TOP + gui.BOX_A + gui.GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(here.FONT, here.Font_size.DEFAULT),
            text="Date"
        )

        for i in range(10):
            self.canvas.create_rectangle(
                gui.Margins.LEFT,
                self.row_y_anchor + i * self.row_h + self.rows_gap,
                gui.Margins.LEFT + self.row_w,
                self.row_y_anchor + (i + 1) * self.row_h,
                activeoutline="red",
                fill=here.Colour.BACKGROUND
            )
