import pygame
from typing import Optional

from games.stac.action import StacAction
from games.stac.result import StacResult
from games.state import State
from games.stac.gui.constants import WIDTH, HEIGHT
from games.stac.gui.display import StacDisplay

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Stac')


class StacState(State):
    EMPTY_CELL = -1
    START_CELL = 1

    def __init__(self):
        super().__init__()
        """
        the dimensions of the board
        """
        self.__num_rows = 5
        self.__num_cols = 5
        """
        the player character
        """
        self.__lord_grid = [[StacState.EMPTY_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]
        self.__lord_grid[0][0] = 1
        self.__lord_grid[4][4] = 0
        """
        the grid
        """
        self.__grid = [[StacState.START_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]
        """
         the display
        """
        self.__board = StacDisplay()
        """
        counts the number of turns in the current games
        """
        self.__turns_count = 1
        """
        the index of the current acting player
        """
        self.__acting_player = 0
        """
        determine if a winner was found already 
        """
        self.__has_winner = False
        """
        jogador vencedor
        """
        self.__winner = -1
        """
        End Gane
        """
        self.__end_game = False


    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_grid(self, row, col):
        if row >= 0 and col >= 0:
            if row < self.__num_rows and col < self.__num_cols:
                return self.__grid[row][col]
        return 404

    def validate_action(self, action: StacAction) -> bool:
        col = action.get_col()
        row = action.get_row()

        # valid column
        if col < 0 or col >= self.__num_cols:
            return False
        # valid line
        if row < 0 or row >= self.__num_rows:
            return False

        return True

    def update(self, action: StacAction):
        col = action.get_col()
        row = action.get_row()

        # add the play
        self.__lord_grid[row][col] = self.__acting_player

        # determine if there is a winner
        if True:
            self.__end_game = False

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def display(self):
        self.__board.draw(WIN, self.__grid, self.__lord_grid)
        pygame.display.update()

    def __is_full(self):
        pass

    def is_finished(self) -> bool:
        return self.__end_game

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = StacState()
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
                cloned_state.__lord_grid[row][col] = self.__lord_grid[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[StacResult]:
        if self.__end_game:
            if self.__has_winner:
                return StacResult.LOOSE if not (pos == self.__winner) else StacResult.WIN
            else:
                return StacResult.DRAW
        return None

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass

    def get_possible_actions(self):
        return list(filter(
            lambda action: self.validate_action(action),
            map(
                lambda row_col: StacAction(row_col[0], row_col[1]),
                [(row, col) for row in range(self.get_num_rows()) for col in range(self.get_num_cols())]
            )
        ))

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
