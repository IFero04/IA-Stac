class StacAction:
    """
    a TicTacToe action is simple - it only takes the value of the column and line to play
    """
    __col: int
    __row: int

    def __init__(self, row: int, col: int, move_piece: int):
        self.__col = col
        self.__row = row
        self.__move_piece = move_piece

    def get_col(self):
        return self.__col

    def get_row(self):
        return self.__row

    def get_move_piece(self):
        return self.__move_piece
