import pygame
import numpy as np

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

# Fonts
FONT = 'verdana'
FONT_COLOR = WHITE
FONT_SIZE_MIN = 10
FONT_SIZE_MAX = 14

# Axes
AXES_COLOR = WHITE


class UserPanelParameter:
    """ UserPanelParameter class : class for parameters which is controlled by user

        Parameters:
            name : string : name of parameter
            value : int or float : numeric value of parameter
            min_value : int or float : minimum for value
            max_value : int or float : maximum for value
            step_value : int or float : step of value changing
        Methods:
            init : Initializing function
            draw : Function draws buttons on the screen
            get_corner : Function calculates the corner coordinates of button
        """
    def __init__(self, name, value, min_value, max_value, step_value):
        """ Initializing function.

            :param name : string : name of parameter
            :param value : int or float : numeric value of parameter
            :param min_value : int or float : minimum for value
            :param max_value : int or float : maximum for value
            :param step_value : int or float : step of value changing
        """
        self.name = name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.step_value = step_value

    def increase(self):
        """ Function increase the parameter value on one step_value. """
        self.value += self.step_value
        if self.value > self.max_value:
            self.value = self.max_value

    def increase_modulo(self):
        """ Function increase by modulo max_value the parameter value on one step_value. """
        self.value = (self.value + self.step_value) % (self.max_value + 1)

    def decrease(self):
        """ Function decrease the parameter value on one step_value. """
        self.value -= self.step_value
        if self.value < self.min_value:
            self.value = self.min_value


class Button:
    """ Button class : class of the button for user panel on the screen.

        Parameters:
            position : list : x and y coordinates of left top corner
            size : list : length and height of button
            function : string : python code that should be done after click
            text : string : text on the button
            parameter : UserPanelParameter : parameter, which is controlled
                by the button
        Methods:
            init : Initializes class
            draw : Draws buttons on the screen
            get_corner : Calculates the corner coordinates of button
    """
    def __init__(self, position, size, function, text, parameter):
        """ Initializing function.

            :param position : list : x and y coordinates of left top corner
            :param size : list : length and height of button
            :param function : string : python code that should be done after click
            :param text : string : text on the button
            :param parameter : UserPanelParameter : parameter, which is controlled
                by the button
        """
        self.position = position
        self.size = size
        self.function = function
        self.text = text
        self.parameter = parameter

    def draw(self, surface):
        """ Function draws buttons on the screen.

            :param surface : pygame.Surface : surface where button will be drawn
            """
        color_set = [WHITE, LIGHT_GREY, DARK_GREY, BLACK]
        # changes color if button not switch
        color = color_set[0]
        pygame.draw.rect(surface, color,
                         [self.position[0], self.position[1],
                          self.size[0], self.size[1]])
        font_surface = pygame.font.SysFont(FONT, FONT_SIZE_MIN)
        text_surface = font_surface.render(str(self.text), True, BLACK)
        text_rect = text_surface.get_rect(
            center=(self.position[0] + self.size[0] // 2,
                    self.position[1] + self.size[1] // 2))
        surface.blit(text_surface, text_rect)

    def get_corner(self, corner_name):
        """ Function calculates the corner coordinates of button.

        :param corner_name : string : name of corner
            ("top-left", "bottom-left", "top-right", "bottom-right")
            """
        if corner_name == "top-left":
            coordinate = self.position
        elif corner_name == "bottom-left":
            coordinate = [self.position[0],
                          self.position[1] + self.size[1]]
        elif corner_name == "top-right":
            coordinate = [self.position[0] + self.size[0],
                          self.position[1]]
        else:
            coordinate = [self.position[0] + self.size[0],
                          self.position[1] + self.size[1]]
        return coordinate


def clean_screen(surface):
    """ Function draw only background color on the surface

        :param surface : pygame.Surface : surface for cleaning
    """
    surface.fill(DARK_GREY)


def draw_user_panel(surf, button_list):
    """ Function draws user panel on the screen with all buttons.

        :param surf : pygame.Surface : surface where user panel will be drawn
        :param button_list : list(Button) : list, each element is Button type
    """
    pygame.draw.rect(
        surf,
        LIGHT_GREY,
        [0, 0, WIDTH, PANEL_HEIGHT]
    )

    for button in button_list:
        button.draw(surf)


def interpolate_color(color_1, color_2, coefficient):
    """ Function interpolate the color between two ones with given ratio.

        :param color_1 : tuple(int, int, int) : first color
        :param color_2 : tuple(int, int, int) : second color
        :param coefficient : float : proportion (part of first color)
    """
    color_1 = np.array(color_1)
    color_2 = np.array(color_2)
    color = color_1 * coefficient + color_2 * (1 - coefficient)
    color = [int(color_part) for color_part in color]

    return tuple(color)


def draw_graph(surface, starting_point, sizes, x_data, y_data,
               axis_comment, graph_name, x_scale=500):
    """ Function draws graph on the screen.

        :param surface : pygame.Surface : surface where graph will be drawn
        :param starting_point : list : the starting point of graph
        :param sizes : list : size of graph
        :param x_data : list : data on x axis
        :param y_data : list : data on y axis
        :param axis_comment : list : each element is string
        :param graph_name : string : name of graph
        :param x_scale : int : maximum value (x_max - x_min)
    """
    # Parameters
    offset = 50
    tick_length = 10
    number_of_ticks = [20, 10]

    x_max = max(x_data) if max(x_data) > x_scale else x_scale
    x_min = x_max - x_scale
    if x_max > 1000:
        number_of_ticks[0] = 10

    min_index_on_screen = 0
    for i in range(len(x_data)):
        if x_data[i] <= x_min:
            min_index_on_screen = i
    x_data = x_data[min_index_on_screen:]
    for i in range(len(y_data)):
        y_data[i] = y_data[i][min_index_on_screen:]

    y_max = 0
    for i in range(len(y_data)):
        y_max = (max(y_max, max(y_data[i])) // 10 + 1) * 10
    y_min = 0

    image_axis = pygame.Surface((sizes[0], sizes[1]), pygame.SRCALPHA)
    image_data = pygame.Surface((sizes[0] - 2 * offset, sizes[1] - 2 * offset))
    image_data.set_colorkey(BLACK)

    # Axes X and Y accordingly
    pygame.draw.line(image_axis, AXES_COLOR,
                     (offset, sizes[1] - offset),
                     (sizes[0] - offset, sizes[1] - offset))
    pygame.draw.line(image_axis, AXES_COLOR,
                     (offset, offset),
                     (offset, sizes[1] - offset))

    # Ticks on axes X and Y accordingly
    font_surface = pygame.font.SysFont(FONT, FONT_SIZE_MIN)
    for i in range(number_of_ticks[0] + 1):
        # Tick position on X axis
        x = offset + (sizes[0] - 2 * offset) * i / number_of_ticks[0]
        y = sizes[1] - offset
        # Tick on X axis
        pygame.draw.line(image_axis, AXES_COLOR, (x, y), (x, y + tick_length))
        # Number on X axis
        text = str(int(x_min + x_scale * i / number_of_ticks[0]))
        text_surface = font_surface.render(text, True, FONT_COLOR)
        text_rect = text_surface.get_rect(
            center=(starting_point[0] + x,
                    starting_point[1] + y + 2 * tick_length))
        surface.blit(text_surface, text_rect)

    # Name of X axis
    text_surface = font_surface.render(axis_comment[0], True, FONT_COLOR)
    text_rect = text_surface.get_rect(
        center=(starting_point[0] + sizes[0] // 2,
                starting_point[1] + sizes[1] - offset + 3.5 * tick_length)
    )
    surface.blit(text_surface, text_rect)

    for i in range(number_of_ticks[1] + 1):
        # Tick position on Y axis
        x = offset
        y = offset + (sizes[1] - 2 * offset) * i / number_of_ticks[1]
        # Tick on Y axis
        pygame.draw.line(image_axis, AXES_COLOR, (x, y), (x - tick_length, y))
        # Number on Y axis
        text = str(int(y_max - (y_max - y_min) * i / number_of_ticks[1]))
        text_surface = font_surface.render(text, True, FONT_COLOR)
        text_rect = text_surface.get_rect(
            center=(starting_point[0] + x - 2 * tick_length,
                    starting_point[1] + y)
        )
        surface.blit(text_surface, text_rect)

    # Name of Y axis
    text_surface = font_surface.render(axis_comment[1], True, FONT_COLOR)
    text_surface = pygame.transform.rotate(text_surface, 90)
    text_rect = text_surface.get_rect(
        center=(starting_point[0] + offset - 3.5 * tick_length,
                starting_point[1] + sizes[1] // 2)
    )
    surface.blit(text_surface, text_rect)

    # Graph name
    font_surface = pygame.font.SysFont(FONT, FONT_SIZE_MAX)
    text_surface = font_surface.render(graph_name, True, FONT_COLOR)
    text_rect = text_surface.get_rect(
        center=(starting_point[0] + sizes[0] // 2,
                starting_point[1] + offset - 2 * tick_length)
    )
    surface.blit(text_surface, text_rect)

    # Draw graph lines
    color_set = [GREEN, RED]
    for i in range(len(y_data)):
        line = []
        basic_color = color_set[i]
        for j in range(len(x_data)):
            line.append(((sizes[0] - 2 * offset) * (x_data[j] - x_min) / x_scale,
                         (sizes[1] - 2 * offset) * (1 - (y_data[i][j] - y_min) / y_max))
                        )
        if len(line) > 1:
            color_steps = min(len(line) - 1, 10)
            for j in range(color_steps):
                start = int(np.floor(len(line) * j / color_steps))
                end = int(np.ceil(len(line) * (j + 1) / color_steps))
                line_segment = line[start:end + 1]
                color = interpolate_color(basic_color, DARK_GREY,
                                          0.2 + (j + 1) * 0.8 / color_steps)
                pygame.draw.lines(image_data, color, False, line_segment, 1)
            pygame.draw.circle(image_data, basic_color, line[-1], 3)

    # Draw the surfaces on the screen
    surface.blit(image_axis,
                 (starting_point[0], starting_point[1]))
    surface.blit(image_data,
                 (starting_point[0] + offset, starting_point[1] + offset))


def draw_cells(list_cells, surface):
    """ Function draws a cells on the surface.

        :param surface: pygame.Surface : surface for drawing
        :param list_cells : list(Cell) : list of cells
    """
    for cell in list_cells:
        position = [cell.position[0], cell.position[1] + PANEL_HEIGHT]
        cell.border_color = (102 + cell.satiety * 153, 102 + cell.satiety * 153,
                             102 + cell.satiety * 153)
        if cell.predator:
            cell.color = (150 + cell.satiety * 102, 102 - cell.satiety * 102,
                          102 - cell.satiety * 102)
        else:
            cell.color = (102 - cell.satiety * 102, 150 + cell.satiety * 102,
                          102 - cell.satiety * 102)
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
    """ Function draws a meal object on the surface.

        :param surface : pygame.Surface : surface where cells will be drawn
        :param meal_list : list : list of meal objects
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
