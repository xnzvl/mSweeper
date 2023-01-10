from typing import Optional, Tuple, Dict

import gui
import minesweeper as ms

import uber


Click_t = uber.mClick_t
Position_t = uber.mPosition_t
Difficulty_t = uber.mDifficulty_t
Dimensions_t = uber.mDimensions_t
Ai_player_t = uber.mAI_player_t


DIMENSIONS = uber.DIMENSIONS
DIFFICULTY = uber.DEFAULT_DIFFICULTY
EASY, MEDIUM, HARD = uber.DIFFICULTY_VALUES

DIFFICULTY_SETTINGS: Dict[Difficulty_t, Tuple[int, Dimensions_t]] = {
    EASY: (10, (10, 10)),
    MEDIUM: (40, (16, 16)),
    HARD: (5, (30, 16))
}


class Session:
    def __init__(
        self,
        difficulty: Difficulty_t,
        ai_player: Optional[Ai_player_t] = None
    ) -> None:
        self.mines, self.dimensions = DIFFICULTY_SETTINGS[difficulty]
        self.difficulty = difficulty
        self.ai_player = ai_player

        self.gui = gui.Gui(self, ai_player is None)
        self.ms: Optional[ms.Minesweeper] = None

    def game_over(
        self
    ) -> None:
        pass

    def get_new_ms(
        self
    ) -> ms.Minesweeper:
        self.ms = ms.Minesweeper(self.dimensions, self.mines)
        return self.ms


def main() -> None:
    session = Session(MEDIUM)
    print(session)


if __name__ == "__main__":
    main()
