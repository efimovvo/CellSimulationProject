from vis_module import *
from actions_module import *
from cells_classes_module import *

cells = []
for i in range(50):
    new_cell = Cell()
    new_cell.position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
    new_cell.age = random.random() * 50
    cells.append(new_cell)
for i in range(7):
    new_cell = Cell()
    new_cell.position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
    new_cell.age = random.random() * 30
    new_cell.predator = True
    new_cell.color = RED
    new_cell.engines = 3 + (2 * random.random() - 1) ** 3
    new_cell.satiety_step = 0.005
    new_cell.reproductive_age = [20, 50]
    new_cell.reproductive_waiting = 3
    cells.append(new_cell)
meal_list = [Meal()]


def add_peaceful(pos, list_cell):
    if pos[0] > SCREEN_WIDTH or pos[0] < 0 or pos[1] > SCREEN_HEIGHT or pos[1] < PANEL_HEIGHT:
        pass
    else:
        new_cell = Cell()
        new_cell.position = np.array(pos)
        list_cell.append(new_cell)


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


def main():
    """Main function of program. It creates a screen where cells lives and makes an actions with them"""
    global meal_list
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
                    add_peaceful([event.pos[0], event.pos[1] - PANEL_HEIGHT], cells)
                elif event.button == 3:
                    add_predator([event.pos[0], event.pos[1] - PANEL_HEIGHT], cells)

        # Update all date for one time step
        if len(meal_list) < 20:
            meal_list.append(Meal())
        multiply(cells, time)
        update(cells, meal_list, time)

        # Draw all
        # Draw the meal on the screen
        draw_meal(meal_list, screen)
        # Draw the cells on the screen
        draw_cells(cells, screen)

        # Draw interface objects
        draw_user_panel(screen)
        # Draw population data
        graph(screen)
        # Update the screen
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
    file = open('data.txt', 'w')
    file.close()
