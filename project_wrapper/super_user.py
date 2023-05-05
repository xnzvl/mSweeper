import tkinter as tk
import sys

import mSweeper_package as mSweeper
import mSweeper_package.data_management.highscores as highscores
import mSweeper_package.data_management.highscores.Load as Load
import mSweeper_package.data_management.highscores.Write as Write


UNIT = 26


def init_super_user() -> None:
    if sys.argv[1] != "custom":
        print("[!] CUSTOM mSweeper INITIATION FAILED")
        print("[i] running classic mSweeper")
        return

    Customize()


class Customize:
    def __init__(
            self
    ) -> None:
        self.width_in_units = 24

        self.root = tk.Tk()
        self.root.geometry(f"{self.width_in_units * UNIT}x{18 * UNIT}")
        self.root.resizable(False, False)
        self.root.title("Customize")

        self.remove_flags = [False for _ in range(10)]

        self.current_diff = mSweeper.Difficulty.MEDIUM

        self.score_book = Load.load_score_book()

        self.refresh()

        self.root.mainloop()

    def set_current_diff(
            self,
            diff: mSweeper.Difficulty
    ) -> None:
        self.current_diff = diff
        self.remove_flags = [False for _ in range(10)]
        self.refresh()

    def refresh(
            self
    ) -> None:
        for widget in self.root.place_slaves():
            widget.destroy()

        self.draw_diffs()
        self.draw_highscores()
        self.draw_config()
        self.draw_save()
        self.draw_exit()

    def draw_diffs(
            self
    ) -> None:
        for i, diff in enumerate(mSweeper.Difficulty):
            button = tk.Button(self.root, text=diff.value, command=lambda d=diff: self.set_current_diff(d))
            button.place(
                x=UNIT, y=UNIT + i * 5 * UNIT,
                width=5 * UNIT, height=4 * UNIT
            )

            if diff == self.current_diff:
                tk.Label(self.root, state="disabled", background="white") \
                    .place(
                        x=1 * UNIT, y=2 * UNIT + i * 5 * UNIT,
                        width=0.5 * UNIT, height=2 * UNIT
                    )

    def draw_highscores(
            self
    ) -> None:
        def format(
                score: highscores.Score_record_t
        ) -> str:
            time_tuple, date, nick = score
            h, m, s, _ = time_tuple
            return "{:02d}:{:02d}:{:02d}".format(h, m, s) + f" - {date} - {nick}"

        def set_flag(
                pos: int,
                score: tk.Label
        ) -> None:
            self.remove_flags[pos] = not self.remove_flags[pos]
            score.config(background="red" if self.remove_flags[pos] else "silver")

        for i in range(10):
            active = i < len(self.score_book[self.current_diff])

            text = format(self.score_book[self.current_diff][i]) \
                if active \
                else "---"

            score_label = tk.Label(self.root, text=text)
            score_label.config(borderwidth=1, relief="raised", background="silver")
            score_label.place(
                x=7 * UNIT, y=UNIT + i * UNIT,
                width=(self.width_in_units - 9) * UNIT, height=UNIT
            )

            tk.Button(
                self.root,
                text="X",
                state="active" if active else "disabled",
                command=lambda pos=i, score=score_label: set_flag(pos, score),
                background="silver"
            ) \
                .place(
                    x=(self.width_in_units - 2) * UNIT, y=UNIT + i * UNIT,
                    width=UNIT, height=UNIT
                )

    def draw_config(
            self
    ) -> None:
        tk.Label(self.root, text="width:", anchor="w") \
            .place(
                x=7 * UNIT, y=13 * UNIT,
                width=3 * UNIT, height=UNIT
            )
        tk.Label(self.root, text=mSweeper.DIFFICULTY_DICT[self.current_diff]["width"], anchor="w") \
            .place(
                x=11 * UNIT, y=13 * UNIT,
                width=3 * UNIT, height=UNIT
            )

        tk.Label(self.root, text="height:", anchor="w") \
            .place(
                x=7 * UNIT, y=14 * UNIT,
                width=3 * UNIT, height=UNIT
            )
        tk.Label(self.root, text=mSweeper.DIFFICULTY_DICT[self.current_diff]["height"], anchor="w") \
            .place(
                x=11 * UNIT, y=14 * UNIT,
                width=3 * UNIT, height=UNIT
            )

        tk.Label(self.root, text="mines:", anchor="w") \
            .place(
                x=7 * UNIT, y=12 * UNIT,
                width=3 * UNIT, height=UNIT
            )
        mines_entry = tk.Entry(self.root)
        mines_entry.insert(0, mSweeper.DIFFICULTY_DICT[self.current_diff]["mines"])
        mines_entry.place(
            x=10 * UNIT, y=12 * UNIT,
            width=4 * UNIT, height=UNIT
        )

        self.mines_entry = mines_entry

    def draw_save(
            self
    ) -> None:
        def save() -> None:
            for i, remove in enumerate(reversed(self.remove_flags)):
                if remove:
                    self.score_book[self.current_diff].pop(9 - i)
            Write.write_score_book(self.score_book)

            mDict = mSweeper.DIFFICULTY_DICT[self.current_diff]
            entry_amount = self.mines_entry.get()

            try:
                entry_amount = int(self.mines_entry.get())

                if 0 < entry_amount and entry_amount < mDict["width"] * mDict["height"] - 9:
                    mDict["mines"] = entry_amount
            except Exception:
                pass

            self.refresh()

        save_button = tk.Button(self.root, text="Save", command=save)
        save_button.place(
            x=15 * UNIT, y=12 * UNIT,
            width=(self.width_in_units - 16) * UNIT, height=3 * UNIT
        )

    def draw_exit(
            self
    ) -> None:
        exit_button = tk.Button(
            self.root,
            text=mSweeper.SOFTWARE_TITLE,
            command=self.root.destroy
        )
        exit_button.place(
            x=UNIT, y=16 * UNIT,
            width=(self.width_in_units - 2) * UNIT, height=UNIT
        )
