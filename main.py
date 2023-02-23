from typing import Optional, Dict

import gui
import minesweeper as ms
import file_manager as fm

import uber as u


DEFAULT_CYPHER = fm.DEFAULT_CYPHER

DIFFICULTY_DICT: Dict[u.mDifficulty_t, Dict[str, int]] = {
    u.EASY: {
        "mines":  10,
        "width":   8,
        "height":  8
    },
    u.MEDIUM: {
        "mines":  40,
        "width":  16,
        "height": 16
    },
    u.HARD: {
        "mines":  99,
        "width":  30,
        "height": 16
    }
}


class Session:
    def __init__(
        self,
        ai_player: Optional[u.mAI_player_t] = None
    ) -> None:
        self.ai_player = ai_player
        self.waiting_for_win = True
        self.top_ten = False

        self.cnfg = fm.get_config()

        current_diff_str = self.cnfg["DEFAULT_DIFFICULTY"]
        difficulties_dict = self.cnfg["DIFFICULTIES"]
        highscore_file = self.cnfg["HIGHSCORE_FILE"]

        assert isinstance(current_diff_str, str) \
            and isinstance(difficulties_dict, dict) \
            and isinstance(highscore_file, str)

        self.difficulty = 0
        self.deets: Dict[str, int] = {
            "mines":   0,
            "width":   0,
            "height":  0
        }

        self.hs_manager = fm.Highscores(highscore_file, DEFAULT_CYPHER)
        self.game_gui = gui.Gui(self, ai_player is None)

    def set_difficulty(
        self,
        diff: u.mDifficulty_t
    ) -> None:
        self.difficulty = diff
        self.deets = DIFFICULTY_DICT[diff]

    def _victory_routine(
        self
    ) -> None:
        assert self.ms is not None
        t = self.ms.get_time()
        print("\nVICTORY!")
        print("time:", t)

        nick = self.cnfg["NICK"]
        diff_str = self.cnfg["DEFAULT_DIFFICULTY"]
        assert isinstance(nick, str) and isinstance(diff_str, str)

        self.top_ten = self.hs_manager.score(t, nick, self.difficulty)
        self.waiting_for_win = False

    def _ms_click_wrapper(
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

    def ms_lmb(
        self,
        position: u.mPosition_t
    ) -> None:
        self._ms_click_wrapper(self._current_ms_lmb, position)
        self.ms_state = self.ms.get_state()

    def ms_rmb(
        self,
        position: u.mPosition_t
    ) -> None:
        self._ms_click_wrapper(self._current_ms_rmb, position)


def main() -> None:
    session = Session()
    print(session)


if __name__ == "__main__":
    main()
