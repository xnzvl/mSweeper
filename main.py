from typing import Optional, Dict

import gui
import minesweeper as ms
import file_manager as fm

import uber


Click_t = uber.mClick_t
Position_t = uber.mPosition_t
Difficulty_t = uber.mDifficulty_t
Dimensions_t = uber.mDimensions_t
Sweeper_state_t = uber.mSweeper_state_t
Ai_player_t = uber.mAI_player_t


DEFAULT_CYPHER = fm.DEFAULT_CYPHER

EASY = uber.EASY
MEDIUM = uber.MEDIUM
HARD = uber.HARD


DIFFICULTY_CONSTANTS: Dict[str, Difficulty_t] = {
    "EASY": EASY,
    "MEDIUM": MEDIUM,
    "HARD": HARD
}


class Session:
    def __init__(
        self,
        ai_player: Optional[Ai_player_t] = None
    ) -> None:
        self.ai_player = ai_player
        self._waiting_for_win = True

        self._cnfg = fm.get_config()

        current_diff_str = self._cnfg["DEFAULT_DIFFICULTY"]
        difficulties_dict = self._cnfg["DIFFICULTIES"]
        highscore_file = self._cnfg["HIGHSCORE_FILE"]

        assert isinstance(current_diff_str, str) \
            and isinstance(difficulties_dict, dict) \
            and isinstance(highscore_file, str)

        field_config = difficulties_dict[current_diff_str]

        self.mines = field_config["mines"]
        self.dimensions: Dimensions_t = (
            field_config["width"],
            field_config["height"]
        )

        self._hs_manager = fm.Highscores(highscore_file, DEFAULT_CYPHER)
        self.game_gui = gui.Gui(self, ai_player is None)

    def _victory_routine(
        self
    ) -> None:
        assert self.ms is not None
        t = self.ms.get_time()
        print("\nVICTORY!")
        print("time:", t)

        nick = self._cnfg["NICK"]
        diff_str = self._cnfg["DEFAULT_DIFFICULTY"]
        assert isinstance(nick, str) and isinstance(diff_str, str)

        self._hs_manager.score(t, nick, DIFFICULTY_CONSTANTS[diff_str])

    def _ms_click_wrapper(
        self,
        click: Click_t,
        position: Position_t
    ) -> None:
        click(position)

        assert self.ms is not None
        if self.ms.get_state() == ms.GAME_WON and self._waiting_for_win:
            self._victory_routine()

    ################################################

    def get_new_ms(
        self
    ) -> None:
        self.ms = ms.Minesweeper(self.dimensions, self.mines)
        self._current_ms_lmb = self.ms.lmb
        self._current_ms_rmb = self.ms.rmb
        self._waiting_for_win = True

    def ms_lmb(
        self,
        position: Position_t
    ) -> None:
        self._ms_click_wrapper(self._current_ms_lmb, position)

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
