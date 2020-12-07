import pygame
from in_out_module import *

# Interface size

# Instrumental panel size
PANEL_HEIGHT = 50
# Simulating area size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# Plot area size
PLOT_AREA_WIDTH = 600
PLOT_AREA_HEIGHT = 600

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

# Interface parameters
FOOD_MAX_QUANTITY = 20


class Button:
    def __init__(self, position, size, text):
        self.position = position
        self.size = size
        self.text = text
        self.active = False

    def click(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def draw(self, surf):
        color = DARK_GREY if self.active else WHITE
        pygame.draw.rect(surf, color,
                         [self.position[0], self.position[1],
                          self.size[0], self.size[1]])


def clean_screen(surf):
    surf.fill(DARK_GREY)


def draw_user_panel(surf, button_list):
    pygame.draw.rect(
        surf,
        LIGHT_GREY,
        [0, 0, WIDTH, PANEL_HEIGHT]
    )

    for button in button_list:
        button.draw(surf)


def draw_plot(surf):
    pygame.draw.rect(
        surf,
        DARK_GREY,
        [SCREEN_WIDTH, PANEL_HEIGHT, PLOT_AREA_WIDTH, SCREEN_HEIGHT]
    )


def draw_graph(surface, starting_point, sizes, x_data, y_data, axis_comment, graph_name, x_scale = 500):
    # Parameters
    offset = 50
    tick_length = 10
    number_of_ticks = [20, 10]

    x_max = max(x_data) if max(x_data) > x_scale else x_scale
    x_min = x_max - x_scale

    min_index_on_screen = 0
    for i in range(len(x_data)):
        if x_data[i] <= x_min:
            min_index_on_screen = i
    x_data = x_data[min_index_on_screen:]
    for i in range(len(y_data)):
        y_data[i] = y_data[i][min_index_on_screen:]

    y_max = (max(max(y_data)) // 10 + 1) * 10
    y_min = 0

    image_axis = pygame.Surface((sizes[0], sizes[1]), pygame.SRCALPHA)
    image_data = pygame.Surface((sizes[0] - 2 * offset, sizes[1] - 2 * offset))
    image_data.set_colorkey(BLACK)
    image_data.set_alpha(255) # Предлагаю удалить, прозрачность не нужна

    # Axes X and Y accordingly
    pygame.draw.line(image_axis, BLACK,
                     (offset, sizes[1] - offset),
                     (sizes[0] - offset, sizes[1] - offset))
    pygame.draw.line(image_axis, BLACK,
                     (offset, offset),
                     (offset, sizes[1] - offset))

    # Ticks on axes X and Y accordingly
    font_surface = pygame.font.SysFont('verdana', 10)
    for i in range(number_of_ticks[0] + 1):
        # Tick position on X axis
        x = offset + (sizes[0] - 2 * offset) * i / number_of_ticks[0]
        y = sizes[1] - offset
        # Tick on X axis
        pygame.draw.line(image_axis, BLACK, (x, y), (x, y + tick_length))
        # Number on X axis
        text = str(int(x_min + x_scale * i / number_of_ticks[0]))
        text_surface = font_surface.render(text, True, BLACK)
        text_rect = text_surface.get_rect(
            center=(starting_point[0] + x,
                    starting_point[1] + y + 1.5 * tick_length))
        surface.blit(text_surface, text_rect)
    # Name of X axis
    text_surface = font_surface.render(axis_comment[0], True, BLACK)
    text_rect = text_surface.get_rect(
        center=(starting_point[0] + sizes[0] // 2,
                starting_point[1] + sizes[1] - offset + 3 * tick_length)
    )
    surface.blit(text_surface, text_rect)
    for i in range(number_of_ticks[1] + 1):
        # Tick position on Y axis
        x = offset
        y = offset + (sizes[1] - 2 * offset) * i / number_of_ticks[1]
        # Tick on Y axis
        pygame.draw.line(image_axis, BLACK, (x, y), (x - tick_length, y))
        # Number on Y axis
        text = str(int(y_max - (y_max - y_min) * i / number_of_ticks[1]))
        text_surface = font_surface.render(text, True, BLACK)
        text_rect = text_surface.get_rect(
            center=(starting_point[0] + x - 2 * tick_length,
                    starting_point[1] + y)
        )
        surface.blit(text_surface, text_rect)
    # Name of Y axis
    text_surface = font_surface.render(axis_comment[1], True, BLACK)
    text_surface = pygame.transform.rotate(text_surface, 90)
    text_rect = text_surface.get_rect(
        center=(starting_point[0] + offset - 3.5 * tick_length,
                starting_point[1] + sizes[1] // 2)
    )
    surface.blit(text_surface, text_rect)

    # Graph name
    font_surface = pygame.font.SysFont('verdana', 12)
    text_surface = font_surface.render(graph_name, True, BLACK)
    text_rect = text_surface.get_rect(
        center=(starting_point[0] + sizes[0] // 2,
                starting_point[1] + offset - 2 * tick_length)
    )
    surface.blit(text_surface, text_rect)

    for i in range(len(y_data)):
        line = []
        color = GREEN if i == 0 else RED
        for j in range(len(x_data)):
            line.append(((sizes[0] - 2 * offset) * (x_data[j] - x_min) / x_scale,
                         (sizes[1] - 2 * offset) * (1 - (y_data[i][j] - y_min) / y_max))
                        )
        if len(line) > 1:
            pygame.draw.lines(image_data, color, False, line, 1)
            pygame.draw.circle(image_data, color, line[-1], 3)

    surface.blit(image_axis,
                 (starting_point[0], starting_point[1]))
    surface.blit(image_data,
                 (starting_point[0] + offset, starting_point[1] + offset))


def draw_cells(list_cells, surface):
    """
    :arg    list_cells - list of cells, list
            surf - surface where cells will be drawn
            color - color of cells, type : tuple

    Function draws a cells on the surface."""
    for cell in list_cells:
        position = [cell.position[0], cell.position[1] + PANEL_HEIGHT]
        cell.border_color = (102 + cell.satiety * 153, 102 + cell.satiety * 153, 102 + cell.satiety * 153)
        if cell.predator:
            cell.color = (150 + cell.satiety * 102, 102 - cell.satiety * 102, 102 - cell.satiety * 102)
        else:
            cell.color = (102 - cell.satiety * 102, 150 + cell.satiety * 102, 102 - cell.satiety * 102)
        if cell.age < cell.reproductive_age[0]:
            cell.border_thickness = -1
        elif cell.reproductive_age[0] <= cell.age <= cell.reproductive_age[1]:
            cell.border_thickness = 1
        elif cell.age > cell.reproductive_age[1]:
            cell.border_thickness = 2

        pygame.draw.circle(
            surface,
            cell.color,
            position,
            cell.size
        )
        pygame.draw.circle(
            surface,
            cell.border_color,
            position,
            cell.size,
            cell.border_thickness
        )


def draw_meal(meal_list, surface):
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
                surface,
                WHITE,
                [x_min, y_min, meal.size, meal.size]
            )