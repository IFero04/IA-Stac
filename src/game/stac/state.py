from typing import Optional

from game.stac.action import StacAction
from game.stac.result import StacResult
from game.state import State


def cell_to_str(val):
    return {
        0: 'X',
        1: 'O',
        StacState.EMPTY_CELL: ' '
    }[val]


class StacState(State):
    EMPTY_CELL = -1

    def __init__(self, dimension: int):
        super().__init__()
        num_rows: int
        num_cols: int

        if dimension < 3:
            raise Exception("the dimension of the board must be 3 or over")
        """
        the dimensions of the board
        """
        self.__num_rows = dimension
        self.__num_cols = dimension
        """
        the grid
        """
        self.__grid = [[StacState.EMPTY_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]
        """
        counts the number of turns in the current game
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
        """
        Offset
        """
        self.__offSetH = [[[0, -1], [0, 0], [0, 1]], [[0, -2], [0, -1], [0, 0]], [[0, 0], [0, 1], [0, 2]]]
        self.__offSetV = [[[-1, 0], [0, 0], [1, 0]], [[-2, 0], [-1, 0], [0, 0]], [[0, 0], [1, 0], [2, 0]]]
        self.__offSetDS = [[[1, -1], [0, 0], [-1, 1]], [[2, -2], [1, -1], [0, 0]], [[0, 0], [-1, 1], [-2, 2]]]
        self.__offSetDI = [[[-1, -1], [0, 0], [1, 1]], [[-2, -2], [-1, -1], [0, 0]], [[0, 0], [1, 1], [2, 2]]]
        self.__offSets = [self.__offSetH, self.__offSetV, self.__offSetDS, self.__offSetDI]

    # Verifica quantas sequecias o jogador tem
    def __count_sequences(self, player):
        contador = 0
        # Verifica as linhas
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols - 2):
                if self.__grid[row][col] == player and \
                        self.__grid[row][col + 1] == player and \
                        self.__grid[row][col + 2] == player:
                    contador += 1
        # Verifica as colunas
        for row in range(0, self.__num_rows - 2):
            for col in range(0, self.__num_cols):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col] == player and \
                        self.__grid[row + 2][col] == player:
                    contador += 1
        # Verifica a digonal superior
        for row in range(2, self.__num_rows):
            for col in range(0, self.__num_cols - 2):
                if self.__grid[row][col] == player and \
                        self.__grid[row - 1][col + 1] == player and \
                        self.__grid[row - 2][col + 2] == player:
                    contador += 1
        # Verifica a digonal inferiro
        for row in range(0, self.__num_rows - 2):
            for col in range(0, self.__num_cols - 2):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col + 1] == player and \
                        self.__grid[row + 2][col + 2] == player:
                    contador += 1
        # Devolve o número de sequências
        return contador

    def valid_grid(self, row, col):
        if (row >= 0 and col >= 0) :
            if (row < self.__num_rows and col < self.__num_cols):
                return self.__grid[row][col]
        return 404

    def __check_sequence_possible(self) -> bool:
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                if self.__grid[row][col] == -1:
                    for offSet in self.__offSets:
                        for position in offSet:
                            p1 = (row + position[0][0], col + position[0][1])
                            p2 = (row + position[1][0], col + position[1][1])
                            p3 = (row + position[2][0], col + position[2][1])
                            if not (self.valid_grid(p1[0], p1[1]) == 404 or self.valid_grid(p2[0], p2[1]) == 404 or self.valid_grid(p3[0], p3[1]) == 404):
                                has_player0 = False
                                has_player1 = False

                                if self.__grid[p1[0]][p1[1]] == 0 or self.__grid[p2[0]][p2[1]] == 0 or self.__grid[p3[0]][p3[1]] == 0:
                                    has_player0 = True
                                if self.__grid[p1[0]][p1[1]] == 1 or self.__grid[p2[0]][p2[1]] == 1 or self.__grid[p3[0]][p3[1]] == 1:
                                    has_player1 = True

                                if not (has_player0 and has_player1):
                                    return True

        # Nao Existem jogadas Pontuaveis
        return False

    def __check_winner(self):
        seqPlayer0 = self.__count_sequences(0)
        seqPlayer1 = self.__count_sequences(1)
        print(f"Contador Sequencias - P0: {seqPlayer0} | P1: {seqPlayer1}")
        if seqPlayer0 > seqPlayer1:
            self.__has_winner = True
            return 0
        elif seqPlayer1 > seqPlayer0:
            self.__has_winner = True
            return 1
        else:
            return -1

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: StacAction) -> bool:
        col = action.get_col()
        row = action.get_row()

        # valid column
        if col < 0 or col >= self.__num_cols:
            return False
        # valid line
        if row < 0 or row >= self.__num_rows:
            return False

        # full column / line
        if self.__grid[row][col] != StacState.EMPTY_CELL:
            return False

        return True

    def update(self, action: StacAction):
        col = action.get_col()
        row = action.get_row()

        # add the play
        self.__grid[row][col] = self.__acting_player
        """print(f"Ações Possíveis: {self.get_possible_actions()}")"""

        # determine if there is a winner
        """print(f"Have Sequence: {self.__check_sequence_possible()} | Is Full: {self.__is_full()}")"""
        if not (self.__check_sequence_possible()) or self.__is_full():
            self.__winner = self.__check_winner()
            self.__end_game = True

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def __display_cell(self, row, col):
        print({
                  0: 'X',
                  1: 'O',
                  StacState.EMPTY_CELL: ' '
              }[self.__grid[row][col]], end="")

    def __display_numbers(self):
        for col in range(1, self.__num_cols + 1):
            print(col, end="")
            if col < 10:
                print(' ', end="")
        print("")

    def display(self):

        print('  ', end="")
        self.__display_numbers()
        for row in range(0, self.__num_rows):
            print(row + 1, end=" ")
            r = map(lambda col: cell_to_str(col), self.__grid[row])
            print("|".join(r))
            print('  ', end="")
            if row < self.__num_rows - 1:
                print("+".join(["-"] * self.__num_cols))

        print("")

    def __is_full(self):
        return self.__turns_count >= (self.__num_cols * self.__num_rows)

    def is_finished(self) -> bool:
        return self.__end_game

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = StacState(self.__num_cols)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
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
