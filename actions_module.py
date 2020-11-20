from cells_classes_module import *
import numpy as np

ind = None


def probability_to_multiply():
    """Function returns float from (0, 1) """
    return random.uniform(0, 1)


def create_new_cell(cell_s, list_cells):
    """:arg:    cell_center - center of cell, type : tuple
                list cells - list of cells, type : list
        Function adds new cell at the list of cells"""
    global ind  # variable that responds for spawn new cell. bool
    if cell_s.predator:
        new_cell = Predator()
    else:
        new_cell = FirstCell()

    new_cell.time_multiply = cell_s.time_multiply + cell_s.multiply_freq
    new_cell.vx = cell_s.vx
    new_cell.vy = cell_s.vy
    new_cell.multiply = cell_s.multiply
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
        p = probability_to_multiply()

        if t > cell.time_multiply and p > cell.multiply:  # do  spawn cell or no
            create_new_cell(cell, list_cells)
            cell.time_multiply += cell.multiply_freq


def update(list_cells):
    """:arg    list_cells - list of cells, type : list

        Function updates cells positions. """

    for cell in list_cells:
        cell.update()
        if cell.vx == 0 and cell.vy == 0:  # stop neighbors next to staying cells
            for neighbor in list_cells:
                if (cell.center[0] - neighbor.center[0]) ** 2 + (cell.center[1] - neighbor.center[1]) ** 2 < (
                        2 * cell.r) ** 2:
                    neighbor.vx = neighbor.vy = 0


def zombie_cell(peaceful_cell, predator, t):
    """:arg     peaceful_cell - type : FirstCell, the peaceful cell which turns into predator
                predator - type : Predator, the predator cell which makes a peaceful cell to predator
                t - type : float, milliseconds, time when predator makes an attack

    Function returns zombie - type Predator, speed as predator, cords - peaceful_cell"""
    zombie = Predator()
    zombie.center = peaceful_cell.center  # make the center of zombie in peaceful cell
    zombie.vx = predator.vx
    zombie.vy = predator.vy
    zombie.time_multiply = t + zombie.multiply_freq  # zombie have to multiply
    zombie.time_attack = t + zombie.freq_attack  # zombie have to attack
    return zombie


def peaceful_cell(predator, t):
    """:arg     predator - type : Predator, predator cell which turns into FirstCell (peaceful)
                t - type : float, milliseconds, time when predator turns to peaceful

    Function returns p_cell - type : FirstCell, center and velocity as predator had"""
    p_cell = FirstCell()
    p_cell.center = predator.center
    p_cell.vx = predator.vx
    p_cell.vy = predator.vy
    p_cell.time_multiply = t + p_cell.multiply_freq
    return p_cell


def predator_attack(list_cells, t):
    """:arg     list_cells - type : list, list of cells
                t - type : float, milliseconds from begin init

    Function turns peaceful cell into predator if they are close, turns predator into peaceful cell if there are more
    than 2 peaceful neighbors close to predator cell"""

    for j in range(len(list_cells)):
        if list_cells[j].predator:
            p_neighbors_num = count_peaceful_cells(list_cells, list_cells[j])  # get the count of peaceful cell
            if p_neighbors_num >= 2:
                list_cells[j] = peaceful_cell(list_cells[j], t)  # turns cell into peaceful cell
            else:
                for i in range(len(list_cells)):
                    if list_cells[i].predator:  # predator cannot make predator from predator cell
                        continue
                    if (list_cells[i].center[0] - list_cells[j].center[0]) ** 2 + (
                            list_cells[i].center[1] - list_cells[j].center[1]) ** 2 <= (
                            2.2 * list_cells[j].r) ** 2 and t > list_cells[j].time_attack:  # check if cells are close,
                        # and the time can allow to attack
                        for neighbors in list_cells:  # gives the velocity as neighbors
                            neighbors.vx = list_cells[j].vx
                            neighbors.vy = list_cells[j].vy
                        list_cells[i] = zombie_cell(list_cells[i], list_cells[j],
                                                    t)  # turns peaceful cell into predator
                        list_cells[j].time_attack += list_cells[j].freq_attack


def count_peaceful_cells(list_cell, cell):
    """:arg     list_cell - type : list, list of cells
                cell - type : cell type, cell

    Function returns amount of peaceful neighbors close to the cell"""
    count = 0
    for neighbor in list_cell:
        if (cell.center[0] - neighbor.center[0]) ** 2 + (cell.center[1] - neighbor.center[1]) ** 2 <= (
                2.2 * cell.r) ** 2 and (
                not neighbor.predator):
            count += 1
    return count
