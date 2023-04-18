import pygame
from .constants import *

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color, stac, lord):
        self.row = row
        self.col = col
        self.color = color
        self.stac = stac
        self.lord = lord

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        for layer in range(self.stac):
            if layer == 3:
                pygame.draw.circle(win, GREY, (self.x + (layer * (-5)), self.y + (layer * (-5))), radius + self.OUTLINE)
                pygame.draw.circle(win, self.lord, (self.x + (layer * (-5)), self.y + (layer * (-5))), radius)
            else:
                pygame.draw.circle(win, GREY, (self.x + (layer * (-5)), self.y + (layer * (-5))), radius + self.OUTLINE)
                pygame.draw.circle(win, self.color, (self.x + (layer * (-5)), self.y + (layer * (-5))), radius)