import random
from cells_classes_module import *
import numpy as np

ind = None


def probabilty_to_multiply():
    """Function returns float from (0, 1) """
    return random.uniform(0, 1)


def create_new_cell(cell_s, list_cells):
    """:arg:    cell_center - center of cell, type : tuple
                list cells - list of cells, type : list
        Function adds new cell at the list of cells"""
    global ind  # variable that responds for spawn new cell. bool
    new_cell = FirstCell()
    new_cell.time_multiply = cell_s.time_multiply + cell_s.multiply_freq
    new_cell.vx = cell_s.vx
    new_cell.vy = cell_s.vy
    phi = random.uniform(0, 2 * np.pi)  # random phi
    x = cell_s.center[0] + 2 * new_cell.r * np.cos(phi)  # x cor of center new cell
    y = cell_s.center[1] + 2 * new_cell.r * np.sin(phi)  # y cor of center new cell
    ind = True
    for cell in list_cells:  # do not spawn cells on each other
        if (cell.center[0] - x) ** 2 + (cell.center[1] - y) ** 2 <= (2 * cell.r) ** 2 or (
                x >= WIDTH or y >= HEIGHT or x <= 0 or y <= 0
        ):
            ind = False
            break

    if ind:
        new_cell.center = [int(x), int(y)]
        list_cells.append(new_cell)


def multiply(list_cells, t):
    """:arg:    list_cells - list of cells, type : list
                t - time from begin simulation, type : float"""

    for cell in list_cells:
        p = probabilty_to_multiply()

        cell.update()
        if t > cell.time_multiply and p > cell.multiply:  # do  spawn cell or no
            create_new_cell(cell, list_cells)
            cell.time_multiply += cell.multiply_freq

