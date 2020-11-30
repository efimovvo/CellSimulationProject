from vis_module import *
from actions_module import *
from cells_classes_module import *


cell_1 = Cell()
cell_1.position = np.array([SCREEN_WIDTH, SCREEN_HEIGHT])
cell_2 = Cell()
cell_3 = Cell()
cell_3.predator = True
cell_3.multiply_skill = 0.9
cell_3.age_step = 0.1
cell_3.color = RED
cell_2.position = np.array([SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3])
meal_list = [Meal()]
cells = [cell_1, cell_2, cell_3]


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
        list_cell.append(new_cell)


def main():
    """Main function of program. It creates a screen where cells lives and makes an actions with them"""
    global meal_list

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.set_alpha(None)
    clock = pygame.time.Clock()
    FPS = 100
    finished = False
    while not finished:
        clean_screen(screen)
        clock.tick(FPS)
        print(clock.get_fps())
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
        if len(meal_list) < 15:
            meal_list.append(Meal())
        multiply(cells)
        update(cells, meal_list)

        # Draw all
        # Draw the meal on the screen
        draw_meal(meal_list, screen)
        # Draw the cells on the screen
        draw_cells(cells, screen)

        # Draw interface objects
        draw_user_panel(screen)
        # Draw population data
        draw_plot(screen)
        # Update the screen
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()