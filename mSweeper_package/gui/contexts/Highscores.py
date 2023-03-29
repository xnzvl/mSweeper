from typing import Optional
import tkinter as tk

from .. import contexts as here
from .. import Context, Core

from ... import gui
from ... import minesweeper as ms
from .... import mSweeper_package as mSweeper


class C_highscores(Context.Context):
    def __init__(
            self,
            gui_root: Core.Gui,
            width: int,
            height: int
    ) -> None:
        super().__init__(gui_root, width, height)

        self.diff_b = (self.width - 4 * gui.GAP_SIZE - 2 * gui.BOX_A - self.gui_root.hor_margin) // 3
        self.subheader_h = 60
        self.rows_gap = 5

        self.row_y_anchor = MARGINS["top"] + gui.BOX_A + gui.GAP_SIZE + self.subheader_h + gui.GAP_SIZE // 2 - self.rows_gap
        self.row_w = self.width - self.gui_root.hor_margin
        self.row_h = (self.height - self.row_y_anchor - MARGINS["bottom"]) // 10

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
                font=(DEF_FONT, record_font_size),
                state="disabled",
                tags=DISPOSABLE,
                text=txt
            )

        def draw_time(
                row: int,
                time: Optional[u.mTime_tuple_t]
        ) -> None:
            if time is not None:
                h, m, s, _ = time
                time_str = "{:02d}:{:02d}:{:02d}".format(h, m, s)
            else:
                time_str = "##:##:##"

            text(
                row,
                time_str,
                MARGINS["left"] + 4 * gui.GAP_SIZE
            )

        def draw_nick(
                row: int,
                nick: Optional[str]
        ) -> None:
            text(
                row,
                nick if nick is not None else "< BLANK >",
                MARGINS["left"] + gui.GAP_SIZE + 250
            )

        def draw_date(
                row: int,
                date: Optional[str]
        ) -> None:
            text(
                row,
                date if date is not None else "####-##-##",
                self.width - MARGINS["right"] - 2 * gui.GAP_SIZE,
                "e"
            )

        def mark_current(
                difficulty: mSweeper.Difficulty
        ) -> None:
            chop = self.diff_b // 4
            x = MARGINS["left"] + gui.BOX_A + gui.GAP_SIZE + chop

            if difficulty == mSweeper.Difficulty.MEDIUM:
                x += self.diff_b + gui.GAP_SIZE
            elif difficulty == mSweeper.Difficulty.HARD:
                x += 2 * (self.diff_b + gui.GAP_SIZE)

            self.canvas.create_rectangle(
                x, MARGINS["top"] + gui.BOX_A,
                x + self.diff_b - 2 * chop, MARGINS["top"] + gui.BOX_A - 5,
                fill="red",
                tags=DISPOSABLE
            )

        record_font_size = 16

        self.canvas.delete(DISPOSABLE)
        diff_records = self.session.hs_manager.get_diff_scores(difficulty)

        mark_current(difficulty)

        for i in range(10):
            text(
                i,
                f"{i + 1}.",
                MARGINS["left"] + gui.GAP_SIZE
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
                self.width - gui.BOX_A - MARGINS["right"], MARGINS["top"],
                self.width - MARGINS["right"], MARGINS["top"] + gui.BOX_A,
                fill=COLOUR_BACKGROUND,
                activeoutline="red",
                activewidth=3
            ),
            "<Button-1>",
            self.q_to_main_menu
        )

        draw_menu_sign(
            self.canvas,
            self.width - gui.BOX_A - MARGINS["right"], MARGINS["top"],
            gui.BOX_A
        )

        self.canvas.create_rectangle(
            MARGINS["right"], MARGINS["top"],
            MARGINS["right"] + gui.BOX_A, MARGINS["top"] + gui.BOX_A
        )

        draw_trophy(
            self.canvas,
            MARGINS["left"], MARGINS["top"],
            gui.BOX_A
        )

        x_anchor = MARGINS["left"] + gui.BOX_A + gui.GAP_SIZE

        for i, diff_enum in enumerate(
            [mSweeper.Difficulty.EASY, mSweeper.Difficulty.MEDIUM, mSweeper.Difficulty.HARD]
        ):
            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    x_anchor + i * (self.diff_b + gui.GAP_SIZE),
                    MARGINS["top"],
                    x_anchor + (i + 1) * self.diff_b + i * gui.GAP_SIZE,
                    MARGINS["top"] + gui.BOX_A,
                    fill=COLOUR_BACKGROUND,
                    activeoutline="red",
                    activewidth=3
                ),
                "<Button-1>",
                lambda _, d=diff_enum: self.change_shown_diff(d)
            )

            self.canvas.create_text(
                x_anchor + i * (self.diff_b + gui.GAP_SIZE) + self.diff_b // 2,
                MARGINS["top"] + gui.BOX_A // 2,
                fill="white",
                font=(DEF_FONT, DEF_FONT_SIZE),
                state="disabled",
                text=str(diff_enum).split('.')[-1]
            )

        self.canvas.create_rectangle(
            MARGINS["left"],
            MARGINS["top"] + gui.BOX_A + gui.GAP_SIZE,
            self.width - MARGINS["right"],
            MARGINS["top"] + gui.BOX_A + gui.GAP_SIZE + self.subheader_h
        )

        self.canvas.create_text(
            MARGINS["left"] + gui.GAP_SIZE,
            MARGINS["top"] + gui.BOX_A + gui.GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(DEF_FONT, DEF_FONT_SIZE),
            text="#"
        )

        self.canvas.create_text(
            MARGINS["left"] + 4 * gui.GAP_SIZE,
            MARGINS["top"] + gui.BOX_A + gui.GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(DEF_FONT, DEF_FONT_SIZE),
            text="Time"
        )

        self.canvas.create_text(
            MARGINS["left"] + gui.GAP_SIZE + 250,
            MARGINS["top"] + gui.BOX_A + gui.GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(DEF_FONT, DEF_FONT_SIZE),
            text="Nickname"
        )

        self.canvas.create_text(
            self.width - MARGINS["right"] - 5 * gui.GAP_SIZE,
            MARGINS["top"] + gui.BOX_A + gui.GAP_SIZE + self.subheader_h // 2,
            anchor="w",
            fill="white",
            font=(DEF_FONT, DEF_FONT_SIZE),
            text="Date"
        )

        for i in range(10):
            self.canvas.create_rectangle(
                MARGINS["left"],
                self.row_y_anchor + i * self.row_h + self.rows_gap,
                MARGINS["left"] + self.row_w,
                self.row_y_anchor + (i + 1) * self.row_h,
                activeoutline="red",
                fill=COLOUR_BACKGROUND
            )
