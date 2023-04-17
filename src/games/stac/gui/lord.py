import pygame
from .constants import *


class Lord:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        if self.color == WHITE:
            win.blit(P1, (self.x - P1.get_width() // 2, self.y - P1.get_height() // 2))
        else:
            win.blit(P2, (self.x - P2.get_width() // 2, self.y - P2.get_height() // 2))

