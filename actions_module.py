import random
from cells_classes_module import *
import numpy as np
time_multiply = 2


def probabilty_to_multiply():
    return random.uniform(0, 1)


def create_new_cell(cell_center, list_cells):
    global ind
    new_cell = FirstCell()
    phi = random.uniform(0, 2*np.pi)
    x = cell_center[0] + 2.2*new_cell.r*np.cos(phi)
    y = cell_center[1] + 2.2*new_cell.r*np.sin(phi)
    ind = True
    for cell in list_cells:
        if (cell.center[0] - x)**2 + (cell.center[1] - y)**2 <= (2*cell.r)**2:
            ind = False
            break
    if ind:
        new_cell.center = (int(x), int(y))
        list_cells.append(new_cell)


def multiply(list_cells, t):
    global time_multiply, ind

    for cell in list_cells:
        ind = True
        if t > time_multiply and probabilty_to_multiply() > cell.multiply:
            create_new_cell(cell.center, list_cells)
            time_multiply += 0.1