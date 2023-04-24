from typing import Dict, Optional

import mSweeper_package as here

import minesweeper as ms


class Session:
    def __init__(
        self,
        ai_player: Optional[u.mAI_player_t] = None  # TODO
    ) -> None:
        self.ai_player = ai_player
        self.waiting_for_win = True
        self.top_ten = False
        self.ms_state = ms.Minesweeper_state.UNINITIALIZED

        self.cnfg = fm.get_config()

        difficulties_dict = self.cnfg["DIFFICULTIES"]
        highscore_file = self.cnfg["HIGHSCORE_FILE"]

        assert isinstance(difficulties_dict, dict) \
            and isinstance(highscore_file, str)

        self.difficulty: Optional[here.Difficulty] = None
        self.deets: Optional[Dict[str, int]] = None

        self.hs_manager = fm.Highscores(highscore_file, DEFAULT_CYPHER)
        self.game_gui = gui.Gui(self, ai_player is None)

    def set_difficulty(
        self,
        diff: here.Difficulty
    ) -> None:
        self.difficulty = diff
        self.deets = DIFFICULTY_DICT[diff]

    def victory_routine(
        self
    ) -> None:
        assert self.ms is not None
        t = self.ms.get_time()
        print("\nVICTORY!")
        print("time:", t, "\n")

        nick = self.cnfg["NICK"]
        diff_str = self.cnfg["DEFAULT_DIFFICULTY"]
        assert isinstance(nick, str) and isinstance(diff_str, str)

        self.top_ten = self.hs_manager.score(t, nick, self.difficulty)
        self.waiting_for_win = False

    def ms_click_wrapper(
        self,
        click: u.mClick_t,
        position: u.mPosition_t
    ) -> None:
        click(position)

        assert self.ms is not None
        if self.ms.get_state() == ms.GAME_WON and self.waiting_for_win:
            self._victory_routine()

    ################################################

    def get_new_ms(
        self
    ) -> None:
        self.ms = ms.Minesweeper(
            (self.deets["width"], self.deets["height"]),
            self.deets["mines"]
        )
        self._current_ms_lmb = self.ms.lmb
        self._current_ms_rmb = self.ms.rmb

        self.waiting_for_win = True
        self.top_ten = False
        self.ms_state = ms.UNINITIALIZED

    def ms_lmb(
        self,
        position: u.mPosition_t
    ) -> None:
        self.ms_click_wrapper(self._current_ms_lmb, position)
        self.ms_state = self.ms.get_state()

    def ms_rmb(
        self,
        position: u.mPosition_t
    ) -> None:
        self.ms_click_wrapper(self._current_ms_rmb, position)
