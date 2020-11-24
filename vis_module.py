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
        pygame.draw.circle(surf, cell.color, cell.position, cell.size)
        pygame.draw.circle(surf, BLACK, cell.position, cell.size, 1)


def draw_meal(meal_list, surf):
    """ Function draws a meal on the surface.
    :arg
    ---
        meal: list - list of meal
        surf - surface where cells will be drawn
    """
    for meal in meal_list:
        if meal != 0:
            pygame.draw.circle(surf, BLACK, meal.position, meal.size)