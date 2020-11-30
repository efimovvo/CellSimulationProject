import pygame

# Interface size

# Instrumental panel size
PANEL_HEIGHT = 100
# Simulating area size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# Plot area size
PLOT_AREA_WIDTH = 600
# Graph area size
GRAPH_AREA_WIDTH = 500
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


def data(list_cells, dt):
    list_victim = [cell for cell in list_cells if not cell.predator]
    list_predator = [cell for cell in list_cells if cell.predator]
    if list_victim != 0:
        with open('data.txt', 'a') as file:
            cell_data = [str(len(list_victim)), str(len(list_predator)), str(dt)]
            cell_data = ' '.join(cell_data)
            cell_data = cell_data + '\n'
            file.write(cell_data)



def graph(surf):
    image_axis = pygame.Surface((GRAPH_AREA_WIDTH, GRAPH_AREA_WIDTH), pygame.SRCALPHA)
    image_data = pygame.Surface((GRAPH_AREA_WIDTH, GRAPH_AREA_WIDTH))
    image_data.set_colorkey(BLACK)
    image_data.set_alpha(255)
    input_data = []
    predators_list = []
    victims_list = []
    time = []   
    pygame.draw.line(image_axis, BLACK, (0, GRAPH_AREA_WIDTH), (GRAPH_AREA_WIDTH, GRAPH_AREA_WIDTH))
    pygame.draw.line(image_axis, BLACK, (0, 0), (0, GRAPH_AREA_WIDTH))
    pygame.draw.line(image_axis, BLACK, (0, GRAPH_AREA_WIDTH - 1), (GRAPH_AREA_WIDTH - 1, GRAPH_AREA_WIDTH - 1))
    with open('data.txt', 'r') as file:
        for line in file:
            input_data.append(line.split())
    for i in range(len(input_data)):
        victims_list.append(input_data[i][0])
        predators_list.append(input_data[i][1])
        time.append(input_data[i][2])
    for i in range(len(input_data) - 1):
        pygame.draw.line(image_data, GREEN, (int(time[i]) / 20, GRAPH_AREA_WIDTH - 5 * int(victims_list[i]),),
                         (int(time[i + 1]) / 20, GRAPH_AREA_WIDTH - 5 * int(victims_list[i + 1])))
        pygame.draw.line(image_data, RED, (int(time[i]) / 20, GRAPH_AREA_WIDTH - 5 * int(predators_list[i]),),
                         (int(time[i + 1]) / 20, GRAPH_AREA_WIDTH - 5 * int(predators_list[i + 1])))

    surf.blit(image_data, (PLOT_AREA_WIDTH, 100))
    surf.blit(image_axis, (PLOT_AREA_WIDTH, 100))


def draw_cells(list_cells, surf):
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
        elif cell.reproductive_age[0] < cell.age < cell.reproductive_age[1]:
            cell.border_thickness = 1
        elif cell.age > cell.reproductive_age[1]:
            cell.border_thickness = 2

        pygame.draw.circle(
            surf,
            cell.color,
            position,
            cell.size
        )
        pygame.draw.circle(
            surf,
            cell.border_color,
            position,
            cell.size,
            cell.border_thickness
        )


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
