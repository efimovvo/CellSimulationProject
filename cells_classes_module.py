import random
import numpy as np
from vis_module import *


def vec_module(vector):
    return (vector[0]**2 + vector[1]**2)**0.5


def find_vector(obj1, obj2):
    return [-obj1.position[0] + obj2.position[0], -obj1.position[1] + obj2.position[1]]


def find_area(cell, list_meal):
    """Function returns vector in area where a lot of food
    :arg
        cell - on cell, type : cell
        list_meal - list of meal, type : list
    """
    vec_area = [0.0, 0.0]
    # Calculating vec_area direction
    for meal in list_meal:
        vector_to_meal = find_vector(cell, meal)
        vec_area[0] += (vector_to_meal[0] / vec_module(vector_to_meal)**2.5) * 100
        vec_area[1] += (vector_to_meal[1] / vec_module(vector_to_meal)**2.5) * 100

    # Normalization of vec_area
    vec_area[0] /= vec_module(vec_area)
    vec_area[1] /= vec_module(vec_area)
    print(vec_area)
    vec_area[0] *= cell.engines
    vec_area[1] *= cell.engines
    print(vec_area)

    return vec_area


class Cell:
    '''Common class for all cells
    attributes:
            multiply_skill - skill to multiply, float from 0 (the best) to 1 ( the worst)
            age - float, age of cell
            size - int, size of cell
            position - cords of center, list
            velocity - velocity of cell [vx, vy], list
            engines - describe how much cells will be move
            color - Tuple, color of cell
    '''
    def __init__(self):
        # Common property
        self.multiply_skill = 0.5
        self.age = 0
        self.size = 5
        self.position = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        self.velocity = [5, 5]
        # Genetic code
        self.shell_thickness = 0.5
        self.satiety = 0.6  # сытость
        self.satiety_step = 0.003
        self.engines = random.randint(1, 3)
        self.reproductive_age = [20, 50]
        self.age_step = 0.05
        self.age_of_last_multiplication = 0
        self.reproductive_waiting = 2
        self.aggressiveness = 0
        self.friendliness = 0
        self.color = GREEN  # Заменить постоянный цвет на зависимый
        self.border_color = WHITE
        self.border_thickness = 1

    def update(self):
        '''Function updates position of cell, it's color, '''

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]  # Решить проблему с убеганием за пределы экрана
        if self.position[0] >= SCREEN_WIDTH or self.position[0] <= 0:
            self.velocity[0] *= -1
        if self.position[1] >= SCREEN_HEIGHT or self.position[1] <= 0:
            self.velocity[1] *= -1

    def food_search(self, list_meal):
        ''' Function calculates the main food direction for cell

        '''

        vec_area = find_area(self, list_meal)
        self.velocity[0] = vec_area[0]
        self.velocity[1] = vec_area[1]

    def multiply(self, list_cells):
        """:arg     list_cells - list of cells"""
        global spawn  # variable to spawn
        spawn = True
        new_cell = Cell()
        phi = random.uniform(0, 2 * np.pi)  # random phi
        x = self.position[0] + 2 * self.size * np.cos(phi)  # x cor of center new cell
        y = self.position[1] + 2 * self.size * np.sin(phi)  # y cor of center new cell

        for cell in list_cells:  # do not spawn near to each other
            vec = [cell.position[0] - x, cell.position[1] - y]
            module_vec = vec_module(vec)
            if module_vec <= 2 * self.size:
                spawn = False
                break
        if spawn:
            new_cell.position = [int(x), int(y)]

            return new_cell
        else:
            return 0


class Meal:
    def __init__(self):
        self.position = [random.uniform(0, 1) * SCREEN_WIDTH, random.uniform(0, 1) * SCREEN_HEIGHT]
        self.size = 3
        self.richness = random.uniform(0, 1)

    def eaten(self, cell):
        return vec_module(find_vector(self, cell)) <= self.size + cell.size



