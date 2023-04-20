import pygame
from .constants import *
from games.stac.gui.piece import Piece
from games.stac.gui.lord import Lord


class StacDisplay:
    def draw_squares(self, win):
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, BLUE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, win, grid):
        for row in range(ROWS):
            for col in range(COLS):
                if grid[row][col] == -1:
                    (Piece(row, col, BLACK, 4, RED)).draw(win)
                elif grid[row][col] == -2:
                    (Piece(row, col, BLACK, 4, BLUE)).draw(win)
                elif grid[row][col] > 0:
                    (Piece(row, col, BLACK, grid[row][col], None)).draw(win)

    def draw_lords(self, win, lord_grid):
        for row in range(ROWS):
            for col in range(COLS):
                if lord_grid[row][col] == 0:
                    (Lord(row, col, WHITE)).draw(win)
                elif lord_grid[row][col] == 1:
                    (Lord(row, col, BLUE)).draw(win)

    def draw(self, grid, lord_grid):
        WINDOW = pygame.display.get_surface()
        self.draw_squares(WINDOW)
        self.draw_pieces(WINDOW, grid)
        self.draw_lords(WINDOW, lord_grid)
