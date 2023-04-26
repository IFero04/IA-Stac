import numpy as np
import pygame

from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.stac.action import StacAction
from games.stac.result import StacResult
from games.state import State


class QLearningStacPlayer(StacPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.q_table = {}
        self.alpha = 0.5
        self.gamma = 0.9
        self.epsilon = 0.1
        self.state = StacState
        self.new_state = StacState

    def get_state_key(self, state: StacState):
        key = np.array(state)
        return tuple(key.flatten())

    def update_q_table(self, state_key, action, reward, next_state_key):
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0 for a in self.new_state.get_possible_actions()}


        q_values = self.q_table[state_key]
        max_next_q_value = max(self.q_table[next_state_key].values())
        q_values[action] += self.alpha * (reward + self.gamma * max_next_q_value - q_values[action])

    def q_lerning_agent(self, state: StacState):
        self.state = state
        state_key = self.get_state_key(self.state.clone())
        actions = self.state.get_possible_actions()

        if np.random.uniform() < self.epsilon:
            # exploration: choose a random action
            action = np.random.choice(actions)
            return StacAction(
                action.get_row(), action.get_col(), action.get_move_piece()
            )

        # exploitation: choose the action with the highest Q-value
        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0 for a in actions}
        q_values = self.q_table[state_key]

        max_q_value = max(q_values.values())
        max_q_actions = [a for a, q in q_values.items() if q == max_q_value]
        action = np.random.choice(max_q_actions)
        return StacAction(
            action.get_row(), action.get_col(), action.get_move_piece()
        )

    def get_action(self, state: StacState):
        if pygame.display.get_init():
            state.display()

        state_key = self.get_state_key(state.clone())

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0 for a in state.get_possible_actions()}

        return self.q_lerning_agent(state)

    def event_action(self, pos: int, action, new_state: State):
        self.new_state = new_state
        state_key = self.get_state_key(self.state.clone())
        next_state_key = self.get_state_key(self.new_state.clone())
        if self.new_state.is_finished():
            # Game is finished, update Q-value with the reward
            result = self.new_state.get_result(pos)
            if result == StacResult.WIN:
                reward = 1
            elif result == StacResult.LOOSE:
                reward = -1
            else:
                reward = 0
        else:
            # Game is not finished, reward is 0
            reward = 0
        self.update_q_table(state_key, action, reward, next_state_key)

    def event_end_game(self, final_state: State):
        # ignore
        pass
