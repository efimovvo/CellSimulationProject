from vis_module import *
from actions_module import *
from cells_classes_module import *


def restart_the_game():
    cell_list = []
    for i in range(50):
        new_cell = Cell()
        new_cell.position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        new_cell.age = random.random() * 50
        new_cell.satiety = random.random()
        cell_list.append(new_cell)
    for i in range(20):
        new_cell = Cell()
        new_cell.position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        new_cell.age = random.random() * 20
        new_cell.predator = True
        new_cell.color = RED
        new_cell.engines = 3 + (2 * random.random() - 1) ** 3
        new_cell.satiety = random.random()
        new_cell.satiety_step = 0.005
        new_cell.reproductive_age = [20, 50]
        new_cell.reproductive_waiting = 3
        cell_list.append(new_cell)
    meal_list = [Meal()]
    return cell_list, meal_list


def add_peaceful(position, cell_list):
    if (position[0] > SCREEN_WIDTH or position[0] < 0
            or position[1] > SCREEN_HEIGHT or position[1] < PANEL_HEIGHT):
        pass
    else:
        new_cell = Cell()
        new_cell.position = np.array(position)
        cell_list.append(new_cell)


def add_predator(pos, list_cell):
    if pos[0] > SCREEN_WIDTH or pos[0] < 0 or pos[1] > SCREEN_HEIGHT or pos[1] < PANEL_HEIGHT:
        pass
    else:
        new_cell = Cell()
        new_cell.predator = True
        new_cell.color = RED
        new_cell.position = np.array(pos)
        new_cell.engines = 2 + (random.random() * 2)**0.5
        new_cell.satiety_step = 0.005
        new_cell.reproductive_age = [5, 50]
        new_cell.reproductive_waiting = 3
        list_cell.append(new_cell)


def find_button(positon, button_list):
    for button in button_list:
        if (button.position[0] <= positon[0] <= button.position[0] + button.size[0]
                and button.position[1] <= positon[1] <= button.position[1] + button.size[1]):
            button.click()


def main():
    """Main function of program. It creates a screen where cells lives and makes an actions with them"""
    button_list = [Button([10, 10], [10, 10], 'Button')]
    cell_list, meal_list = restart_the_game()
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
                if event.button == 1:
                    add_peaceful([event.pos[0], event.pos[1] - PANEL_HEIGHT], cell_list)
                    find_button(event.pos, button_list)
                elif event.button == 3:
                    add_predator([event.pos[0], event.pos[1] - PANEL_HEIGHT], cell_list)

        # Update all date for one time step
        if len(meal_list) < FOOD_MAX_QUANTITY:
            meal_list.append(Meal())
        multiply(cell_list, time)
        update(cell_list, meal_list, time)

        # Draw all
        # Draw the meal on the screen
        draw_meal(meal_list, screen)
        # Draw the cells on the screen
        draw_cells(cell_list, screen)

        # Draw interface objects
        draw_user_panel(screen, button_list)
        # Draw population data
        victims_list, predators_list, time_list = read_data()
        if len(time_list) > 0:
            draw_graph(screen,
                       starting_point=[SCREEN_WIDTH, PANEL_HEIGHT],
                       sizes=[PLOT_AREA_WIDTH, SCREEN_HEIGHT // 2],
                       x_data=time_list,
                       y_data=[victims_list, predators_list],
                       axis_comment=["Время, шаг симуляции", "Популяция, шт."],
                       graph_name="График зависимости размера популяции от времени")
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

    pygame.quit()


if __name__ == '__main__':
    main()
    file = open('data.txt', 'w')
    file.close()
