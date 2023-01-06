from typing import Optional

import gui
import minesweeper as ms

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
        self.dimensions = DIMENSIONS[difficulty]
        self.difficulty = difficulty
        self.ai_player = ai_player

        self.gui = gui.Gui(self, True)
        self.ms = None
        self.lmb = None
        self.rmb = None

    def game_over(
        self
    ) -> None:
        pass

    def get_new_ms(
        self
    ) -> ms.Minesweeper:
        print("create_new_ms()")

        self.ms = ms.Minesweeper(self.dimensions, 40)
        self.lmb = self.ms.lmb
        self.rmb = self.ms.rmb

        # # testing
        # self.lmb = lambda _: print("LMB")
        # self.rmb = lambda _: print("RMB")

        return self.ms


def main() -> None:
    session = Session(MEDIUM)
    print(session)


if __name__ == "__main__":
    main()
