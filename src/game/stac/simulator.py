from game.stac.player import StacPlayer
from game.stac.state import StacState
from game.game_simulator import GameSimulator

class StacSimulator(GameSimulator):

    def __init__(self, player1: StacPlayer, player2: StacPlayer, dimension: int):
        super(StacSimulator, self).__init__([player1, player2])
        """
        the number of rows and cols from the TicTacToe grid
        """
        self.__dimension = dimension

    def init_game(self):
        return StacState(self.__dimension)

    def before_end_game(self, state: StacState):
        # ignored for this simulator
        pass

    def end_game(self, state: StacState):
        # ignored for this simulator
        pass

    def get_dimension(self):
        return self.__dimension