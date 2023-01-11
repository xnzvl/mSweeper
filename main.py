from typing import Optional, Tuple, Dict
from datetime import date

import gui
import minesweeper as ms
import highscorer as hsm

import uber


Click_t = uber.mClick_t
Position_t = uber.mPosition_t
Difficulty_t = uber.mDifficulty_t
Dimensions_t = uber.mDimensions_t
Sweeper_state_t = uber.mSweeper_state_t
Ai_player_t = uber.mAI_player_t


DIMENSIONS = uber.DIMENSIONS
DIFFICULTY = uber.DEFAULT_DIFFICULTY
EASY, MEDIUM, HARD = uber.DIFFICULTY_VALUES

DIFFICULTY_SETTINGS: Dict[Difficulty_t, Tuple[int, Dimensions_t]] = {
    EASY: (10, (10, 10)),
    MEDIUM: (40, (16, 16)),
    HARD: (5, (30, 16))
}

DEFAULT_CYPHER = hsm.Cypher(
    hsm.default_cypher_encrypt,
    hsm.default_cypher_decrypt
)


class Session:
    def __init__(
        self,
        difficulty: Difficulty_t,
        ai_player: Optional[Ai_player_t] = None
    ) -> None:
        self.mines, self.dimensions = DIFFICULTY_SETTINGS[difficulty]

        self.mines = 5

        self.difficulty = difficulty
        self.ai_player = ai_player

        self._hs_manager = hsm.Highscores(uber.HIGHSCORE_FILE, DEFAULT_CYPHER)
        self._waiting_for_win = True

        self.game_gui = gui.Gui(self, ai_player is None)

    def _victory_routine(
        self
    ) -> None:
        assert self.ms is not None
        t = self.ms.get_time()
        print("VICTORY!")
        print("time:", t)

        self._hs_manager.score(
            (t, date.today().strftime("%Y-%m-%d"), "Kubik"), MEDIUM
        )

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
    session = Session(MEDIUM)
    print(session)


if __name__ == "__main__":
    main()
