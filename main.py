from vis_module import *
from actions_module import *
from cells_classes_module import *
WIDTH = 600
HEIGHT = 600
test_cell = FirstCell()  # first cells
test_cells = [test_cell]


def main():
    """Main function of program. It creates a screen where cells lives and makes an actions with them"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(WHITE)
    FPS = 30
    finished = False
    while not finished:
        clock.tick(FPS)
        time = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        multiply(test_cells, time)
        draw_cells(test_cells, screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
