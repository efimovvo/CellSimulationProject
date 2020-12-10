from cells_classes_module import *
from in_out_module import *
from vis_module import *
import numpy as np

ind = None


def probability_to_multiply():
    """Function returns float from (0, 1) """
    return random.uniform(0, 1)


def change_age_step(list_cell, status):
    """:arg :   list_cell - type : list, each element Cell type
                status - type : int, status of button

    Function changes age step.
    """
    if status == 1:
        delta = 0.001
    else:
        delta = -0.001
    for i in range(len(list_cell)):
        list_cell[i].age_step += delta


def change_multiply_skill(list_cells, status):
    """:arg :   list_cell - type : list, each element Cell type
                   status - type : int, status of button

       Function changes multiply skill.
    """
    if status == 1:
        delta = 0.02
    else:
        delta = -0.02
    for i in range(len(list_cells)):
        list_cells[i].multiply_skill += delta


def kill_the_cell(list_cell, cell, time):
    """:arg     list_cell - type : list, each element is Cell type,
                cell - type : Cell, cell which was killed
                time - type : float, time when cell was killed

    Function removes cell from list cell and writes data about it"""

    if cell in list_cell:
        list_cell.remove(cell)  # cell removes from list
        write_data(list_cell, time)  # writes data about kill


def born_the_cell(list_cell, cell, time):
    """:arg     list_cell - type : list, each element is Cell type,
                    cell - type : Cell, cell which was born
                    time - type : float, time when cell was born

    Function removes cell from list cell and writes data about it"""
    list_cell.append(cell)  # cell adds to the list of cells
    write_data(list_cell, time)  # writes data about born


def multiply(list_cells, time, parameters):
    """:arg:    list_cells - list of cells, type : list, each element is Cell type
                time - time from begin simulation, type : float

    Function responsible for add new cell (cells multiply),
    kill cells if the last one is too old or too hungry"""

    for cell in list_cells:
        p = probability_to_multiply()  # chance cell to multiply
        if cell.age >= 100 or cell.satiety <= 0:  # cells could not live if they are too old or too hungry
            kill_the_cell(list_cells, cell, time)
        if (p > cell.multiply_skill
                # cells have to be if reproductive age to multiply :
                and cell.reproductive_age[0] <= cell.age <= cell.reproductive_age[1]
                # cells could not multiply each moment of time :
                and cell.age - cell.age_of_last_multiplication > cell.reproductive_waiting
                # cells have to have a lot of satiety to multiply :
                and cell.satiety >= 0.5):
            new_cell = cell.multiply(list_cells, parameters)  # new_cell = Cell() or 0
            # born the cell :
            if new_cell != 0:
                born_the_cell(list_cells, new_cell, time)


def update(list_cells, meal_list, time):
    """:arg    list_cells - list of cells, type : list, each element is Cell type
                meal_list - list of meal, type : list, each element is meal type
                time - time to update, type : float

    Function responsible for updates positions of cell and meal on the screen,
        kills the peaceful cells if they are attacked by predator cell,
        adds age of cell and gets lower satiety of cell"""

    victim_list = [cell for cell in list_cells if not cell.predator]  # list of cells with not predator
    for cell in list_cells:
        cell.calc_forces(meal_list, list_cells)  # calculate the forces
        cell.update()  # updates position of cells
        # is peaceful cell was eaten by predator :
        if cell.predator:
            if len(victim_list) != 0:
                for victim in victim_list:
                    # they are have to be close to each other :
                    if vec_module(find_vector(cell, victim)) <= victim.size:
                        # kills the cell :
                        kill_the_cell(list_cells, victim, time)
                        # adds satiety :
                        cell.satiety += victim.richness
                        # satiety have to be from 0 to 1 :
                        cell.satiety = min(cell.satiety, 1)

        cell.age += cell.age_step
        cell.satiety -= cell.satiety_step

    # it is checks if meal was eaten by peaceful cell :
    for meal in meal_list:

        meal_eaten = False  # special that responsible for eaten meal

        for cell in list_cells:
            if meal.eaten(cell):
                if not cell.predator:  # meal could be eaten only by peaceful cell
                    cell.satiety += meal.richness
                    cell.satiety = min(cell.satiety, 1)
                # meal removes from list when it is eaten :
                meal_list.remove(meal)

                meal_eaten = True
                break
        if meal_eaten:
            break
