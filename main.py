from typing import Optional, Literal
from minesweeper import Minesweeper
import gui

import uber


Click_t = uber.mClick_t
Position_t = uber.mPosition_t
Difficulty_t = uber.mDifficulty_t
Ai_player_t = uber.mAI_player_t


DIMENSIONS = uber.DIMENSIONS
DIFFICULTY = uber.DEFAULT_DIFFICULTY
EASY, MEDIUM, HARD = uber.DIFFICULTY_VALUES


class Session:
    def __init__(
        self,
        difficulty: Difficulty_t,
        ai_player: Optional[Ai_player_t] = None
    ) -> None:
        self.difficulty = difficulty
        self.ai_player = ai_player
        self.dimensions = DIMENSIONS[difficulty]

        self.gui = gui.Gui(self, True)

    def new_game(
        self
    ) -> Literal[2, 3]:  # GAME_LOST = 2, GAME_WON = 3
        self.gui.start_mainloop()

    def _get_new_ms(
        self
    ) -> Minesweeper:
        print("create_new_ms()")

        self.ms = Minesweeper(self.dimensions)
        self.lmb = self.ms.cell_LMB
        self.rmb = self.ms.cell_RMB

        # testing
        self.lmb = lambda _: print("LMB")
        self.rmb = lambda _: print("RMB")

        return self.ms


def main() -> None:
    session = Session(MEDIUM)
    print(session.new_game())


if __name__ == "__main__":
    main()
