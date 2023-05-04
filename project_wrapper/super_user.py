from typing import Dict, List

import tkinter as tk
import sys

import mSweeper_package as mSweeper


UNIT = 25


class customize:
    def __init__(
            self
    ) -> None:
        self.diff_bs: Dict[mSweeper.Difficulty, tk.Button] = {}

        self.mine_entry = None
        self.save_b = None

        self.delete_flags: Dict[mSweeper.Difficulty, List[bool]] = {
            mSweeper.Difficulty.EASY:   [False for _ in range(10)],
            mSweeper.Difficulty.MEDIUM: [False for _ in range(10)],
            mSweeper.Difficulty.HARD:   [False for _ in range(10)]
        }


def init_super_user() -> None:
    if sys.argv[1] != "custom":
        print("[!] CUSTOM mSweeper INITIATION FAILED")
        print("[i] running classic mSweeper")
        return

    custom()


def draw_diffs(
        root: tk.Tk
) -> None:
    for i, diff in enumerate(mSweeper.Difficulty):
        button = tk.Button(root, text=diff.value)
        button.place(
            x=UNIT, y=UNIT + i * 5 * UNIT,
            width=5 * UNIT, height=4 * UNIT
        )


def draw_highscores(
        root: tk.Tk
) -> None:
    for i in range(10):
        score_label = tk.Label(root, text=str(i))
        score_label.config(background="silver")
        score_label.place(
                x=7 * UNIT, y=UNIT + i * UNIT,
                width=7 * UNIT, height=UNIT
            )

        tk.Button(root, text="X") \
            .place(
                x=14 * UNIT, y=UNIT + i * UNIT,
                width=UNIT, height=UNIT
            )


def draw_config(
        root: tk.Tk
) -> None:
    tk.Label(root, text="mines:") \
        .place(
            x=7 * UNIT, y=12 * UNIT,
            width=4 * UNIT, height=UNIT
        )

    mines_entry = tk.Entry(root)
    mines_entry.insert(0, "dunno")
    mines_entry.place(
        x=11 * UNIT, y=12 * UNIT,
        width=4 * UNIT, height=UNIT
    )


def draw_save(
        root: tk.Tk
) -> None:
    save_button = tk.Button(root, text="Save")
    save_button.place(
        x=7 * UNIT, y=14 * UNIT,
        width=8 * UNIT, height=UNIT
    )


def draw_exit(
        root: tk.Tk
) -> None:
    exit_button = tk.Button(root, text=mSweeper.SOFTWARE_TITLE)
    exit_button.place(
        x=UNIT, y=16 * UNIT,
        width=14 * UNIT, height=UNIT
    )


def custom() -> None:
    root = tk.Tk()
    root.geometry(f"{16 * UNIT}x{18 * UNIT}")
    root.resizable(False, False)
    root.title("Customize")

    draw_diffs(root)
    draw_highscores(root)
    draw_config(root)
    draw_save(root)
    draw_exit(root)

    root.mainloop()
