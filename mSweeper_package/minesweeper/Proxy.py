from typing import Optional

import mSweeper_package.Details as Details
import mSweeper_package.minesweeper as ms
import mSweeper_package.minesweeper.Minesweeper as Minesweeper


class Minesweeper_proxy:
    def __init__(
            self,
            info_blob: Details.Info_blob
    ) -> None:
        self.info_blob = info_blob
        self.ms: Optional[Minesweeper.Minesweeper] = None

        self.new_minesweeper()

    def new_minesweeper(
            self
    ) -> None:
        ms_details = self.info_blob

        ms_details.ms_top_ten = False
        ms_details.ms_win_waiting = True
        ms_details.ms_state = ms.Minesweeper_state.UNINITIALIZED

        self.ms = Minesweeper.Minesweeper(
            (ms_details.ms_config["width"], ms_details.ms_config["height"]),
            ms_details.ms_config["mines"]
        )

    def victory_routine(
        self
    ) -> None:
        assert self.ms is not None

        print("\nVICTORY!")
        print("time:", self.ms.get_time(), "\n")

        nick = "hardcoded"
        x, y = self.info_blob.hs_manager.score(self.ms.get_time(), nick, self.info_blob.ms_difficulty)
        self.ms_scored_top_ten = x is not None or y is not None

        self.ms_waiting_for_win = False

    def ms_click_wrapper(
        self,
        click: ms.Click_t,
        position: ms.Position_t
    ) -> None:
        click(position)

        assert self.ms is not None
        if self.ms.get_state() == ms.Minesweeper_state.GAME_WON and self.ms_waiting_for_win:
            self.victory_routine()

    def ms_lmb(
        self,
        position: ms.Position_t
    ) -> None:
        assert self.ms is not None

        self.ms_click_wrapper(self.ms.lmb, position)
        self.ms_state = self.ms.get_state()

    def ms_rmb(
        self,
        position: ms.Position_t
    ) -> None:
        assert self.ms is not None

        self.ms_click_wrapper(self.ms.rmb, position)
