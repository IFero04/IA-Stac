from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.game_simulator import GameSimulator

class StacSimulator(GameSimulator):

    def __init__(self, player1: StacPlayer, player2: StacPlayer, display_game: bool):
        self.display_game = display_game
        super(StacSimulator, self).__init__([player1, player2], self.display_game)

    def init_game(self):
        return StacState(self.display_game)

    def before_end_game(self, state: StacState):
        # ignored for this simulator
        pass

    def end_game(self, state: StacState):
        # ignored for this simulator
        pass
