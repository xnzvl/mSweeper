import contexts as here

import gui

import Context
import Core

import mSweeper_package as mSweeper


class Context_main_menu(Context.Context):
    def __init__(
            self,
            gui_core: Core.Gui,
            width: int,
            height: int
    ) -> None:

        def draw_title(
                y: int
        ) -> int:
            self.canvas.create_text(
                gui.Margins.LEFT + gui.GAP_SIZE, y,
                anchor="sw",
                fill=here.Colour.BLACK,
                font=(here.FONT, 64),
                text=SW_TITLE  # TODO
            )
            return 0

        def draw_header(
                y: int
        ) -> int:
            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    gui.Margins.LEFT + header_b_width + gui.GAP_SIZE, y,
                    gui.Margins.LEFT + header_b_width * 2 + gui.GAP_SIZE, y + gui.BOX_A,
                    activeoutline="red",
                    activewidth=3,
                    fill=here.Colour.BACKGROUND
                ),
                "<Button-1>",  # TODO add RMB button consts
                self.q_to_highscores
            )

            here.draw_trophy(
                self.canvas,
                gui.Margins.LEFT + header_b_width + gui.GAP_SIZE, y,
                gui.BOX_A
            )

            self.canvas.create_text(
                gui.Margins.LEFT + header_b_width + gui.GAP_SIZE + gui.BOX_A,
                y + gui.BOX_A // 2,
                anchor="w",
                fill=here.Colour.BLACK,
                font=(here.FONT, here.Font_size.DEFAULT),
                state="disabled",
                text="Highscores"
            )

            return gui.BOX_A

        def draw_diffs(
                y: int
        ) -> int:
            def create_ctext(
                x_anchor: int,
                y_delta: int,
                font_size: int,
                text: str
            ) -> None:
                self.canvas.create_text(
                    x_anchor + diff_b_a // 2,
                    y + diff_b_a // 2 + y_delta,
                    fill=here.Colour.BLACK,
                    font=(here.FONT, font_size),
                    state="disabled",
                    text=text
                )

            e = "=="  # TODO

            for i, diff in enumerate(mSweeper.Difficulty):
                tmp_x_anchor = gui.Margins.LEFT + diff_b_a * i + gui.GAP_SIZE * i
                diff_dict = mSweeper.DIFFICULTY_DICT[diff]

                self.canvas.tag_bind(
                    self.canvas.create_rectangle(
                        tmp_x_anchor, y,
                        tmp_x_anchor + diff_b_a, y + diff_b_a,
                        fill=here.Colour.BACKGROUND,
                        outline=here.Colour.BLACK,
                        activeoutline="#ff0000",  # TODO remove colour strings
                        activewidth=3
                    ),
                    "<Button-1>",
                    lambda _, d=diff: self.set_diff_and_quit(d)
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
                y: int
        ) -> int:
            qm_box_a = round(gui.BOX_A * (2 / 3))

            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    gui.Margins.LEFT, y,
                    gui.Margins.LEFT + qm_box_a, y + qm_box_a,
                    activeoutline="red",
                    fill=here.Colour.BACKGROUND
                ),
                "<Button-1>",
                self.q_to_help
            )

            self.canvas.create_text(
                gui.Margins.LEFT + qm_box_a / 2, y + qm_box_a / 2,
                fill="#484848",
                font=(here.FONT, 22),
                state="disabled",
                text="?"
            )

            self.canvas.create_text(
                width - gui.Margins.RIGHT - gui.GAP_SIZE, height,
                anchor="se",
                fill="#484848",
                font=(here.FONT, 15),
                state="disabled",
                text="v" + SW_VERSION  # TODO
            )

            return qm_box_a

        super().__init__(gui_core, width, height)

        header_b_width = (width - self.gui_core.hor_margin - gui.GAP_SIZE) // 2
        diff_b_a = (width - self.gui_core.hor_margin - 2 * gui.GAP_SIZE) // 3

        y_anchor = height - (3 * gui.GAP_SIZE + 2 * gui.BOX_A + diff_b_a)
        y_anchor += draw_title(y_anchor) + gui.GAP_SIZE
        y_anchor += draw_header(y_anchor) + gui.GAP_SIZE
        y_anchor += draw_diffs(y_anchor) + gui.GAP_SIZE
        y_anchor += draw_footer(y_anchor)

        if y_anchor > height - gui.Margins.BOTTOM:
            raise ValueError("Content out of bounds (margins)")

    def set_diff_and_quit(
            self,
            difficulty: mSweeper.Difficulty
    ) -> None:
        self.session.set_difficulty(difficulty)
        self.quit_context_for(here.Context.MINESWEEPER)
