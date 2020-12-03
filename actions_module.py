from cells_classes_module import *
import numpy as np

ind = None


def probability_to_multiply():
    """Function returns float from (0, 1) """
    return random.uniform(0, 1)


def kill_the_cell(list_cell, cell, time):
    if cell in list_cell:
        list_cell.remove(cell)
        write_data(list_cell, time)


def born_the_cell(list_cell, cell, time):
    list_cell.append(cell)
    write_data(list_cell, time)


def multiply(list_cells, time):
    """:arg:    list_cells - list of cells, type : list
                time - time from begin simulation, type : float"""
    for cell in list_cells:
        p = probability_to_multiply()
        if cell.age >= 100 or cell.satiety <= 0:
            kill_the_cell(list_cells, cell, time)
        if (p > cell.multiply_skill
                and cell.reproductive_age[0] <= cell.age <= cell.reproductive_age[1]
                and cell.age - cell.age_of_last_multiplication > cell.reproductive_waiting
                and cell.satiety >= 0.5
        ):
            new_cell = cell.multiply(list_cells)
            if new_cell != 0:
                born_the_cell(list_cells, new_cell, time)


def update(list_cells, meal_list, time):
    """:arg    list_cells - list of cells, type : list

        Function updates cells positions. """
    victim_list = [cell for cell in list_cells if not cell.predator]
    for cell in list_cells:
        cell.calc_forces(meal_list, list_cells)
        cell.update()
        if cell.predator:
            if len(victim_list) != 0:
                for victim in victim_list:
                    if vec_module(find_vector(cell, victim)) <= victim.size:
                        kill_the_cell(list_cells, victim, time)
                        cell.satiety += victim.richness
                        cell.satiety = min(cell.satiety, 1)

        cell.age += cell.age_step
        cell.satiety -= cell.satiety_step

    for meal in meal_list:
        ind = False
        for cell in list_cells:
            if meal.eaten(cell):
                if not cell.predator:
                    cell.satiety += meal.richness
                    cell.satiety = min(cell.satiety, 1)
                meal_list.remove(meal)
                ind = True
                break
        if ind:
                break
