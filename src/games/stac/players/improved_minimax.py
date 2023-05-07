import pygame
import math

from games.stac.players.history import read_file, add_history, str_to_action, str_to_state, check_play
from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.stac.result import StacResult
from games.state import State
from games.stac.action import StacAction


class ImprovedMinimaxStacPlayer(StacPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.path = 'games/stac/players/ImprovedMinimax_History.txt'
        self.history = read_file(self.path)
        self.match = []

    def __heuristic(self, state: StacState):
        """
        Game State
        """
        value = 0
        grid = state.get_grid()
        lord_grid = state.get_lord_grid()

        player_pos = self.get_current_pos()
        player_grid_value = -1 - self.get_current_pos()
        player_stacks = 0
        opponent_pos = 0 if self.get_current_pos() == 1 else 1
        opponent_grid_value = -2 if player_grid_value == -1 else -1
        opponent_stacks = 0

        unclaimed_stacks = []

        player_row = player_col = opponent_row = opponent_col = 0

        player_actions = state.get_possible_actions()
        opponent_state = state.clone()
        opponent_state.switch_player()
        opponent_actions = opponent_state.get_possible_actions()

        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if lord_grid[row][col] == player_pos:
                    player_row, player_col = row, col
                elif lord_grid[row][col] == opponent_pos:
                    opponent_row, opponent_col = row, col

        """
        Check Victory
        """
        if player_stacks >= 4:
            value = 90
        elif opponent_stacks >= 4:
            value = -90

        """
        Material Advantage 
        """
        for row in range(0, state.get_num_rows()):
            for col in range(0, state.get_num_cols()):
                if grid[row][col] == player_grid_value:
                    player_stacks += 1
                elif grid[row][col] == opponent_grid_value:
                    opponent_stacks += 1
                elif grid[row][col] == 2:
                    unclaimed_stacks.append((row, col))

        value += player_stacks - opponent_stacks

        if value > 0:
            value += len(unclaimed_stacks) / 5
        elif value < 0:
            value -= len(unclaimed_stacks) / 5
        else:
            value += len(unclaimed_stacks) / 10

        """
        Pawn Position
        """
        contP = contO = 0

        if grid[player_row][player_col] == 1:
            for stack in unclaimed_stacks:
                if stack[0] == player_row or stack[1] == player_col:
                    contP += 1
                if stack[0] + 1 == player_row:
                    value += 0.05
                elif stack[0] - 1 == player_row:
                    value += 0.05
                if stack[1] + 1 == player_col:
                    value += 0.05
                elif stack[1] - 1 == player_col:
                    value += 0.05

        if grid[opponent_row][opponent_col] == 1:
            for stack in unclaimed_stacks:
                if stack[0] == opponent_row or stack[1] == opponent_col:
                    contO += 1
                if stack[0] + 1 == opponent_row:
                    value -= 0.05
                elif stack[0] - 1 == opponent_row:
                    value -= 0.05
                if stack[1] + 1 == opponent_col:
                    value -= 0.05
                elif stack[1] - 1 == opponent_col:
                    value -= 0.05

        if contP >= 2 or contO >= 2:
            if contP >= contO:
                value += 0.75
            else:
                value -= 0.75

        """
        Pawn Mobility
        """
        value += (len(player_actions) - len(opponent_actions)) / 100

        """
        Blocking Moves
        """
        if grid[opponent_row][opponent_col] == 1:
            for stack in unclaimed_stacks:
                if stack[0] == opponent_row:
                    step = 1 if stack[1] > opponent_col else -1
                    for block in range(opponent_col + step, stack[1] - step, step):
                        if lord_grid[opponent_row][block] != -1:
                            value += 0.15

                elif stack[1] == opponent_col:
                    step = 1 if stack[0] > opponent_row else -1
                    for block in range(opponent_row + step, stack[0] - step, step):
                        if lord_grid[block][opponent_col] != -1:
                            value += 0.15

        return value

    def __top_actions(self, state: StacState):
        actions = state.get_possible_actions()
        actions_values = []
        for action in actions:
            new_state = state.clone()
            new_state.play(action)
            value_play = self.__heuristic(new_state)
            actions_values.append((action, value_play))

        n = len(actions_values)
        for i in range(n):
            for j in range(0, n - i - 1):
                if actions_values[j][1] < actions_values[j + 1][1]:
                    actions_values[j], actions_values[j + 1] = actions_values[j + 1], actions_values[j]

        if n > 5:
            n = 5

        top_actions = []
        for i in range(n):
            top_actions.append(actions_values[i][0])

        return top_actions

    def minimax(self, state: StacState, depth: int, alpha: int = -math.inf, beta: int = math.inf,
                is_initial_node: bool = True):
        if state.is_finished():
            return {
                StacResult.WIN: 90,
                StacResult.LOOSE: -90,
                StacResult.DRAW: 0
            }[state.get_result(self.get_current_pos())]

        if depth == 0:
            heuristic = self.__heuristic(state)
            print(f"Player {self.get_name()} | Valor Jogada: {heuristic:.4f}")
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

        for play in self.history:
            if str(state) == play[0]:
                action = str_to_action(play[1])
                if state.validate_action(action):
                    return action

        action = self.minimax(state, 6)

        self.match.append((str(state) + "$" + str(action) + "\n"))

        return action

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        result = final_state.get_result(self.get_current_pos())
        history_plays = []
        with open(self.path, 'r') as file:
            lines = file.read()
            lines = lines.split('\n')
            for line in lines:
                history_plays.append(line)

        if result == StacResult.WIN:
            for play in self.match:
                flag = check_play(play.split('$'))

                if play not in history_plays and flag:
                    add_history(self.path, play)
                    history_plays.append(play)

        self.history = read_file(self.path)

