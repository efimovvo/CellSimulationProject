from cells_classes_module import *
from in_out_module import *
from vis_module import *
import numpy as np

ind = None


def probability_to_multiply():
    """Function returns float from (0, 1) """
    return random.uniform(0, 1)


def change_age_step(list_cell, status):
    """:arg :   list_cell - type : list. Contains all elements with type 'Cell'
                status - type : int. Status of the button

    Function changes age step.

    """
    if status == 1:
        delta = 0.001
    else:
        delta = -0.001
    for i in range(len(list_cell)):
        list_cell[i].age_step += delta


def change_multiply_skill(list_cells, status):
    """:arg :   list_cell - type : list. Contains all elements with type 'Cell'
                   status - type : int. Status of the button

       Function changes multiply skill.

    """
    if status == 1:
        delta = 0.02
    else:
        delta = -0.02
    for i in range(len(list_cells)):
        list_cells[i].multiply_skill += delta


def kill_the_cell(list_cell, cell, time):
    """:arg:     list_cell - type : list. Contains all elements with type 'Cell'
                cell - type : Cell. A cell that was killed
                time - type : float. Moment of the time when the cell was killed

    Function removes cell from the list_cell and writes data about it

    """

    if cell in list_cell:
        list_cell.remove(cell)  # A cell removed from the list
        write_data(list_cell, time)  # Writes data about a dead cell


def born_the_cell(list_cell, cell, time):
    """:arg:     list_cell - type : list. Contains all elements with type 'Cell'
                cell - type : Cell. A cell that was born
                time - type : float. Moment of the time when the cell was born

    Function adds cell to the list_cell and writes data about it

    """
    list_cell.append(cell)  # A cell added to the list
    write_data(list_cell, time)  # Writes data about a new cell


def multiply(list_cells, time, parameters):
    """:arg:    list_cells - type : list. Contains all elements with type 'Cell'
                time -  type : float. How much time passed since the beginning of the simulation

    Function adds new cell (cells multiply) and kills cell if it is too old or too hungry

    """
    for cell in list_cells:
        p = probability_to_multiply()  # The chance of a cell to multiply
        if cell.age >= 100 or cell.satiety <= 0:  # A cell dies if it is too old or too hungry
            kill_the_cell(list_cells, cell, time)
        if (p > cell.multiply_skill
                # Cells have to be if reproductive age to multiply :
                and cell.reproductive_age[0] <= cell.age <= cell.reproductive_age[1]
                # Cells could not multiply each moment of time :
                and cell.age - cell.age_of_last_multiplication > cell.reproductive_waiting
                # Cells have to have a lot of satiety to multiply :
                and cell.satiety >= 0.5):
            new_cell = cell.multiply(list_cells, parameters)  # new_cell = Cell() or 0
            # Born the cell :
            if new_cell != 0:
                born_the_cell(list_cells, new_cell, time)


def update(list_cells, meal_list, time):
    """:arg:    list_cells - type : list. Contains all elements with type 'Cell'
                meal_list - type : list. Contains all elements with type 'Meal'
                time - type : float. The moment of time when update is called

    Updates of cell's and meal's positions on the screen;
    kills the peaceful cells if they are attacked by predator cell;
    adds age of cell and gets lower satiety of cell

    """

    victim_list = [cell for cell in list_cells if not cell.predator]  # List of the peaceful cells
    for cell in list_cells:
        cell.calc_forces(meal_list, list_cells)  # Calculates forces
        cell.update()  # Updates a position of the cells
        # Is a peaceful cell was eaten by a predator :
        if cell.predator:
            if len(victim_list) != 0:
                for victim in victim_list:
                    # They are have to be close to each other :
                    if vec_module(find_vector(cell, victim)) <= victim.size:
                        # Kills a cell :
                        kill_the_cell(list_cells, victim, time)
                        # Adds satiety :
                        cell.satiety += victim.richness
                        # Satiety have to be from 0 to 1 :
                        cell.satiety = min(cell.satiety, 1)

        cell.age += cell.age_step
        cell.satiety -= cell.satiety_step

    # It checks was meal eaten by peaceful cell or not:
    for meal in meal_list:

        meal_eaten = False  # Special that responsible for eaten meal

        for cell in list_cells:
            if meal.eaten(cell):
                if not cell.predator:  # Meal could be eaten only by peaceful cell
                    cell.satiety += meal.richness
                    cell.satiety = min(cell.satiety, 1)
                # Meal removed from the list when it is eaten :
                meal_list.remove(meal)

                meal_eaten = True
                break
        if meal_eaten:
            break
