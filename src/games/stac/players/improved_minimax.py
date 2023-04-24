import pygame
import math

from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.stac.result import StacResult
from games.state import State
from games.stac.action import StacAction


class ImprovedMinimaxStacPlayer(StacPlayer):
    def __init__(self, name):
        super().__init__(name)

    def __heuristic(self, state: StacState):
        grid = state.get_grid()
        player = -1 - self.get_current_pos()
        player_stacks = 0
        opponent_player = -2 if player == -1 else -1
        opponent_stacks = 0
        unclaimed_stacks = 0

        for row in range(0, state.get_num_rows()):
            for col in range(0, state.get_num_cols()):
                if grid[row][col] == player:
                    player_stacks += 1
                elif grid[row][col] == opponent_player:
                    opponent_stacks += 1
                elif grid[row][col] == 2:
                    unclaimed_stacks += 1

        value = (player_stacks - opponent_stacks) + (unclaimed_stacks / 10)

        lord_grid = state.get_lord_grid()
        lord_row = 0
        lord_col = 0
        opponent_lord_row = 0
        opponent_lord_col = 0

        for row in range(0, state.get_num_rows()):
            for col in range(0, state.get_num_cols()):
                if lord_grid[row][col] == self.get_current_pos():
                    lord_row = row
                    lord_col = col
                elif lord_grid[row][col] == 0 if self.get_current_pos() == 1 else 1:
                    opponent_lord_row = row
                    opponent_lord_col = col

        # Check for a winning move by the player
        if grid[lord_row][lord_col] == 1 and player_stacks == 3:
            for check in range(0, state.get_num_rows()):
                if grid[check][lord_col] == 2:
                    action = list(map(int, (check, lord_col, 1)))
                    if state.validate_action(StacAction(action[0], action[1], action[2])):
                        return 100

            for check in range(0, state.get_num_cols()):
                if grid[lord_row][check] == 2:
                    action = list(map(int, (lord_row, check, 1)))
                    if state.validate_action(StacAction(action[0], action[1], action[2])):
                            return 100

        # Check for a winning move by the opponent
        if grid[opponent_lord_row][opponent_lord_col] == 1 and opponent_stacks == 3:
            for check in range(0, state.get_num_rows()):
                if grid[check][opponent_lord_col] == 2:
                    action = list(map(int, (check, opponent_lord_col, 1)))
                    if state.validate_action(StacAction(action[0], action[1], action[2])):
                        return -100

            for check in range(0, state.get_num_cols()):
                if grid[opponent_lord_row][check] == 2:
                    action = list(map(int, (opponent_lord_row, check, 1)))
                    if state.validate_action(StacAction(action[0], action[1], action[2])):
                        return -100

        return value

    def minimax(self, state: StacState, depth: int, alpha: int = -math.inf, beta: int = math.inf,
                is_initial_node: bool = True):
        if state.is_finished():
            return {
                StacResult.WIN: 40,
                StacResult.LOOSE: -40,
                StacResult.DRAW: 0
            }[state.get_result(self.get_current_pos())]

        if depth == 0:
            print(f"VALOR JOGADA: {self.__heuristic(state)}")
            return self.__heuristic(state)

        if self.get_current_pos() == state.get_acting_player():
            value = -math.inf
            selected_action = None

            for action in state.get_possible_actions():
                """ ANTI BREAK PYGAME """
                if pygame.display.get_init():
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                """ ANTI BREAK PYGAME """

                pre_value = value
                value = max(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                if value > pre_value:
                    selected_action = action
                if value > beta:
                    break
                alpha = max(alpha, value)

            return selected_action if is_initial_node else value

        else:
            value = math.inf
            for action in state.get_possible_actions():
                """ ANTI BREAK PYGAME """
                if pygame.display.get_init():
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                """ ANTI BREAK PYGAME """

                value = min(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                if value < alpha:
                    break
                beta = min(beta, value)

            return value

    def get_action(self, state: StacState):
        if pygame.display.get_init():
            state.display()
        return self.minimax(state, 5)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
