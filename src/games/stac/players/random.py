from random import randint

from game.stac.action import StacAction
from game.stac.player import StacPlayer
from game.stac.state import StacState
from game.state import State


class RandomTicTacToePlayer(StacPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: StacState):
        return StacAction(
            randint(0, state.get_num_cols()),
            randint(0, state.get_num_cols())
        )

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
