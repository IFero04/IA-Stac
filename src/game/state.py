from abc import ABC, abstractmethod


class State(ABC):

    """
    Retrieve the number of players
    """
    @abstractmethod
    def get_num_players(self):
        pass

    """
    Checks if an action can be performed in the current state and returns true if so
    :param action: action that we want to validate
    :return bool:
    """
    @abstractmethod
    def validate_action(self, action) -> bool:
        pass

    """
    Updates the game state with an action (if valid, check validate_action)
    """
    @abstractmethod
    def update(self, action):
        pass

    """
    Prints the game state to the console
    """
    @abstractmethod
    def display(self):
        pass

    """
    Returns true if the game state is final
    """
    @abstractmethod
    def is_finished(self) -> bool:
        pass

    """ 
    Returns the index of the current acting player, between [0, num_players[
    """
    @abstractmethod
    def get_acting_player(self) -> int:
        pass

    """
    Applies an action to a state, symbolizing a play 
    :param action: the action to be performed (by the current acting player)
    :returns: True if the action ends up being performed
    """
    def play(self, action) -> bool:
        if not self.validate_action(action):
            return False
        self.update(action)
        return True

    """
    copies the current game state
    """
    def clone(self):
        pass

    """
    Retrieves the game result for a player in a given position
    :param pos: position of the player in the game [0, num_players[
    """
    @abstractmethod
    def get_result(self, pos):
        pass

    """
    this handler is executed before the results are communicated to the players
    """
    @abstractmethod
    def before_results(self):
        pass
