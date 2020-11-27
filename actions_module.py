from cells_classes_module import *
import numpy as np

ind = None


def probability_to_multiply():
    """Function returns float from (0, 1) """
    return random.uniform(0, 1)


def kill_the_cell(list_cell, cell):
    list_cell.remove(cell)


def born_the_cell(list_cell, cell):
    list_cell.append(cell)


def multiply(list_cells):
    """:arg:    list_cells - list of cells, type : list
                time - time from begin simulation, type : float"""
    for cell in list_cells:
        p = probability_to_multiply()
        if cell.age >= 100 or cell.satiety <= 0:
            kill_the_cell(list_cells, cell)
        if (p > cell.multiply_skill
                and cell.reproductive_age[0] <= cell.age <= cell.reproductive_age[1]
                and cell.age - cell.age_of_last_multiplication > cell.reproductive_waiting
                and cell.satiety >= 0.5
        ):
            new_cell = cell.multiply(list_cells)
            if new_cell != 0:
                born_the_cell(list_cells, new_cell)


def update(list_cells, meal_list):
    """:arg    list_cells - list of cells, type : list

        Function updates cells positions. """
    for cell in list_cells:
        cell.food_search(meal_list)
        cell.update()
        cell.age += cell.age_step
        cell.satiety -= 0.005

    for meal in meal_list:
        ind = False
        for cell in list_cells:
            if meal.eaten(cell):
                cell.satiety += meal.richness
                meal_list.remove(meal)
                ind = True
                break
        if ind:
                break
