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
        track last piece moved
        """
        self.__last_moved = [(int, int), (int, int)]
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
        pos_row = pos_col = None
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                if self.__lord_grid[row][col] == self.__acting_player:
                    pos_row = row
                    pos_col = col
        row = action.get_row()
        col = action.get_col()
        move_piece = action.get_move_piece()

        # valid column
        if col < 0 or col >= self.__num_cols:
            return False

        # valid line
        if row < 0 or row >= self.__num_rows:
            return False

        # vertically or horizontally movement
        if pos_row != row and pos_col != col:
            return False

        # player overlap
        if self.__lord_grid[row][col] != -1:
            return False

        # validate moving piece
        if move_piece and self.__grid[pos_row][pos_col] != 1:
            return False

        # validate tower
        if move_piece and (self.__grid[row][col] >= 3 or self.__grid[row][col] < 0):
            return False

        # validate move piece over player
        if move_piece and pos_col != col:
            step = 1 if col > pos_col else -1
            for check in range(pos_col + step, col, step):
                if self.__lord_grid[row][check] != -1:
                    return False

        if move_piece and pos_row != row:
            step = 1 if row > pos_row else -1
            for check in range(pos_row + step, row, step):
                if self.__lord_grid[check][col] != -1:
                    return False

        # validate move piece on consecutive turns
        if move_piece and (self.__last_moved[self.__acting_player][0] == row or self.__last_moved[self.__acting_player][1] == col):
            return False

        return True

    def __add_play(self, row, col, move_piece):
        lord_row = None
        lord_col = None
        for r in range(self.__num_rows):
            for c in range(self.__num_cols):
                if self.__lord_grid[r][c] == self.__acting_player:
                    lord_row = r
                    lord_col = c
                    self.__lord_grid[r][c] = -1
        self.__lord_grid[row][col] = self.__acting_player

        self.__last_moved[self.__acting_player] = (int, int)
        if move_piece:
            self.__grid[lord_row][lord_col] -= 1
            self.__grid[row][col] += 1
            self.__last_moved[self.__acting_player] = (row, col)
            if self.__grid[row][col] == 3:
                self.__grid[row][col] = -1 - self.__acting_player

    def update(self, action: StacAction):
        row = action.get_row()
        col = action.get_col()
        move_piece = action.get_move_piece()

        # add the play
        self.__add_play(row, col, move_piece)

        # determine if there is a winner
        if self.__is_full():
            self.__end_game = True

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def display(self):
        self.__board.draw(WIN, self.__grid, self.__lord_grid)
        pygame.display.update()

    def __is_full(self):
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                if self.__grid[row][col] == 1:
                    return False
        return True

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
