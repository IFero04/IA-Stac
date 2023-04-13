from abc import ABC, abstractmethod

from game.state import State


class Player(ABC):

    """
    :param name: name of the player (simply a text identifier for the player)
    """
    def __init__(self, name):
        # name of the player
        self.__name = name

        # index of the current position of the player in the game
        # in most game, the first player takes the position 0
        self.__current_pos = None

    """
    retrieves the name of the player
    """
    def get_name(self):
        return self.__name

    """
    retrieves the current position of the player
    """
    def get_current_pos(self):
        return self.__current_pos

    """
    sets the current position of the player
    :param new_pos: the new position
    """
    def set_current_pos(self, new_pos):
        self.__current_pos = new_pos

    """
    prints to the console the stats of the player
    """
    @abstractmethod
    def print_stats(self):
        pass

    """
    Method that returns an action for a certain game state
    :param state: the current game state
    """
    @abstractmethod
    def get_action(self, state):
        pass

    """
    A method that is invoked once a new game starts
    """
    @abstractmethod
    def event_new_game(self):
        pass

    """
    A method that notifies the player that someone did a certain action. This can be used to log opponents actions
    :param pos: the position of the player that performed the action
    :param action: the action that was performed
    :param new_state: the resulting game state
    """
    @abstractmethod
    def event_action(self, pos: int, action, new_state: State):
        pass

    """
    A method that notifies the player of a game result of a given player
    :param pos: the position of the player that got the result
    :param result: the result of the player
    """
    @abstractmethod
    def event_result(self, pos: int, result):
        pass

    """
    A method that notifies the player that a game has ended
    :param final_state: the final state of the game
    """
    @abstractmethod
    def event_end_game(self, final_state: State):
        pass
