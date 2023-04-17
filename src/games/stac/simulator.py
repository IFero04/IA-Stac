from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.game_simulator import GameSimulator

class StacSimulator(GameSimulator):

    def __init__(self, player1: StacPlayer, player2: StacPlayer):
        super(StacSimulator, self).__init__([player1, player2])

    def init_game(self):
        return StacState()

    def before_end_game(self, state: StacState):
        # ignored for this simulator
        pass

    def end_game(self, state: StacState):
        # ignored for this simulator
        pass
