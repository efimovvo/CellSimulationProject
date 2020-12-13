import random
import numpy as np
from vis_module import *


def vec_module(vector):
    """:arg :   vector - type : numpy array

    Function returns the modulus of the vector

    """
    return (vector[0] ** 2 + vector[1] ** 2) ** 0.5


def find_vector(object_1, object_2):
    """:arg :   object_1, object_2 - the objects between which a vector will be calculated,
                type : Cell or Meal

    Function returns the vector between objects, type : numpy array

    """
    return - object_1.position + object_2.position


def find_area(cell, list_meal):
    """Function returns the vector aimed to the area with the most food
    :arg
        cell - on cell, type : cell
        list_meal - list of meal, type : list

    """
    vec_area = np.array([0.0, 0.0])
    # Calculating a vec_area direction
    for meal in list_meal:
        vector_to_meal = find_vector(cell, meal)
        vec_area[0] += (vector_to_meal[0] / vec_module(vector_to_meal) ** 3)
        vec_area[1] += (vector_to_meal[1] / vec_module(vector_to_meal) ** 3)

    # Normalization of the vec_area
    if vec_module(vec_area) > 0:
        vec_area = vec_area / vec_module(vec_area)
        vec_area *= cell.engines

    return vec_area


def find_force(vector):
    """:arg :   vector - type : numpy array
    Function returns the value of a force (type : numpy array) that applied to the cell

    """

    if vec_module(vector) == 0:
        force = np.array([0, 0])
    else:
        # The value of the force :
        force = vector / (vec_module(vector) / 5) ** 10

    if vec_module(force) > 10:
        force *= 10 / vec_module(force)

    return force


class Cell:
    """The common class for all cells
    Parameters:
            multiply_skill : float : A skill to multiply
            age : float : An age of a cell
            size  : int : A size of the cell
            position  : numpy array : Cords of a center of the cell
            velocity : numpy array : Velocity of the cell
            satiety : float : Satiety of a cell
            satiety_step  : float : It is taken from satiety every moment of time; how fast satiety gets lower
            engines : float: A limit of the velocity the cell
            reproductive_age  : list :  Limit of the cell's age where the cell can multiply
            age_step  : float : It is added to the age every moment of time; how fast a cell gets older
            age_of_last_multiplication  : float or int : The last time when the cell multiplied
            reproductive_waiting  : float : How long the cell need to wait before multiply
            color : list : A color of the cell
            border_color  : list : A color of the borderline of the cell
            border_thickness  : int : A variable that responsible for a thickness of the border; when cell gets
            older borderline gets thicker
            predator  : Bool : The type of the cell. If True - the cell is a predator, else - the cell is peaceful
            richness  : float : How much satiety a predator cell will get from eating a cell
            view_radius : float or int : How much a peaceful cell can see to find a predator
    Methods:
        init : Initializes class
        update : Updates the cells' states
        calc_forces : Calculates the forces that applied to the cells
        multiply : Creating new cells

    """

    def __init__(self, age_step, multiply_skill, satiety_step):
        # Common property
        self.multiply_skill = multiply_skill
        self.age = 0
        self.size = 5
        self.position = np.array([SCREEN_WIDTH / 2 * random.uniform(0, 1),
                                  SCREEN_HEIGHT / 2 * random.uniform(0, 1)])
        self.velocity = np.array([1.0, 1.0])
        # Genetic code
        self.satiety = 1.0  # сытость
        self.satiety_step = satiety_step
        self.engines = 3 + (3 * random.random() - 1.5) ** 3
        self.reproductive_age = [5, 80]
        self.age_step = age_step
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

        # Updates position :
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Cell can not run outside the screen :
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

        Function calculates forces.
                For peaceful cell it depends on how close the meal, how close predator to the cell, viscosity
                 For predator cell it depends on how close the victims (peaceful cells), viscosity"""

        ''' For the predator cell. This block searches victims first of all in 100 radius, if there are nothing in
         300 radius and 600 radius. It helps avoid a lot of calculations'''

        list_victim = [cell for cell in list_cells
                       if not cell.predator and vec_module(find_vector(self, cell)) <= 100]

        if len(list_victim) == 0:
            list_victim = [cell for cell in list_cells
                           if not cell.predator and vec_module(find_vector(self, cell)) <= 300]
        if len(list_victim) == 0:
            list_victim = [cell for cell in list_cells
                           if not cell.predator and vec_module(find_vector(self, cell)) <= 600]

        ''' For the peaceful cell. This block searches meal first of all in 100 radius, if there are nothing in
                 300 radius and 600 radius. It helps avoid a lot of calculations'''
        closest_meal = [meal for meal in list_meal
                        if vec_module(find_vector(self, meal)) <= 100]
        if len(closest_meal) == 0:
            closest_meal = [meal for meal in list_meal
                            if vec_module(find_vector(self, meal)) <= 300]
        if len(closest_meal) == 0:
            closest_meal = [meal for meal in list_meal
                            if vec_module(find_vector(self, meal)) <= 600]

        # For the peaceful cell. It searches the nearest enemies
        list_predator = [cell for cell in list_cells if cell.predator
                         and vec_module(find_vector(self, cell)) <= self.view_radius]

        # Calculating the force of entire engine
        # Gets direction of the vector to a meal
        if not self.predator:
            vec_area = find_area(self, closest_meal)
        elif len(list_victim) != 0:
            vec_area = find_area(self, list_victim)
        else:
            vec_area = find_area(self, closest_meal)
        acceleration_to_meal = vec_area

        # Calculating the force of a viscosity
        viscosity = 0.5
        acceleration = - viscosity * np.array(self.velocity)

        # Calculating the repulsive force between two cells if they in the same class
        for cell in list_cells:
            if self != cell and self.predator == cell.predator:
                vector_to_cell = find_vector(self, cell)
                if vec_module(vector_to_cell) <= self.size:
                    acceleration -= find_force(np.array(vector_to_cell))

        # Calculating the force of a victim from a predator chasing after him
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

    def multiply(self, list_cells, parameters):
        """:arg:     list_cells - list of cells

        Function returns new_cell if it could spawn or 0 if it could not."""

        global spawn
        spawn = True
        new_cell = Cell(parameters[2].value, parameters[3].value, parameters[4].value)  # Creates a new cell

        # The predator multiplies with another predator:
        if self.predator:
            new_cell.predator = True
            new_cell.color = RED
            new_cell.engines = 3 + (2 * random.random() - 1) ** 3
            new_cell.satiety_step = 0.005
            new_cell.reproductive_age = [5, 50]
            new_cell.reproductive_waiting = 3

        phi = random.uniform(0, 2 * np.pi)  # Random phi
        x = self.position[0] + 2 * self.size * np.cos(phi)  # x cor of center new cell
        y = self.position[1] + 2 * self.size * np.sin(phi)  # y cor of center new cell

        for cell in list_cells:  # Do not spawn near each other
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
    """The common class for meal
    Parameters:
            position : numpy array : The position of the meal on the screen
            size : int : The size of the meal
            richness : float (from 0 to 1) : How much a peaceful cell gets satiety after eating a meal
    Methods:
        init : Initializes class
        eaten : Shows was a meal eaten or not

    """

    def __init__(self):
        self.position = np.array([random.uniform(0, 1) * SCREEN_WIDTH,
                                  random.uniform(0, 1) * SCREEN_HEIGHT])
        self.size = 3
        self.richness = random.uniform(0, 1)

    def eaten(self, cell):
        """:arg :   cell - type : Cell. The cell that can eat the meal

        Function returns True or False, depending on how much the cell is close to the meal.

        """
        return vec_module(find_vector(self, cell)) <= self.size + cell.size
