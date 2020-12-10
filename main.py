from vis_module import *
from actions_module import *
from cells_classes_module import *


def restart_the_game():
    """Function returns cell_list with 50 different peaceful cells (type : list, each element is Cell) and
    meal_list (type : list, each element is Meal) with 20 different predator cells"""
    cell_list = []
    for i in range(50):
        new_cell = Cell()  # create Cell
        # random cell position :
        new_cell.position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        new_cell.age = random.random() * 50
        new_cell.satiety = random.random()  # random cell satiety
        cell_list.append(new_cell)
    for i in range(20):
        new_cell = Cell()
        # random cell position :
        new_cell.position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        new_cell.age = random.random() * 20
        new_cell.predator = True  # special indicator that have only predator cells
        new_cell.color = RED  # color of predator cell
        new_cell.engines = 3 + (2 * random.random() - 1) ** 3
        new_cell.satiety = random.random()
        new_cell.satiety_step = 0.005
        new_cell.reproductive_age = [20, 50]
        new_cell.reproductive_waiting = 3
        cell_list.append(new_cell)
    meal_list = [Meal()]
    return cell_list, meal_list


def add_peaceful(position, cell_list):
    """:arg     position - type : list, position of event
                cell_list - type : list, list of cells
    Function adds the new peaceful cell in the place, where mouse clicks"""

    # do not spawn cells outside screen :
    if (position[0] > SCREEN_WIDTH or position[0] < 0
            or position[1] > SCREEN_HEIGHT or position[1] < PANEL_HEIGHT):
        pass
    # add new cell :
    else:
        new_cell = Cell()
        new_cell.position = np.array(position)
        cell_list.append(new_cell)


def add_predator(position, list_cell):
    """:arg     position - type : list, position of event
                    list_cell - type : list, list of cells
        Function adds the new predator cell in the place, where mouse clicks"""

    # do not spawn cells outside screen :
    if position[0] > SCREEN_WIDTH or position[0] < 0 or position[1] > SCREEN_HEIGHT or position[1] < PANEL_HEIGHT:
        pass
    else:
        # spawns predator cell :
        new_cell = Cell()
        new_cell.predator = True
        new_cell.color = RED
        new_cell.position = np.array(position)
        new_cell.engines = 2 + (random.random() * 2) ** 0.5
        new_cell.satiety_step = 0.005
        new_cell.reproductive_age = [5, 50]
        new_cell.reproductive_waiting = 3
        list_cell.append(new_cell)


def find_button(positon, button_list):
    """:arg     positon - type : list, position of event
                button_list - type : list, list of different buttons
    Function activates the button if it is clicked"""
    for button in button_list:
        if not button.switch:
            if (button.position[0] <= positon[0] <= button.position[0] + button.size[0]
                    and button.position[1] <= positon[1] <= button.position[1] + button.size[1]):
                button.click()
        else:
            if (button.position[0] <= positon[0] <= button.position[0] + button.size[0]
                    and button.position[1] <= positon[1] <= button.position[1] + button.size[1]):
                button.status = 1


def buttons():
    """Function returns list of buttons"""

    offset = 10
    # change graph button :
    button_graph = Button([offset, offset], [100, PANEL_HEIGHT - 2 * offset], '', 'Change graph')

    button_decrease = Button([button_graph.position[0] + button_graph.size[0] + 10, button_graph.position[1]],
                             [0.5 * button_graph.size[0], 0.5 * button_graph.size[1]], '', '-')
    button_increase = Button([button_graph.position[0] + 2 * button_graph.size[0] + 20 + button_decrease.size[0],
                              button_graph.position[1]], [0.5 * button_graph.size[0], 0.5 * button_graph.size[1]], '', '+')

    # change age step button :
    button_change_age_step = Button([400, 10], [100, 20], '', 'Change age step')
    button_age_step_increase = Button([510, 10], [20, 20], '', '+')
    button_age_step_decrease = Button([370, 10], [20, 20], '', '-')

    # change multiply skill button
    button_change_multiply_skill = Button([600, 10], [130, 20], '', 'Change multiply skill')
    button_multiply_skill_increase = Button([750, 10], [20, 20], '', '+')
    button_multiply_skill_decrease = Button([570, 10], [20, 20], '', '-')

    # indicate what type of buttons
    button_increase.switch = button_decrease.switch = button_age_step_increase.switch = \
        button_age_step_decrease.switch = button_multiply_skill_increase.switch = \
        button_multiply_skill_decrease.switch = True


    button_list = [button_graph, button_decrease, button_increase,
                   button_change_age_step, button_age_step_increase, button_age_step_decrease,
                   button_change_multiply_skill, button_multiply_skill_decrease, button_multiply_skill_increase]

    return button_list


def graphs(surf, button_list, time_list, victims_list, predators_list,
           victims_list_mid_age, predators_list_mid_age, victims_list_mid_engine, predators_list_mid_engine,
           victims_list_mid_satiety, predators_list_mid_satiety):

    """Function draws graphs on the surf. It depends what type of button is pushed"""

    # for 0 type :
    if button_list[0].status == 0:
        draw_graph(surf,
                   starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                   sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                   x_data=time_list,
                   y_data=[victims_list, predators_list],
                   axis_comment=["Время, шаг симуляции", "Популяция, шт."],
                   graph_name="График зависимости размера популяции от времени")

    # for 1 type :
    elif button_list[0].status == 1:
        draw_graph(surf,
                   starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                   sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                   x_data=time_list,
                   y_data=[victims_list_mid_age, predators_list_mid_age],
                   axis_comment=["Время, шаг симуляции", "Средний возраст популяции, ед. возраста"],
                   graph_name="График зависимости возраста популяции от времени")

    # for 2 type :
    elif button_list[0].status == 2:
        draw_graph(surf,
                   starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                   sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                   x_data=time_list,
                   y_data=[victims_list_mid_engine, predators_list_mid_engine],
                   axis_comment=["Время, шаг симуляции", "Средняя подвижность по популяции, ед. подвижности"],
                   graph_name="График зависимости возраста популяции от времени")
    # for 3 type
    else:
        draw_graph(surf,
                   starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                   sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                   x_data=time_list,
                   y_data=[victims_list_mid_satiety, predators_list_mid_satiety],
                   axis_comment=["Время, шаг симуляции", "Средняя сытость по популяции, % сытости"],
                   graph_name="График зависимости возраста популяции от времени")


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
    button_list = buttons()  # creates a button list
    offset = 10

    button_graph = Button([offset, offset], [50, PANEL_HEIGHT - 2 * offset], 'graph', '№1')
    button_decrease_meal = Button([button_graph.position[0] + button_graph.size[0] + BUTTON_DISTANCE,
                                   button_graph.position[1] + 0.5 * button_graph.size[1]],
                                  [0.5 * button_graph.size[0], 0.5 * button_graph.size[1]], 'decrease_meal', '-')
    button_increase_meal = Button([button_graph.position[0] + 2 * button_graph.size[0] + 2 * BUTTON_DISTANCE
                                   + button_decrease_meal.size[0], button_graph.position[1] + 0.5 * button_graph.size[1]
                                   ], [0.5 * button_graph.size[0], 0.5 * button_graph.size[1]], 'increase_meal', '+')

    button_decrease_satiety = Button([button_graph.position[0] + 3 * button_graph.size[0] + 3 * BUTTON_DISTANCE,
                                      button_graph.position[1] + 0.5 * button_graph.size[1]],
                                     [0.5 * button_graph.size[0], 0.5 * button_graph.size[1]], 'decrease_satiety', '-')
    button_increase_satiety = Button([button_graph.position[0] + 4.5 * button_graph.size[0] + 4 * BUTTON_DISTANCE,
                                      button_graph.position[1] + 0.5 * button_graph.size[1]],
                                     [0.5 * button_graph.size[0], 0.5 * button_graph.size[1]], 'increase_satiety', '+')

    button_pause = Button([button_graph.position[0] + 5 * button_graph.size[0] + 5 * BUTTON_DISTANCE,
                           button_graph.position[1]], [button_graph.size[0], button_graph.size[1]], 'pause/play', '||')

    button_restart = Button([button_graph.position[0] + 6 * button_graph.size[0] + 6 * BUTTON_DISTANCE,
                             button_graph.position[1]], [button_graph.size[0], button_graph.size[1]], 'restart', 'Restart')

    button_list = [button_graph, button_decrease_meal, button_increase_meal,
                   button_decrease_satiety, button_increase_satiety, button_pause, button_restart]  # creates a button list

    cell_list, meal_list = restart_the_game()  # creates the cells and the meal lists
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
                    add_peaceful([event.pos[0], event.pos[1] - PANEL_HEIGHT], cell_list)
                    # button activate :
                    find_button(event.pos, button_list)
                # if the left button of mouse is clicked :
                elif event.button == 3:
                    # add predator cell :
                    add_predator([event.pos[0], event.pos[1] - PANEL_HEIGHT], cell_list)

        # Update all date for one time step
        if len(meal_list) < food_max_quantity():
            meal_list.append(Meal())
        multiply(cell_list, time)
        update(cell_list, meal_list, time)

        # Draw all
        # Draw the meal on the screen
        draw_meal(meal_list, screen)
        # Draw the cells on the screen
        draw_cells(cell_list, screen)

        # Draw interface objects
        draw_user_panel(screen, button_list, cell_list[0])
        # Draw population data
        (time_list,
         victims_list, predators_list,
         victims_list_mid_age, predators_list_mid_age,
         victims_list_mid_engine, predators_list_mid_engine,
         victims_list_mid_satiety, predators_list_mid_satiety) = read_data()
        if len(time_list) > 0:
            graphs(screen, button_list, time_list,
                   victims_list, predators_list,
                   victims_list_mid_age, predators_list_mid_age,
                   victims_list_mid_engine, predators_list_mid_engine,
                   victims_list_mid_satiety, predators_list_mid_satiety)

            cells_parameters(cell_list, button_list)

        if len(victims_list) > 0:
            draw_graph(screen,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT + SCREEN_HEIGHT // 2],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=victims_list,
                       y_data=[predators_list],
                       axis_comment=["Популяция жертв, шт.", "Популяция хищников, шт."],
                       graph_name="Фазовая диаграмма: зависимость популяции хищников от популяции жертв",
                       x_scale=10 * (max(victims_list) // 10 + 1))

        # Update the screen
        pygame.display.flip()

    save_file()
    pygame.quit()


if __name__ == '__main__':
    main()
