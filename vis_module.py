import pygame
WIDTH = 400
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def draw_cells(list_cells, surf):
    for cell in list_cells:
        pygame.draw.circle(surf, RED, cell.center, cell.r)
        pygame.draw.circle(surf, BLACK, cell.center, cell.r, 1)