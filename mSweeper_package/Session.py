from typing import Any, Dict, Optional

import mSweeper_package as here

from . import minesweeper as ms
from .data_management.highscores import Highscore_manager as Hs_manager
from .gui import Core


class Session:
    def __init__(
        self,
        ai_player: Optional[Any] = None  # TODO
    ) -> None:
        self.ai_player = ai_player

        self.hs_manager = Hs_manager.Highscore_manager()

        self.ms_waiting_for_win = True
        self.ms_scored_top_ten = False
        self.ms: Optional[ms.Minesweeper] = None
        self.ms_state = ms.Minesweeper_state.UNINITIALIZED
        self.ms_difficulty: Optional[here.Difficulty] = None
        self.ms_deets: Optional[Dict[str, int]] = None

        self.game_gui = Core.Gui(self, ai_player is None)

    def set_difficulty(
        self,
        diff: here.Difficulty
    ) -> None:
        self.ms_difficulty = diff
        self.ms_deets = here.DIFFICULTY_DICT[diff]

    def victory_routine(
        self
    ) -> None:
        assert self.ms is not None and self.ms_difficulty is not None

        print("\nVICTORY!")
        print("time:", self.ms.get_time(), "\n")

        nick = "hardcoded"
        x, y = self.hs_manager.score(self.ms.get_time(), nick, self.ms_difficulty)  # TODO
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

    ################################################

    def get_new_ms(
        self
    ) -> None:
        assert self.ms_deets is not None

        self.ms = ms.Minesweeper(
            (self.ms_deets["width"], self.ms_deets["height"]),
            self.ms_deets["mines"]
        )
        self._current_ms_lmb = self.ms.lmb
        self._current_ms_rmb = self.ms.rmb

        self.ms_scored_top_ten = False
        self.ms_waiting_for_win = True
        self.ms_state = ms.Minesweeper_state.UNINITIALIZED

    def ms_lmb(
        self,
        position: ms.Position_t
    ) -> None:
        assert self.ms is not None

        self.ms_click_wrapper(self._current_ms_lmb, position)
        self.ms_state = self.ms.get_state()

    def ms_rmb(
        self,
        position: ms.Position_t
    ) -> None:
        self.ms_click_wrapper(self._current_ms_rmb, position)
