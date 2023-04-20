from random import choice, randint

from games.stac.action import StacAction
from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.state import State


class RandomStacPlayer(StacPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: StacState):
        action = choice(state.get_possible_actions())
        return StacAction(
            action.get_row(), action.get_col(), action.get_move_piece()
        )

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
