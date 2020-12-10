import random
import numpy as np
from vis_module import *


def vec_module(vector):
    """:arg :   vector - type : numpy array

    Function returns module of vector"""
    return (vector[0]**2 + vector[1]**2)**0.5


def find_vector(object_1, object_2):
    """:arg :   object_1, object_2 - the objects between which vector will be calculated,
                type : Cell or Meal

    Function returns vector between objects, type : numpy array"""
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
    """:arg :   vector - type : numpy array
    Function returns force (type : numpy array) that moves cell"""

    if vec_module(vector) == 0:
        force = np.array([0, 0])
    else:
        # value of force :
        force = vector / (vec_module(vector) / 5)**10

    if vec_module(force) > 10:
        force *= 10 / vec_module(force)

    return force


class Cell:
    """Common class for all cells
    attributes:
            multiply_skill - skill to multiply, type : float, value is from 0 (the best) to 1 ( the worst)

            age - type : float, age of cell

            size - type : int, size of cell

            position - type : numpy array, cords of center the cell

            velocity - type : numpy array, velocity of the cell

            satiety - type : float, satiety of the cell

            satiety_step - type : float, it is taken from satiety every moment of time,
                                    responsible how fast satiety gets loser

            engines - type : float, responsible for limit of velocity the cell

            reproductive_age - type : list, it is limits when cell could multiply

            age_step - type : float, it is added to the age every moment of time,
                                responsible how fast cell gets older

            age_of_last_multiplication - type : float or int, it responsible for age when the cell
                                            multiply the last time

            reproductive_waiting - type : float, it responsible how long the cell have to wait before multiply

            color - type : list, color of cell

            border_color - type : list, color of border the cell

            border_thickness - type : int, variable responsible for thickness of border,
                                        when cell is gets older border is gets more and more white

            predator - type : Bool, it responsible for type of the cell : if True cell is predator, else :
                                        peaceful cell

            richness - type : float, responsible how much predator cell will get from cell when the last one will
                                                                                                        be eaten

            view_radius - type : float or int, how much peaceful cell can see to find predator

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
        self.satiety = 1.0  # сытость
        self.satiety_step = satiety_step()
        self.engines = 3 + (3 * random.random() - 1.5)**3
        self.reproductive_age = [5, 80]
        self.age_step = 0.03
        self.age_of_last_multiplication = 0
        self.reproductive_waiting = 0.5
        self.color = GREEN
        self.border_color = WHITE
        self.border_thickness = 1
        self.predator = False
        self.richness = 0.5
        self.view_radius = 200

    def update(self):
        """ Function updates position of cell, cell can not run outside the screen """

        # updates position :
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # cell can not run outside the screen :
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
        """:arg :   list_meal - type : list, each element is Meal type
                    list_cells - type : list, each element is Cell type

        Function calculates forces where cell will be move.
                For peaceful cell it depends on how close the meal, how close predator to the cell and viscosity
                 For predator cell it depends on how closw the victims (peaceful cells), viscosity"""

        ''' for the predator cell. This block searches victims first of all in 100 radius, if there are nothing in
         300 radius and 600 radius. It helps avoid a lot of calculations'''

        list_victim = [cell for cell in list_cells
                       if not cell.predator and vec_module(find_vector(self, cell)) <= 100]

        if len(list_victim) == 0:
            list_victim = [cell for cell in list_cells
                           if not cell.predator and vec_module(find_vector(self, cell)) <= 300]
        if len(list_victim) == 0:
            list_victim = [cell for cell in list_cells
                           if not cell.predator and vec_module(find_vector(self, cell)) <= 600]

        ''' for the peaceful cell. This block searches meal first of all in 100 radius, if there are nothing in
                 300 radius and 600 radius. It helps avoid a lot of calculations'''
        closest_meal = [meal for meal in list_meal
                        if vec_module(find_vector(self, meal)) <= 100]
        if len(closest_meal) == 0:
            closest_meal = [meal for meal in list_meal
                            if vec_module(find_vector(self, meal)) <= 300]
        if len(closest_meal) == 0:
            closest_meal = [meal for meal in list_meal
                            if vec_module(find_vector(self, meal)) <= 600]

        # for peaceful cell. It searches the nearest enemies
        list_predator = [cell for cell in list_cells if cell.predator
                         and vec_module(find_vector(self, cell)) <= self.view_radius]

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
        """:arg     list_cells - list of cells

        Function returns new_cell if it could spawn or 0 if not."""

        global spawn  # variable to spawn
        spawn = True
        new_cell = Cell()  # creates new cell

        # predator multiply with predator :
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
    """Common class for all meal
    attributes :
            position - type : numpy array, position of the meal on the screen

            size - type : int, size of the meal

            richness - type : float (from 0 to 1), responsible how much peaceful cell will gets satiety when meal
                                                                            will be eaten"""

    def __init__(self):
        self.position = np.array([random.uniform(0, 1) * SCREEN_WIDTH,
                                  random.uniform(0, 1) * SCREEN_HEIGHT])
        self.size = 3
        self.richness = random.uniform(0, 1)

    def eaten(self, cell):
        """:arg :   cell - type : Cell, cell that can eat the meal

        Function returns True or False, in case cell is close the meal. """
        return vec_module(find_vector(self, cell)) <= self.size + cell.size
