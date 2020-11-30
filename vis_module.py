import pygame

# Interface size

# Instrumental panel size
PANEL_HEIGHT = 100
# Simulating area size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# Plot area size
PLOT_AREA_WIDTH = 600
# Full screen size
WIDTH = SCREEN_WIDTH + PLOT_AREA_WIDTH
HEIGHT = PANEL_HEIGHT + SCREEN_HEIGHT

# Color set
WHITE = (255, 255, 255)
DARK_GREY = (102, 102, 102)
LIGHT_GREY = (204, 204, 204)
BLACK = (0, 0, 0)
RED = (204, 0, 0)
GREEN = (0, 204, 0)
BLUE = (0, 0, 204)


def clean_screen(surf):
    surf.fill(DARK_GREY)


def draw_user_panel(surf):
    pygame.draw.rect(
        surf,
        LIGHT_GREY,
        [0, 0, WIDTH, PANEL_HEIGHT]
    )


def draw_plot(surf):
    pygame.draw.rect(
        surf,
        DARK_GREY,
        [SCREEN_WIDTH, PANEL_HEIGHT, PLOT_AREA_WIDTH, SCREEN_HEIGHT]
    )


def draw_cells(list_cells, surf):
    """
    :arg    list_cells - list of cells, list
            surf - surface where cells will be drawn
            color - color of cells, type : tuple

    Function draws a cells on the surface."""
    for cell in list_cells:
        position = [cell.position[0], cell.position[1] + PANEL_HEIGHT]
        '''  Когда будет введена степень агрессии и дружелюбия
         if cell.aggressiveness - cell.friendliness >= 0:         
            cell.color = RED
        elif cell.friendliness - cell.aggressiveness > 0:
            cell.color = GREEN '''
        image = pygame.Surface((WIDTH, HEIGHT))
        image.set_colorkey(BLACK)
        image.set_alpha(cell.satiety * 255)
        if cell.age < cell.reproductive_age[0]:
            cell.border_thickness = -1
        elif cell.reproductive_age[0] < cell.age < cell.reproductive_age[1]:
            cell.border_thickness = 1
        elif cell.age > cell.reproductive_age[1]:
            cell.border_thickness = 4

        pygame.draw.circle(
            image,
            cell.color,
            position,
            cell.size
        )
        pygame.draw.circle(
            image,
            cell.border_color,
            position,
            cell.size,
            cell.border_thickness
        )
        surf.blit(image, (0, 0))


def draw_meal(meal_list, surf):
    """ Function draws a meal on the surface.
    :arg
    ---
        meal: list - list of meal
        surf - surface where cells will be drawn
    """
    for meal in meal_list:
        x_min = meal.position[0] - meal.size / 2
        y_min = PANEL_HEIGHT + meal.position[1] - meal.size / 2

        if meal != 0:
            pygame.draw.rect(
                surf,
                WHITE,
                [x_min, y_min, meal.size, meal.size]
            )
