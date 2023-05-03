from typing import Any, Optional

import mSweeper_package.Details as Details
import mSweeper_package.gui.Core as Core
import mSweeper_package.data_management.Nick_manager as Nick_manager
import mSweeper_package.data_management.highscores.Highscore_manager as Hs_manager


class Session:
    def __init__(
        self,
        ai_player: Optional[Any] = None  # TODO
    ) -> None:
        self.ai_player = ai_player

        self.hs_manager = Hs_manager.Highscore_manager()
        self.details_blob = Details.Info_blob(ai_player, self.hs_manager)

        self.game_gui = Core.Gui(self.details_blob, ai_player is None)

        Nick_manager.write_nickname(self.details_blob.player_nick)
