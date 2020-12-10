from vis_module import *
from actions_module import *
from cells_classes_module import *


cell_list, meal_list = [], []


def restart_the_game(parameters):
    """Function returns cell_list with 50 different peaceful cells (type : list, each element is Cell) and
    meal_list (type : list, each element is Meal) with 20 different predator cells"""
    global cell_list, meal_list

    clean_file(file_name='data.txt')
    cell_list = []
    for i in range(50):
        position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        add_peaceful(position, cell_list, parameters)
    for i in range(20):
        position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        add_predator(position, cell_list, parameters)
    meal_list = [Meal()]


def add_peaceful(position, cell_list, parameters):
    """:arg     position - type : list, position of event
                cell_list - type : list, list of cells
    Function adds the new peaceful cell in the place, where mouse clicks"""

    # do not spawn cells outside screen :
    if (position[0] > SCREEN_WIDTH or position[0] < 0
            or position[1] > SCREEN_HEIGHT or position[1] < 0):
        pass
    # add new cell :
    else:
        new_cell = Cell(parameters[2].value, parameters[3].value, parameters[4].value)  # create Cell
        # random cell position :
        new_cell.position = position
        new_cell.age = random.random() * 50
        new_cell.satiety = random.random()  # random cell satiety
        cell_list.append(new_cell)


def add_predator(position, cell_list, parameters):
    """:arg     position - type : list, position of event
                    list_cell - type : list, list of cells
        Function adds the new predator cell in the place, where mouse clicks"""

    # do not spawn cells outside screen :
    if (position[0] > SCREEN_WIDTH or position[0] < 0
            or position[1] > SCREEN_HEIGHT or position[1] < 0):
        pass
    else:
        new_cell = Cell(parameters[2].value, parameters[3].value, 0.005)
        # random cell position :
        new_cell.position = position
        new_cell.age = random.random() * 20
        new_cell.predator = True  # special indicator that have only predator cells
        new_cell.color = RED  # color of predator cell
        new_cell.engines = 3 + (2 * random.random() - 1) ** 3
        new_cell.satiety = random.random()
        new_cell.reproductive_age = [20, 50]
        new_cell.reproductive_waiting = 3
        cell_list.append(new_cell)


def find_button(positon, button_list):
    """:arg     positon - type : list, position of event
                button_list - type : list, list of different buttons
    Function activates the button if it is clicked"""
    for button in button_list:
        if (button.position[0] <= positon[0] <= button.position[0] + button.size[0]
                and button.position[1] <= positon[1] <= button.position[1] + button.size[1]):
            eval(button.function)


def buttons(parameters):
    """Function returns list of buttons"""

    offset = 5
    button_height = PANEL_HEIGHT - 2 * offset
    button_height_small = (PANEL_HEIGHT - 3 * offset) // 2
    button_length = 80
    button_length_small = button_height_small

    # change graph button :
    button_graph = Button(
        [offset, offset],
        [1.5 * button_length, button_height],
        function='button.parameter.increase_modulo()',
        text='Change graph',
        parameter=parameters[0]
    )

    # change max food quantity
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

    # change age step
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

    # change multiply skill
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

    # change satiety
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

    # pause button
    point = button_satiety.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_pause = Button(
        point,
        [1.5 * button_length, button_height],
        function='pass',
        text='> / ||',
        parameter=''
    )

    # restart button
    point = button_pause.get_corner("top-right")
    point = [point[0] + offset, point[1]]
    button_restart = Button(
        point,
        [1.5 * button_length, button_height],
        function='restart_the_game()',
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
    round_set = [0, 3, 2, 4]
    for i in range(len(labels)):
        labels[i].text = round(parameters[i].value, round_set[i])


def update_parameters(parameters, cells):
    for cell in cells:
        cell.age_step = parameters[2].value
        cell.multiply_skill = parameters[3].value
        cell.satiety_step = parameters[4].value


def graphs(surf, button_list, time_list, victims_list, predators_list,
           victims_list_mid_age, predators_list_mid_age, victims_list_mid_engine, predators_list_mid_engine,
           victims_list_mid_satiety, predators_list_mid_satiety):

    """Function draws graphs on the surf. It depends what type of button is pushed"""
    # for top graph
    if len(time_list) > 0:
        # for 0 type :
        if button_list[0].parameter.value == 0:
            draw_graph(surf,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=time_list,
                       y_data=[victims_list, predators_list],
                       axis_comment=["Время, шаг симуляции", "Популяция, шт."],
                       graph_name="График зависимости размера популяции от времени")

        # for 1 type :
        elif button_list[0].parameter.value == 1:
            draw_graph(surf,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=time_list,
                       y_data=[victims_list_mid_age, predators_list_mid_age],
                       axis_comment=["Время, шаг симуляции", "Средний возраст популяции, ед. возраста"],
                       graph_name="График зависимости возраста популяции от времени")

        # for 2 type :
        elif button_list[0].parameter.value == 2:
            draw_graph(surf,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=time_list,
                       y_data=[victims_list_mid_engine, predators_list_mid_engine],
                       axis_comment=["Время, шаг симуляции", "Ср. подвижность по популяции, ед. подв-ти"],
                       graph_name="График зависимости средней подвижности от времени")
        # for 3 type
        else:
            draw_graph(surf,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=time_list,
                       y_data=[victims_list_mid_satiety, predators_list_mid_satiety],
                       axis_comment=["Время, шаг симуляции", "Средняя сытость по популяции, % сытости"],
                       graph_name="График зависимости средней сытости от времени")

    # for bottom graph
    if len(victims_list) > 0:
        draw_graph(surf,
                   starting_point=[SCREEN_WIDTH, PANEL_HEIGHT + SCREEN_HEIGHT // 2],
                   sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                   x_data=victims_list,
                   y_data=[predators_list],
                   axis_comment=["Популяция жертв, шт.", "Популяция хищников, шт."],
                   graph_name="Фазовая диаграмма: зависимость популяции хищников от популяции жертв",
                   x_scale=10 * (max(victims_list) // 10 + 1))


def cells_parameters(list_cell, button_list):
    """:arg :   list_cell - type : list, each element is Cell type
                button_list - type : list, each element if Button type

    Function changes cells parameters if button was pressed.
    """
    # decrease max food number :
    if button_list[1].status == 1:
        change_food_max_quantity(2)
        button_list[1].status = 0

    # increase max food number :
    elif button_list[2].status == 1:
        change_food_max_quantity(1)
        button_list[2].status = 0

    # increase age step :
    elif button_list[4].status == 1:
        change_age_step(list_cell, 1)
        button_list[4].status = 0
    # decrease age step :
    elif button_list[5].status == 1:
        change_age_step(list_cell, 2)
        button_list[5].status = 0

    '''# decrease multiply skill :
    elif button_list[7].status == 1:
        change_multiply_skill(list_cell, 2)
        button_list[7].status = 0
    # increase multiply skill :
    elif button_list[8].status == 1:
        change_multiply_skill(list_cell, 1)
        button_list[8].status = 0'''


def main():
    """Main function of program. It creates a screen where cells lives and makes an actions with them"""

    # Interface parameters
    user_parameter_set = user_parameters()

    # Buttons
    button_list = buttons(user_parameter_set)  # creates a button list

    restart_the_game(user_parameter_set)  # creates the cells and the meal lists
    time = 0
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.set_alpha(None)
    clock = pygame.time.Clock()
    fps = 100
    finished = False
    while not finished:
        time += 1
        clean_screen(screen)
        clock.tick(fps)
        # Check the users actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if the right button of mouse is clicked :
                if event.button == 1:
                    # add peaceful cell :
                    add_peaceful(np.array([event.pos[0], event.pos[1] - PANEL_HEIGHT]),
                                 cell_list,
                                 user_parameter_set)
                    # button activate :
                    find_button(event.pos, button_list)
                    # if the left button of mouse is clicked
                    update_labels(labels=button_list[3::4],
                                  parameters=user_parameter_set[1:])
                    update_parameters(user_parameter_set, cell_list)
                elif event.button == 3:
                    # add predator cell :
                    add_predator(np.array([event.pos[0], event.pos[1] - PANEL_HEIGHT]),
                                 cell_list,
                                 user_parameter_set)

        # Update all date for one time step
        if len(meal_list) < user_parameter_set[1].value:
            meal_list.append(Meal())
        multiply(cell_list, time, user_parameter_set)
        update(cell_list, meal_list, time)

        # Draw all
        # Draw the meal on the screen
        draw_meal(meal_list, screen)
        # Draw the cells on the screen
        draw_cells(cell_list, screen)

        # Draw interface objects
        draw_user_panel(screen, button_list)
        # Draw population data
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

        # Update the screen
        pygame.display.flip()

    save_file(file_name='data.txt', folder_name='database')
    pygame.quit()


if __name__ == '__main__':
    main()
