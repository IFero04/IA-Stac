import pygame

WIDTH, HEIGHT = 500, 500
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH//COLS

# RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 191, 255)
GREY = (128, 128, 128)

# ASSETS
P1 = pygame.transform.scale(pygame.image.load('games/stac/gui/assets/P1.png'), (44, 65))
P2 = pygame.transform.scale(pygame.image.load('games/stac/gui/assets/P2.png'), (44, 65))
