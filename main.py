from actions_module import *
from cells_classes_module import *


cell_list, meal_list = [], []
time = 0
time_step = 1


def restart_the_game(parameters):
    """ Function returns cell_list with 50 different peaceful cells and 20 predators
        and the meal_list.

        :param parameters : list(UserPanelParameter) : user parameters
    """
    global cell_list, meal_list, time, time_step

    clean_file(file_name='data.txt')
    time = 0
    time_step = 1
    cell_list = []
    for i in range(50):
        position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        add_peaceful(position, cell_list, parameters)
    for i in range(20):
        position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        add_predator(position, cell_list, parameters)
    meal_list = [Meal()]


def add_peaceful(position, cells, parameters):
    """ Function adds the new peaceful cell to the place,
        where mouse was clicked.

        :param position : list : position of event
        :param cells : list(Cell) : list of cells
        :param parameters : list(UserPanelParameter) : user parameters
    """

    # Do not spawn cells outside screen
    if (position[0] > SCREEN_WIDTH or position[0] < 0
            or position[1] > SCREEN_HEIGHT or position[1] < 0):
        pass
    # Adds new cell
    else:
        # Creates cell
        new_cell = Cell(parameters[2].value, parameters[3].value, parameters[4].value)
        new_cell.position = position  # Generates random cell's position
        new_cell.age = random.random() * 50  # Generates random cell's age
        new_cell.satiety = random.random()  # Generates random cell's satiety
        cells.append(new_cell)


def add_predator(position, cells, parameters):
    """ Function adds the new predator cell in the place,
        where mouse clicks.

        :param position : list : position of event
        :param cells : list(Cell) : list of cells
        :param parameters : list(UserPanelParameter) : user parameters
    """

    # Do not spawn cells outside screen
    if (position[0] > SCREEN_WIDTH or position[0] < 0
            or position[1] > SCREEN_HEIGHT or position[1] < 0):
        pass
    else:
        # Creates cell
        new_cell = Cell(parameters[2].value, parameters[3].value, 0.005)
        # Generates random cell position
        new_cell.position = position
        new_cell.age = random.random() * 20
        new_cell.predator = True  # Special indicator that have only predators
        new_cell.color = RED  # Color of the predator
        new_cell.engines = 3 + (2 * random.random() - 1) ** 3
        new_cell.satiety = random.random()
        new_cell.reproductive_age = [20, 50]
        new_cell.reproductive_waiting = 3
        cells.append(new_cell)


def find_button(position, buttons):
    """ Function activates the button if it is clicked.

        :param position : list : position of event
        :param buttons : list(Button) : list of cells
    """
    global time_step

    for button in buttons:
        if (button.position[0] <= position[0] <= button.position[0] + button.size[0]
                and button.position[1] <= position[1] <= button.position[1] + button.size[1]):
            if button.function == 'Play/Pause':
                time_step = (time_step + 1) % 2
            elif button.function != 'pass':
                eval(button.function)


def buttons(parameters):
    """Function returns list of buttons"""

    offset = 5
    button_height = PANEL_HEIGHT - 2 * offset
    button_height_small = (PANEL_HEIGHT - 3 * offset) // 2
    button_length = 80
    button_length_small = button_height_small

    # Changes a graph's button :
    button_graph = Button(
        [offset, offset],
        [1.5 * button_length, button_height],
        function='button.parameter.increase_modulo()',
        text='Change graph',
        parameter=parameters[0]
    )

    # Changes a maximum of the  food quantity
    point = button_graph.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_max_food = Button(
        point,
        [2 * button_length, button_height_small],
        function='pass',
        text='Number of meal',
        parameter=parameters[1]
    )

    point = button_max_food.get_corner("bottom-left")
    point = [point[0], point[1] + offset]
    button_max_food_decrease = Button(
        point,
        [button_length_small, button_height_small],
        function='button.parameter.decrease()',
        text='-',
        parameter=parameters[1]
    )

    point = button_max_food_decrease.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_max_food_value = Button(
        point,
        [2 * button_length - 2 * button_length_small - 2 * offset, button_height_small],
        function='pass',
        text=parameters[1].value,
        parameter=parameters[1]
    )

    point = button_max_food_value.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_max_food_increase = Button(
        point,
        [button_length_small, button_height_small],
        function='button.parameter.increase()',
        text='+',
        parameter=parameters[1]
    )

    # Changes a age step
    point = button_max_food.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_age_step = Button(
        point,
        [2 * button_length, button_height_small],
        function='pass',
        text='Age step',
        parameter=parameters[2]
    )

    point = button_age_step.get_corner("bottom-left")
    point = [point[0], point[1] + offset]
    button_age_step_decrease = Button(
        point,
        [button_length_small, button_height_small],
        function='button.parameter.decrease()',
        text='-',
        parameter=parameters[2]
    )

    point = button_age_step_decrease.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_age_step_value = Button(
        point,
        [2 * button_length - 2 * button_length_small - 2 * offset, button_height_small],
        function='pass',
        text=parameters[2].value,
        parameter=parameters[2]
    )

    point = button_age_step_value.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_age_step_increase = Button(
        point,
        [button_length_small, button_height_small],
        function='button.parameter.increase()',
        text='+',
        parameter=parameters[2]
    )

    # Change a multiply skill
    point = button_age_step.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_multiply_skill = Button(
        point,
        [2 * button_length, button_height_small],
        function='pass',
        text='Multiply skill',
        parameter=parameters[3]
    )

    point = button_multiply_skill.get_corner("bottom-left")
    point = [point[0], point[1] + offset]
    button_multiply_skill_decrease = Button(
        point,
        [button_length_small, button_height_small],
        function='button.parameter.decrease()',
        text='-',
        parameter=parameters[3]
    )

    point = button_multiply_skill_decrease.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_multiply_skill_value = Button(
        point,
        [2 * button_length - 2 * button_length_small - 2 * offset, button_height_small],
        function='pass',
        text=parameters[3].value,
        parameter=parameters[3]
    )

    point = button_multiply_skill_value.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_multiply_skill_increase = Button(
        point,
        [button_length_small, button_height_small],
        function='button.parameter.increase()',
        text='+',
        parameter=parameters[3]
    )

    # Changes a satiety
    point = button_multiply_skill.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_satiety = Button(
        point,
        [2 * button_length, button_height_small],
        function='pass',
        text='Satiety step',
        parameter=parameters[4]
    )

    point = button_satiety.get_corner("bottom-left")
    point = [point[0], point[1] + offset]
    button_satiety_decrease = Button(
        point,
        [button_length_small, button_height_small],
        function='button.parameter.decrease()',
        text='-',
        parameter=parameters[4]
    )

    point = button_satiety_decrease.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_satiety_value = Button(
        point,
        [2 * button_length - 2 * button_length_small - 2 * offset, button_height_small],
        function='pass',
        text=parameters[4].value,
        parameter=parameters[4]
    )

    point = button_satiety_value.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_satiety_increase = Button(
        point,
        [button_length_small, button_height_small],
        function='button.parameter.increase()',
        text='+',
        parameter=parameters[4]
    )

    # A pause button
    point = button_satiety.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_pause = Button(
        point,
        [1.5 * button_length, button_height],
        function='Play/Pause',
        text='> / ||',
        parameter=''
    )

    # A restart button
    point = button_pause.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_restart = Button(
        point,
        [1.5 * button_length, button_height],
        function='restart_the_game(parameters)',
        text='Restart',
        parameter=''
    )

    button_list = [button_graph,
                   button_max_food, button_max_food_decrease,
                   button_max_food_value, button_max_food_increase,
                   button_age_step, button_age_step_decrease,
                   button_age_step_value, button_age_step_increase,
                   button_multiply_skill, button_multiply_skill_decrease,
                   button_multiply_skill_value, button_multiply_skill_increase,
                   button_satiety, button_satiety_decrease,
                   button_satiety_value, button_satiety_increase,
                   button_pause, button_restart]

    return button_list


def user_parameters():
    """ Function creates user parameter set for user panel. """
    graph_number_parameter = UserPanelParameter('Номер графика', 0, 0, 3, 1)
    max_food_quantity_parameter = UserPanelParameter('Макс. кол-во еды', 20, 0, 200, 1)
    age_step_parameter = UserPanelParameter('Шаг старения', 3e-2, 0, 0.5, 1e-3)
    multiply_skill_parameter = UserPanelParameter('Сложность размножения', 0.8, 0, 1, 0.01)
    satiety_step_parameter = UserPanelParameter('Шаг сытости', 3e-3, 0, 0.5, 1e-4)
    return [graph_number_parameter,
            max_food_quantity_parameter,
            age_step_parameter,
            multiply_skill_parameter,
            satiety_step_parameter]


def update_labels(labels, parameters):
    """ Function updates text values in buttons that indicates
        the current values of user parameters.

        :param labels : list(Button) : list of buttons that indicates values
        :param parameters : list(UserPanelParameter) : list of parameters
    """
    round_set = [0, 3, 2, 4]
    for i in range(len(labels)):
        labels[i].text = round(parameters[i].value, round_set[i])


def update_parameters(parameters, cells):
    """ Function updates values of current parameters after changing.

        :param parameters : list(UserPanelParameter) : list of parameters
        :param cells : list(Cell) : list of cell
    """
    for cell in cells:
        cell.age_step = parameters[2].value
        cell.multiply_skill = parameters[3].value
        cell.satiety_step = parameters[4].value


def graphs(surf, button_list, time_list, victims_list, predators_list,
           victims_list_mid_age, predators_list_mid_age, victims_list_mid_engine, predators_list_mid_engine,
           victims_list_mid_satiety, predators_list_mid_satiety):

    """Function draws graphs on the surf. It depends what type of button is pushed"""
    # For the upper graph
    if len(time_list) > 0:
        # For 0 type
        if button_list[0].parameter.value == 0:
            draw_graph(surf,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=time_list,
                       y_data=[victims_list, predators_list],
                       axis_comment=["Время, шаг симуляции", "Популяция, шт."],
                       graph_name="График зависимости размера популяции от времени")

        # For 1 type :
        elif button_list[0].parameter.value == 1:
            draw_graph(surf,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=time_list,
                       y_data=[victims_list_mid_age, predators_list_mid_age],
                       axis_comment=["Время, шаг симуляции", "Средний возраст популяции, ед. возраста"],
                       graph_name="График зависимости возраста популяции от времени")

        # For 2 type :
        elif button_list[0].parameter.value == 2:
            draw_graph(surf,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=time_list,
                       y_data=[victims_list_mid_engine, predators_list_mid_engine],
                       axis_comment=["Время, шаг симуляции", "Ср. подвижность по популяции, ед. подв-ти"],
                       graph_name="График зависимости средней подвижности от времени")
        # For 3 type
        else:
            draw_graph(surf,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=time_list,
                       y_data=[victims_list_mid_satiety, predators_list_mid_satiety],
                       axis_comment=["Время, шаг симуляции", "Средняя сытость по популяции, % сытости"],
                       graph_name="График зависимости средней сытости от времени")

    # For the lower graph
    if len(victims_list) > 0:
        draw_graph(surf,
                   starting_point=[SCREEN_WIDTH, PANEL_HEIGHT + SCREEN_HEIGHT // 2],
                   sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                   x_data=victims_list,
                   y_data=[predators_list],
                   axis_comment=["Популяция жертв, шт.", "Популяция хищников, шт."],
                   graph_name="Фазовая диаграмма: зависимость популяции хищников от популяции жертв",
                   x_scale=10 * (max(victims_list) // 10 + 1))


def main():
    """Main function of program. It creates a screen where cells lives and makes an actions with them"""

    global time

    # Interface parameters
    user_parameter_set = user_parameters()

    # Buttons
    button_list = buttons(user_parameter_set)  # Creates a button list

    restart_the_game(user_parameter_set)  # Creates the cells and the meal lists
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.set_alpha(None)
    clock = pygame.time.Clock()
    fps = 100
    finished = False
    while not finished:
        time += time_step
        clean_screen(screen)
        clock.tick(fps)
        # Checks the users actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if the right button of the mouse is clicked
                if event.button == 1:
                    # Adds a peaceful cell
                    add_peaceful(np.array([event.pos[0], event.pos[1] - PANEL_HEIGHT]),
                                 cell_list,
                                 user_parameter_set)
                    # Calls a find_button function
                    find_button(event.pos, button_list, user_parameter_set)
                    # Checks if the left button of the mouse is clicked
                    update_labels(labels=button_list[3::4],
                                  parameters=user_parameter_set[1:])
                    update_parameters(user_parameter_set, cell_list)
                elif event.button == 3:
                    # Adds a predator
                    add_predator(np.array([event.pos[0], event.pos[1] - PANEL_HEIGHT]),
                                 cell_list,
                                 user_parameter_set)

        if time_step != 0:
            # Update all data for one time step
            if len(meal_list) < user_parameter_set[1].value:
                meal_list.append(Meal())
            multiply(cell_list, time, user_parameter_set)
            update(cell_list, meal_list, time)

        # Draws meal on the screen
        draw_meal(meal_list, screen)
        # Draws cells on the screen
        draw_cells(cell_list, screen)

        # Draws interface objects
        draw_user_panel(screen, button_list)
        # Draws population data
        (time_list,
         victims_list, predators_list,
         victims_list_mid_age, predators_list_mid_age,
         victims_list_mid_engine, predators_list_mid_engine,
         victims_list_mid_satiety, predators_list_mid_satiety) = read_data('data.txt')
        graphs(screen, button_list, time_list,
               victims_list, predators_list,
               victims_list_mid_age, predators_list_mid_age,
               victims_list_mid_engine, predators_list_mid_engine,
               victims_list_mid_satiety, predators_list_mid_satiety)

        # Updates the screen
        pygame.display.flip()

    save_file(file_name='data.txt', folder_name='database')
    pygame.quit()


if __name__ == '__main__':
    main()
