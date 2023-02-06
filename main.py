from typing import Optional, Dict

import gui
import minesweeper as ms
import file_manager as fm

import uber


Click_t = uber.mClick_t
Context_t = uber.mContext_t
Position_t = uber.mPosition_t
Difficulty_t = uber.mDifficulty_t
Dimensions_t = uber.mDimensions_t
Sweeper_state_t = uber.mSweeper_state_t
Ai_player_t = uber.mAI_player_t


DEFAULT_CYPHER = fm.DEFAULT_CYPHER

EASY = uber.EASY
MEDIUM = uber.MEDIUM
HARD = uber.HARD

DIFFICULTY_DICT: Dict[Difficulty_t, Dict[str, int]] = {
    EASY: {
        "mines":  10,
        "width":   8,
        "height":  8
    },
    MEDIUM: {
        "mines":  40,
        "width":  16,
        "height": 16
    },
    HARD: {
        "mines":  99,
        "width":  30,
        "height": 16
    }
}


class Session:
    def __init__(
        self,
        ai_player: Optional[Ai_player_t] = None
    ) -> None:
        self.ai_player = ai_player
        self.waiting_for_win = True
        self.ms_state = ms.UNINITIALIZED

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

        # testing
        self.set_difficulty(MEDIUM)

        self.hs_manager = fm.Highscores(highscore_file, DEFAULT_CYPHER)
        self.game_gui = gui.Gui(self, ai_player is None)

    def set_difficulty(
        self,
        diff: Difficulty_t
    ) -> None:
        self.difficulty = diff

        for attr in ["mines", "width", "height"]:
            self.deets[attr] = DIFFICULTY_DICT[diff][attr]

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

        self.hs_manager.score(t, nick, self.difficulty)

    def _ms_click_wrapper(
        self,
        click: Click_t,
        position: Position_t
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

    def ms_lmb(
        self,
        position: Position_t
    ) -> None:
        self._ms_click_wrapper(self._current_ms_lmb, position)
        self.ms_state = self.ms.get_state()

    def ms_rmb(
        self,
        position: Position_t
    ) -> None:
        self._ms_click_wrapper(self._current_ms_rmb, position)


def main() -> None:
    session = Session()
    print(session)


if __name__ == "__main__":
    main()
