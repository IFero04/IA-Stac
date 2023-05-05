import pygame
import math

from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.stac.result import StacResult
from games.state import State


class MinimaxStacPlayer(StacPlayer):
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
            heuristic = self.__heuristic(state)
            print(f"Player {self.get_name()} | Valor Jogada: {heuristic}")
            return heuristic

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
