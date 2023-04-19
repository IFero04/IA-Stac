import pygame
from games.stac.action import StacAction
from games.stac.player import StacPlayer
from games.stac.state import StacState
from games.stac.gui.constants import SQUARE_SIZE


class HumanStacPlayer(StacPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: StacState):
        state.display()
        while True:
            # noinspection PyBroadException
            try:
                cords = list(map(int, self.get_move_gui()))
                return StacAction(cords[0], cords[1], cords[2])
            except Exception:
                continue

    def get_row_col_from_mous(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def get_move_gui(self):
        pos = None
        while not pos:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    left, middle, right = pygame.mouse.get_pressed()
                    row, col = self.get_row_col_from_mous(pygame.mouse.get_pos())
                    if left:
                        return row, col, False
                    elif right:
                        return row, col, True



    def event_action(self, pos: int, action, new_state: StacState):
        # ignore
        pass

    def event_end_game(self, final_state: StacState):
        # ignore
        pass
