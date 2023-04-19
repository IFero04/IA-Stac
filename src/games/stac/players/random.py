from random import randint

from games.stac.action import StacAction
from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.state import State


class RandomStacPlayer(StacPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: StacState):
        return StacAction(
            randint(0, state.get_num_cols()),
            randint(0, state.get_num_cols()),
            randint(0, 1)
        )

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
