from typing import Callable
import tkinter as tk

import mSweeper_package.gui.contexts as here

import mSweeper_package as mSweeper
import mSweeper_package.Details as Details
import mSweeper_package.gui as gui
import mSweeper_package.data_management as data
import mSweeper_package.data_management.highscores as Highscores
import mSweeper_package.gui.Context as Context
import mSweeper_package.gui.Core as Core


class Context_main_menu(Context.Context):
    def __init__(
            self,
            info_blob: Details.Info_blob,
            gui_core: Core.Gui,
            width: int,
            height: int
    ) -> None:
        super().__init__(info_blob, gui_core, width, height)

        header_b_width: int = (width - self.gui_core.hor_margin - gui.GAP_SIZE) // 2
        diff_b_a: int = (width - self.gui_core.hor_margin - 2 * gui.GAP_SIZE) // 3

        y_anchor = height - (3 * gui.GAP_SIZE + 2 * gui.BOX_A + diff_b_a)
        y_anchor += draw_title(self.canvas, y_anchor) + gui.GAP_SIZE

        self.nickbox_y = y_anchor
        self.nickbox_width = header_b_width

        self.keyboard = False
        self.bind_default()

        y_anchor += draw_header(self.canvas, y_anchor, header_b_width, self.q_to_highscores) + gui.GAP_SIZE
        y_anchor += draw_diffs(self.canvas, y_anchor, diff_b_a, self.set_diff_and_quit) + gui.GAP_SIZE
        y_anchor += draw_footer(self.canvas, y_anchor, width, height, self.q_to_help)

        if y_anchor > height - gui.Margins.BOTTOM.value:
            raise ValueError("Content out of bounds (margins)")

    def set_diff_and_quit(
            self,
            difficulty: mSweeper.Difficulty
    ) -> None:
        self.info_blob.set_difficulty(difficulty)
        self.quit_context_for(here.Context.MINESWEEPER)

    def draw_nickbox(
            self,
            colour: here.Colour
    ) -> None:
        self.canvas.delete("nick_box")
        self.canvas.tag_bind(
            self.canvas.create_rectangle(
                gui.Margins.LEFT.value, self.nickbox_y,
                gui.Margins.LEFT.value + self.nickbox_width, self.nickbox_y + gui.BOX_A,
                activeoutline="red",
                activewidth=3,
                fill=here.Colour.BACKGROUND.value,
                outline=colour.value,
                tag="nick_box"
            ),
            "<Button-1>",  # TODO add RMB button consts
            lambda _: self.bind_keyboard()
        )

    def draw_nick_text(
            self
    ) -> None:
        self.canvas.delete("nick_text")
        self.canvas.create_text(
            gui.GAP_SIZE * 2, self.nickbox_y + gui.BOX_A // 2,
            anchor="w",
            fill=here.Colour.WHITE.value,
            font=(here.FONT, here.Font_size.DEFAULT.value),
            state="disabled",
            tags="nick_text",
            text=self.info_blob.player_nick
        )

    def update_nick_text(
            self,
            char: str
    ) -> None:
        if char == "\b":
            self.info_blob.player_nick = self.info_blob.player_nick[:len(self.info_blob.player_nick) - 1]
        elif len(self.info_blob.player_nick) < 16:
            self.info_blob.player_nick += char

        self.draw_nick_text()

    def bind_default(
            self
    ) -> None:
        if self.keyboard:  # TODO bind with `add` argument
            self.keyboard = False
            return

        self.unbind_keyboard()
        self.draw_nickbox(here.Colour.BLACK)
        self.draw_nick_text()

        Core.bind_default(self.root)

        self.canvas.bind(
            "<Button-1>",
            lambda _: self.bind_default()
        )

    def bind_keyboard(
            self
    ) -> None:
        if self.info_blob.player_nick == data.DEFAULT_NICKNAME:
            self.info_blob.player_nick = ""

        Core.unbind_default(self.root)

        self.draw_nickbox(here.Colour.RED)
        self.draw_nick_text()
        self.keyboard = True

        for char in Highscores.ALLOWED_CHARS | {"\b"}:
            self.root.bind(
                char_to_tksequence(char),
                lambda _, c=char: self.update_nick_text(c)
            )

    def unbind_keyboard(
            self
    ) -> None:
        for char in Highscores.ALLOWED_CHARS | {"\b"}:
            self.root.unbind(char_to_tksequence(char))

        if self.info_blob.player_nick.strip() == "":
            self.info_blob.player_nick = data.DEFAULT_NICKNAME


def char_to_tksequence(
        char: str
) -> str:
    match char:
        case " ":
            return "<space>"
        case "\b":
            return "<BackSpace>"
        case _:
            return char


def draw_title(
        canvas: tk.Canvas,
        y: int
) -> int:
    canvas.create_text(
        gui.Margins.LEFT.value + gui.GAP_SIZE, y,
        anchor="sw",
        fill=here.Colour.WHITE.value,
        font=(here.FONT, 64),
        text=mSweeper.SOFTWARE_TITLE
    )
    return 0


def draw_header(
        canvas: tk.Canvas,
        y: int,
        header_b_width: int,
        q_to_highscores: gui.Quit_context_lambda
) -> None:
    canvas.tag_bind(
        canvas.create_rectangle(
            gui.Margins.LEFT.value + header_b_width + gui.GAP_SIZE, y,
            gui.Margins.LEFT.value + header_b_width * 2 + gui.GAP_SIZE, y + gui.BOX_A,
            activeoutline="red",
            activewidth=3,
            fill=here.Colour.BACKGROUND.value
        ),
        "<Button-1>",  # TODO add RMB button consts
        q_to_highscores
    )

    here.draw_trophy(
        canvas,
        gui.Margins.LEFT.value + header_b_width + gui.GAP_SIZE, y,
        gui.BOX_A
    )

    canvas.create_text(
        gui.Margins.LEFT.value + header_b_width + gui.GAP_SIZE + gui.BOX_A,
        y + gui.BOX_A // 2,
        anchor="w",
        fill=here.Colour.WHITE.value,
        font=(here.FONT, here.Font_size.DEFAULT.value),
        state="disabled",
        text="Highscores"
    )

    return gui.BOX_A


def draw_diffs(
        canvas: tk.Canvas,
        y: int,
        diff_b_a: int,
        set_diff_and_quit: Callable[[mSweeper.Difficulty], None]
) -> int:
    def create_ctext(
            x_anchor: int,
            y_delta: int,
            font_size: int,
            text: str
    ) -> None:
        canvas.create_text(
            x_anchor + diff_b_a // 2,
            y + diff_b_a // 2 + y_delta,
            fill=here.Colour.WHITE.value,
            font=(here.FONT, font_size),
            state="disabled",
            text=text
        )

    e = "=="  # TODO

    for i, diff in enumerate(mSweeper.Difficulty):
        tmp_x_anchor = gui.Margins.LEFT.value + diff_b_a * i + gui.GAP_SIZE * i
        diff_dict = mSweeper.DIFFICULTY_DICT[diff]

        canvas.tag_bind(
            canvas.create_rectangle(
                tmp_x_anchor, y,
                tmp_x_anchor + diff_b_a, y + diff_b_a,
                fill=here.Colour.BACKGROUND.value,
                outline=here.Colour.BLACK.value,
                activeoutline="#ff0000",  # TODO remove colour strings
                activewidth=3
            ),
            "<Button-1>",  # TODO
            lambda _, d=diff: set_diff_and_quit(d)  # type: ignore # TODO lambda type
        )

        create_ctext(
            tmp_x_anchor, -80, 28,
            f'{e * 2} {str(diff).split(".")[1]} {e * 2}'
        )
        create_ctext(
            tmp_x_anchor, 0, 42,
            f'{diff_dict["width"]} x {diff_dict["height"]}'
        )
        create_ctext(
            tmp_x_anchor, 80, 28,
            f'{e} mines: {diff_dict["mines"]} {e}'
        )

    return diff_b_a


def draw_footer(
        canvas: tk.Canvas,
        y: int,
        width: int,
        height: int,
        q_to_help: gui.Quit_context_lambda
) -> int:
    qm_box_a = round(gui.BOX_A * (2 / 3))

    canvas.tag_bind(
        canvas.create_rectangle(
            gui.Margins.LEFT.value, y,
            gui.Margins.LEFT.value + qm_box_a, y + qm_box_a,
            activeoutline="red",
            fill=here.Colour.BACKGROUND.value
        ),
        "<Button-1>",  # TODO
        q_to_help
    )

    canvas.create_text(
        gui.Margins.LEFT.value + qm_box_a / 2, y + qm_box_a / 2,
        fill="#484848",
        font=(here.FONT, 22),
        state="disabled",
        text="?"
    )

    canvas.create_text(
        width - gui.Margins.RIGHT.value - gui.GAP_SIZE, height,
        anchor="se",
        fill="#484848",
        font=(here.FONT, 15),
        state="disabled",
        text="v" + mSweeper.SOFTWARE_VERSION
    )

    return qm_box_a
