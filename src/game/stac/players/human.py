from game.stac.action import StacAction
from game.stac.player import StacPlayer
from game.stac.state import StacState


class HumanStacPlayer(StacPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: StacState):
        state.display()
        while True:
            # noinspection PyBroadException
            try:
                cords = list(map(int, input(f"Player {state.get_acting_player()}, choose a column and a row: ").split(' ', 2)))

                return StacAction(cords[0] - 1, cords[1] - 1)
            except Exception:
                continue

    def event_action(self, pos: int, action, new_state: StacState):
        # ignore
        pass

    def event_end_game(self, final_state: StacState):
        # ignore
        pass
