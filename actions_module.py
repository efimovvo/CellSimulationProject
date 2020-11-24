from cells_classes_module import *
import numpy as np

ind = None


def probability_to_multiply():
    """Function returns float from (0, 1) """
    return random.uniform(0, 1)



def multiply(list_cells, t):
    """:arg:    list_cells - list of cells, type : list
                t - time from begin simulation, type : float"""
    for cell in list_cells:
        p = probability_to_multiply()
        cell.age += cell.age_step
        print(cell.age)
        if p > cell.multiply_skill and cell.reproductive_age[0] <= cell.age <= cell.reproductive_age[1] and (
            t - cell.age > cell.reproductive_waiting
        ):
            new_cell = cell.multiply(list_cells)
            if new_cell != 0:
                list_cells.append(new_cell)


def update(list_cells, meal_list):
    """:arg    list_cells - list of cells, type : list

        Function updates cells positions. """
    for cell in list_cells:
        cell.food_search(meal_list)
        cell.update()

    for i in range(len(meal_list)):
        ind = False
        for cell in list_cells:
            if meal_list[i].eaten(cell):
                meal_list.pop(i)
                ind = True
                break
        if ind:
                break
