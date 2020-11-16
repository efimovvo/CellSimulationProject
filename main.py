from vis_module import *
from actions_module import *
WIDTH = 400
HEIGHT = 600


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(WHITE)
    test_cell = FirstCell()
    test_cells = []
    test_cells.append(test_cell)
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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
