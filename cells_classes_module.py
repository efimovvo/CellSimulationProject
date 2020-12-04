import random
import numpy as np
from vis_module import *


def vec_module(vector):
    return (vector[0]**2 + vector[1]**2)**0.5


def find_vector(object_1, object_2):
    return - object_1.position + object_2.position


def find_area(cell, list_meal):
    """Function returns vector in area where a lot of food
    :arg
        cell - on cell, type : cell
        list_meal - list of meal, type : list
    """
    vec_area = np.array([0.0, 0.0])
    # Calculating vec_area direction
    for meal in list_meal:
        vector_to_meal = find_vector(cell, meal)
        vec_area[0] += (vector_to_meal[0] / vec_module(vector_to_meal)**3)
        vec_area[1] += (vector_to_meal[1] / vec_module(vector_to_meal)**3)

    # Normalization of vec_area
    if vec_module(vec_area) > 0:
        vec_area = vec_area / vec_module(vec_area)
        vec_area *= cell.engines

    return vec_area


def find_force(vector):
    if vec_module(vector) == 0:
        force = np.array([0, 0])
    else:
        force = vector / (vec_module(vector) / 5)**10
    if vec_module(force) > 10:
        force *= 10 / vec_module(force)
    return force


class Cell:
    """Common class for all cells
    attributes:
            multiply_skill - skill to multiply, float from 0 (the best) to 1 ( the worst)
            age - float, age of cell
            size - int, size of cell
            position - cords of center, list
            velocity - velocity of cell [vx, vy], list
            engines - describe how much cells will be move
            color - Tuple, color of cell
    """
    def __init__(self):
        # Common property
        self.multiply_skill = 0.8
        self.age = 0
        self.size = 5
        self.position = np.array([SCREEN_WIDTH / 2 * random.uniform(0, 1),
                                  SCREEN_HEIGHT / 2 * random.uniform(0, 1)])
        self.velocity = np.array([1.0, 1.0])
        # Genetic code
        self.shell_thickness = 0.5
        self.satiety = 1  # сытость
        self.satiety_step = 0.003
        self.engines = 3 + (3 * random.random() - 1.5)**3
        self.reproductive_age = [5, 80]
        self.age_step = 0.03
        self.age_of_last_multiplication = 0
        self.reproductive_waiting = 0.5
        self.aggressiveness = 0
        self.friendliness = 0
        self.color = GREEN  # Заменить постоянный цвет на зависимый
        self.border_color = WHITE
        self.border_thickness = 1
        self.predator = False
        self.richness = 0.5

    def update(self):
        ''' Function updates position of cell, it's color '''
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        if self.position[0] >= SCREEN_WIDTH:
            self.position[0] = SCREEN_WIDTH - (self.position[0] - SCREEN_WIDTH)
            self.velocity[0] *= -1
        elif self.position[0] <= 0:
            self.position[0] = abs(self.position[0])
            self.velocity[0] *= -1

        if self.position[1] >= SCREEN_HEIGHT:
            self.position[1] = SCREEN_HEIGHT - (self.position[1] - SCREEN_HEIGHT)
            self.velocity[1] *= -1
        elif self.position[1] <= 0:
            self.position[1] = abs(self.position[1])
            self.velocity[1] *= -1

    def calc_forces(self, list_meal, list_cells):
        list_victim = [cell for cell in list_cells
                       if not cell.predator and vec_module(find_vector(self, cell)) <= 100]
        if len(list_victim) == 0:
            list_victim = [cell for cell in list_cells
                           if not cell.predator and vec_module(find_vector(self, cell)) <= 300]
        if len(list_victim) == 0:
            list_victim = [cell for cell in list_cells
                           if not cell.predator and vec_module(find_vector(self, cell)) <= 600]

        closest_meal = [meal for meal in list_meal
                        if vec_module(find_vector(self, meal)) <= 100]
        if len(closest_meal) == 0:
            closest_meal = [meal for meal in list_meal
                            if vec_module(find_vector(self, meal)) <= 300]
        if len(closest_meal) == 0:
            closest_meal = [meal for meal in list_meal
                            if vec_module(find_vector(self, meal)) <= 600]

        list_predator = [cell for cell in list_cells if cell.predator
                         and vec_module(find_vector(self, cell)) <= 200]

        # Calculating force of entire engine
        # Get direction vector to meal
        if not self.predator:
            vec_area = find_area(self, closest_meal)
        elif len(list_victim) != 0:
            vec_area = find_area(self, list_victim)
        else:
            vec_area = find_area(self, closest_meal)
        acceleration_to_meal = vec_area

        # Calculating force of viscosity
        viscosity = 0.5
        acceleration = - viscosity * np.array(self.velocity)

        # Calculating force of cell to cell interaction
        for cell in list_cells:
            if self != cell and self.predator == cell.predator:
                vector_to_cell = find_vector(self, cell)
                if vec_module(vector_to_cell) <= self.size:
                    acceleration -= find_force(np.array(vector_to_cell))

        # Calculating force of victim from predator running
        list_of_danger = []
        if not self.predator:
            list_of_danger = [cell for cell in list_predator if vec_module(find_vector(cell, self)) < 40]

            vec_area = - find_area(self, list_of_danger)
        acceleration_from_predator = vec_area

        if len(list_of_danger) > 0:
            acceleration += acceleration_from_predator
        else:
            acceleration += acceleration_to_meal

        self.velocity += acceleration

    def multiply(self, list_cells):
        """:arg     list_cells - list of cells"""
        global spawn  # variable to spawn
        spawn = True
        new_cell = Cell()
        if self.predator:
            new_cell.predator = True
            new_cell.color = RED
            new_cell.engines = 3 + (2 * random.random() - 1)**3
            new_cell.satiety_step = 0.005
            new_cell.reproductive_age = [5, 50]
            new_cell.reproductive_waiting = 3
        phi = random.uniform(0, 2 * np.pi)  # random phi
        x = self.position[0] + 2 * self.size * np.cos(phi)  # x cor of center new cell
        y = self.position[1] + 2 * self.size * np.sin(phi)  # y cor of center new cell

        for cell in list_cells:  # do not spawn near to each other
            vector = cell.position - np.array([x, y])
            module_vec = vec_module(vector)
            if module_vec <= 2 * self.size:
                spawn = False
                break
        if spawn:
            new_cell.position = np.array([x, y])
            self.satiety, new_cell.satiety = self.satiety / 2, self.satiety / 2
            return new_cell
        else:
            return 0


class Meal:
    def __init__(self):
        self.position = np.array([random.uniform(0, 1) * SCREEN_WIDTH,
                                  random.uniform(0, 1) * SCREEN_HEIGHT])
        self.size = 3
        self.richness = random.uniform(0, 1)

    def eaten(self, cell):
        return vec_module(find_vector(self, cell)) <= self.size + cell.size