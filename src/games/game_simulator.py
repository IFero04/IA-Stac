import pygame
from abc import ABC, abstractmethod

from games.player import Player
from games.state import State
from games.stac.players.human import HumanStacPlayer
from games.stac.gui.constants import WIDTH, HEIGHT


class GameSimulator(ABC):

    def __init__(self, players: list, display: bool):
        # only allow list of players
        assert len(list(filter(lambda p: not isinstance(p, Player), players))) <= 0

        # stores the possible permutations between players
        self.__permutations = []

        self.heap_permutation(players, len(players))

        # the selected permutation for the current games
        self.__current_permutation = 0

        # create display
        self.display_game = display
        has_human = False
        for player in players:
            if isinstance(player, HumanStacPlayer):
                has_human = True

        if has_human or self.display_game:
            pygame.display.init()
            self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('Stac')


    """
    Adapted from https://www.geeksforgeeks.org/heaps-algorithm-for-generating-permutations/
    It allows for generating all possible permutations of seats in a games
    """

    def heap_permutation(self, a: list, size: int):
        if size == 1:
            self.__permutations.append(a.copy())

        for i in range(0, size):
            self.heap_permutation(a, size - 1)

            if size % 2 == 1:
                temp = a[0]
                a[0] = a[size - 1]
                a[size - 1] = temp
            else:
                temp = a[i]
                a[i] = a[size - 1]
                a[size - 1] = temp

    """
    Swaps the order of the players. The order is changed in a way that guarantees that all combinations are considered
    Example for 2 players [a,b]
        - iteration 1: a,b
        - iteration 2, b,a
        - iteration 3, a,b (back to the initial configuration)
    
    Example for 3 players [x,y,z]
        - iteration 1: x,y,z
        - iteration 2: y,x,z
        - iteration 3: z,x,y
        - iteration 4: x,z,y
        - iteration 5: y,z,x
        - iteration 6: z,y,x
        - iteration 6: x,y,z (back to the initial configuration)
    """

    def change_player_positions(self):
        self.__current_permutation += 1
        if self.__current_permutation >= len(self.__permutations):
            self.__current_permutation = 0

    """
    starts a new games
    """

    @abstractmethod
    def init_game(self) -> State:
        pass

    """
    event before a games ends
    """

    @abstractmethod
    def before_end_game(self, state):
        pass

    """
    event when a games ends
    """

    @abstractmethod
    def end_game(self, state):
        pass

    """
    """

    def get_player_positions(self):
        return self.__permutations[self.__current_permutation]

    """
    runs the simulation
    """
    def run_simulation(self):
        state = self.init_game()
        players = self.get_player_positions()

        # notify players a new games is starting
        for pos in range(0, len(players)):
            players[pos].set_current_pos(pos)
            players[pos].event_new_game()

        # play a turn
        while not state.is_finished():
            selected_action = None
            pos = state.get_acting_player()

            # obtain a valid action
            while True:
                selected_action = players[pos].get_action(state.clone())
                if state.validate_action(selected_action):
                    break

            state.play(selected_action)

            # notify players of the action
            for player in players:
                player.event_action(pos, selected_action, state.clone())
        # handler to run before the games ends
        self.before_end_game(state)

        # notify all players of the result each player got
        for player in players:
            for pos in range(0, len(players)):
                player.event_result(pos, state.get_result(pos))
            player.event_end_game(state.clone())

        # handler to run after a games ends
        self.end_game(state)

    # prints the stats for all players
    def print_stats(self):
        for player in self.__permutations[0]:
            player.print_stats()

    # returns the list of players
    def get_players(self):
        return self.__permutations[0]

    # returns the ordered list of players for the current permutation
    def get_player_positions(self):
        return self.__permutations[self.__current_permutation]

    # gets the number os players
    def num_players(self):
        return len(self.__permutations[0])
