import pygame
from random import choice, randint

from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.stac.result import StacResult
from games.state import State


class MonteCarloStacPlayer(StacPlayer):

    def __init__(self, name):
        super().__init__(name)

    def montecarlo(self, state: StacState):
        win = lost = draw = 0
        for play in range(25):
            state_clone = state.clone()
            while not state_clone.is_finished():
                action = choice(state_clone.get_possible_actions())
                state_clone.play(action)

            if state_clone.get_result(self.get_current_pos()) == StacResult.WIN:
                win += 1
            elif state_clone.get_result(self.get_current_pos()) == StacResult.LOOSE:
                lost += 1
            else:
                draw += 1

        return (win + draw * 0.25) / (win + lost + draw)

    def get_action(self, state: StacState):
        if pygame.display.get_init():
            state.display()
        selected_action = None
        max_score = -1
        actions = state.get_possible_actions()
        cont = 1
        loop = len(actions)
        for action in actions:
            """ ANTI BREAK PYGAME """
            if pygame.display.get_init():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
            """ ANTI BREAK PYGAME """

            new_state = state.sim_play(action)
            score = self.montecarlo(new_state)
            if score > max_score:
                max_score = score
                selected_action = action
            elif score == max_score:
                if action.get_move_piece() == 1:
                    selected_action = action
            print(f"CALCULAR JOGADA: {cont}/{loop} | SCORE: {score}/{max_score}")
            cont += 1

        return selected_action

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
