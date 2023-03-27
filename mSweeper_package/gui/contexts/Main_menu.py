from .. import contexts as here
from .. import Context, Core

from .... import mSweeper_package as mSweeper


class C_main_menu(Context.Context):
    def __init__(
        self,
        gui_root: Core.Gui,
        width: int,
        height: int
    ) -> None:
        def draw_title(
            y: int
        ) -> int:
            self.canvas.create_text(
                MARGINS["left"] + GAP_SIZE, y,
                anchor="sw",
                fill=COLOUR_FONT,
                font=(DEF_FONT, 64),
                text=SW_TITLE
            )
            return 0

        def draw_header(
            y: int
        ) -> int:
            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    MARGINS["left"] + header_b_width + GAP_SIZE, y,
                    MARGINS["left"] + header_b_width * 2 + GAP_SIZE, y + BOX_A,
                    activeoutline="red",
                    activewidth=3,
                    fill=COLOUR_BACKGROUND
                ),
                "<Button-1>",
                self.q_to_highscores
            )

            here.draw_trophy(
                self.canvas,
                MARGINS["left"] + header_b_width + GAP_SIZE, y,
                BOX_A
            )

            self.canvas.create_text(
                MARGINS["left"] + header_b_width + GAP_SIZE + BOX_A,
                y + BOX_A // 2,
                anchor="w",
                fill=COLOUR_FONT,
                font=(DEF_FONT, DEF_FONT_SIZE),
                state="disabled",
                text="Highscores"
            )

            return BOX_A

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
                    fill=COLOUR_FONT,
                    font=(DEF_FONT, font_size),
                    state="disabled",
                    text=text
                )

            e = "=="

            for i, diff in enumerate(mSweeper.Difficulty_t):
                tmp_x_anchor = MARGINS["left"] + diff_b_a * i + GAP_SIZE * i
                diff_dict = main.DIFFICULTY_DICT[diff]

                self.canvas.tag_bind(
                    self.canvas.create_rectangle(
                        tmp_x_anchor, y,
                        tmp_x_anchor + diff_b_a, y + diff_b_a,
                        fill=COLOUR_BACKGROUND,
                        outline=COLOUR_BLACK,
                        activeoutline="#ff0000",
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
            qm_box_a = round(BOX_A * (2 / 3))

            self.canvas.tag_bind(
                self.canvas.create_rectangle(
                    MARGINS["left"], y,
                    MARGINS["left"] + qm_box_a, y + qm_box_a,
                    activeoutline="red",
                    fill=COLOUR_BACKGROUND
                ),
                "<Button-1>",
                self.q_to_help
            )

            self.canvas.create_text(
                MARGINS["left"] + qm_box_a / 2, y + qm_box_a / 2,
                fill="#484848",
                font=(DEF_FONT, 22),
                state="disabled",
                text="?"
            )

            self.canvas.create_text(
                width - MARGINS["right"] - GAP_SIZE, height,
                anchor="se",
                fill="#484848",
                font=(DEF_FONT, 15),
                state="disabled",
                text="v" + SW_VERSION
            )

            return qm_box_a

        super().__init__(gui_root, width, height)

        header_b_width = (width - self.gui_root.hor_margin - GAP_SIZE) // 2
        diff_b_a = (width - self.gui_root.hor_margin - 2 * GAP_SIZE) // 3

        y_anchor = height - (3 * GAP_SIZE + 2 * BOX_A + diff_b_a)
        y_anchor += draw_title(y_anchor) + GAP_SIZE
        y_anchor += draw_header(y_anchor) + GAP_SIZE
        y_anchor += draw_diffs(y_anchor) + GAP_SIZE
        y_anchor += draw_footer(y_anchor)

        if y_anchor > height - MARGINS["bottom"]:
            raise ValueError("Content out of bounds (margins)")

    def set_diff_and_quit(
        self,
        difficulty: mSweeper.Difficulty_t
    ) -> None:
        self.session.set_difficulty(difficulty)
        self.quit_context_for(here.Context_t.MINESWEEPER)
