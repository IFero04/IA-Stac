import pygame
from typing import Optional

from games.stac.action import StacAction
from games.stac.result import StacResult
from games.state import State
from games.stac.gui.display import StacDisplay


class StacState(State):
    EMPTY_CELL = -1
    START_CELL = 1


    def __init__(self, display_game:bool):
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
        track the last moved token 
        """
        self.__last_token_moved = [(None, None), (None, None)]
        """
        the display
        """
        self.__display_game = display_game
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
        Draw Counter
        """
        self.__draw_counter = 0

    def count_draw(self):
        tokens_in_game = 0
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                if self.__grid[row][col] == 1:
                    tokens_in_game += 1

        if tokens_in_game < 10 and self.__turns_count > 50:
            self.__draw_counter += 1

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
        if move_piece and self.__last_token_moved[self.__acting_player] == (pos_row, pos_col):
            return False

        return True

    def __add_play(self, row, col, move_piece):
        lord_row = None
        lord_col = None
        self.count_draw()
        for r in range(self.__num_rows):
            for c in range(self.__num_cols):
                if self.__lord_grid[r][c] == self.__acting_player:
                    lord_row = r
                    lord_col = c
                    self.__lord_grid[r][c] = -1
        self.__lord_grid[row][col] = self.__acting_player

        self.__last_token_moved[self.__acting_player] = (None, None)

        if move_piece:
            self.__grid[lord_row][lord_col] -= 1
            self.__grid[row][col] += 1
            self.__last_token_moved[self.__acting_player] = (row, col)
            if self.__grid[row][col] == 3:
                self.__grid[row][col] = -1 - self.__acting_player
                self.__draw_counter = 0

    def __count_tower(self, player):
        cont = 0
        player_value = -1 - player

        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                if self.__grid[row][col] == player_value:
                    cont += 1

        return cont

    def __check_winner(self):
        if self.__count_tower(self.__acting_player) >= 4:
            return True

        return False

    def __is_full(self):
        #print(f"DRAW: {self.__draw_counter}, Turnos: {self.__turns_count}")
        if self.__turns_count < 200:
            for row in range(self.__num_rows):
                for col in range(self.__num_cols):
                    if self.__grid[row][col] == 1:
                        return False

        towerP0 = self.__count_tower(0)
        towerP1 = self.__count_tower(1)
        if towerP0 > towerP1:
            self.__has_winner = True
            self.__winner = 0
        elif towerP1 > towerP0:
            self.__has_winner = True
            self.__winner = 1
        else:
            self.__has_winner = False
            self.__winner = -1

        return True

    def update(self, action: StacAction):
        row = action.get_row()
        col = action.get_col()
        move_piece = action.get_move_piece()

        # add the play
        self.__add_play(row, col, move_piece)

        # determine if there is a winner
        if self.__check_winner():
            self.__has_winner = True
            self.__winner = self.__acting_player

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def display(self):
        if pygame.display.get_init():
            self.__board.draw(self.__grid, self.__lord_grid)
            pygame.display.flip()

    def is_finished(self) -> bool:
        return self.__has_winner or self.__is_full()

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = StacState(False)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        cloned_state.__last_token_moved = self.__last_token_moved
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
                cloned_state.__lord_grid[row][col] = self.__lord_grid[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[StacResult]:
        if self.__has_winner:
            return StacResult.LOOSE if not(pos == self.__winner) else StacResult.WIN
        if self.__is_full():
            return StacResult.DRAW
        return None

    def get_grid(self):
        return self.__grid

    def get_lord_grid(self):
        return self.__lord_grid

    def get_turn(self):
        return self.__turns_count

    def get_num_players(self):
        return 2

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass

    def get_possible_actions(self):
        return list(
            filter(
                lambda action: self.validate_action(action),
                list(map(
                    lambda row_col: StacAction(row_col[0], row_col[1], 1),
                    [(row, col) for row in range(self.get_num_rows()) for col in range(self.get_num_cols())]
                )) +
                list(map(
                    lambda row_col: StacAction(row_col[0], row_col[1], 0),
                    [(row, col) for row in range(self.get_num_rows()) for col in range(self.get_num_cols())]
                ))
            )
        )

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
