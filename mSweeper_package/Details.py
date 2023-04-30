from typing import Any, Dict, Optional

import mSweeper_package.minesweeper as here

import mSweeper_package as mSweeper
import mSweeper_package.data_management.highscores.Highscore_manager as Hs_manager


class Info_blob:
    def __init__(
            self,
            ai_player: Optional[Any],
            hs_manager: Hs_manager.Highscore_manager
    ) -> None:
        self.ai_player = ai_player

        self.hs_manager = hs_manager

        self.ms_config: Dict[str, int] = {}
        self.ms_difficulty = mSweeper.Difficulty.MEDIUM
        self.ms_state = here.Minesweeper_state.UNINITIALIZED
        self.ms_top_ten = False
        self.ms_win_waiting = True

    def set_difficulty(
        self,
        diff: mSweeper.Difficulty
    ) -> None:
        self.ms_difficulty = diff
        self.ms_config = mSweeper.DIFFICULTY_DICT[diff]
