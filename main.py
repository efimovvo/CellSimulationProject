from vis_module import *
from actions_module import *
from cells_classes_module import *


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


WIDTH = 600
HEIGHT = 600
test_cell = FirstCell()  # first cells
predator = Predator()  # first predator
test_cells = [test_cell, predator]


def main():
    """Main function of program. It creates a screen where cells lives and makes an actions with them"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    FPS = 100
    finished = False
    while not finished:
        screen.fill(WHITE)
        clock.tick(FPS)
        time = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        multiply(test_cells, time)
        update(test_cells)
        predator_attack(test_cells, time)
        draw_cells(test_cells, screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
