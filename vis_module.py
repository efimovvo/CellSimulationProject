import pygame
WIDTH = 600
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def draw_cells(list_cells, surf):
    """
    :arg    list_cells - list of cells, list
            surf - surface where cells will be drawn
            color - color of cells, type : tuple

    Function draws a cells on the surface."""
    surf.fill(WHITE)
    for cell in list_cells:
        pygame.draw.circle(surf, cell.color, cell.center, cell.r)
        pygame.draw.circle(surf, BLACK, cell.center, cell.r, 1)
