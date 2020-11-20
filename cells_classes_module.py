import random

WIDTH = 600
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class FirstCell:
    """First type of cell.
    attributes:     multiply - float from 0 to 1. 0 - the most possible to multiply, 1 - dont multiply at all
                    center - type : list, center of cell
                    r - type : int, radius of cell
                    time_multiply - integer(or float) - time when cell multiplies
                    multiply_freq - type : float, frequency of multiply
                    vx, xy - type : float, velocity of cell
                    color - type : tuple, color of cell
                    predator - type : bool, shows if it is predator cell"""

    def __init__(self):
        self.multiply = 0
        self.center = [WIDTH // 2, HEIGHT // 2]
        self.r = 10
        self.time_multiply = 0.5
        self.multiply_freq = 0.5
        self.vx = 0
        self.vy = 0
        self.color = GREEN
        self.predator = False

    def update(self):
        """Function updates position cell"""
        self.center[0] += self.vx
        self.center[1] += self.vy
        if self.center[0] >= WIDTH or self.center[0] <= 0:
            self.vx = 0
        if self.center[1] >= HEIGHT or self.center[1] <= 0:
            self.vy = 0


class Predator:
    """Class of predaors cell
        Attributes : multiply - float from 0 to 1. 0 - the most possible to multiply, 1 - dont multiply at all
                    center - type : list, center of cell
                    r - type : int, radius of cell
                    time_multiply - integer(or float) - time when cell multiplies
                    multiply_freq - type : float, frequency of multiply
                    vx, xy - type : float, velocity of cell
                    color - type : tuple, color of cell
                    predator - type : bool, shows if it is predator cell
                    time_attack - type : float or int, milliseconds, when predator cell will attack another cells
                    time_freq - type : float or int, milliseconds, frequency of attack"""

    def __init__(self):
        self.multiply = 0.5
        self.center = [WIDTH // 2, HEIGHT//4]
        self.r = 10
        self.time_multiply = 1
        self.multiply_freq = 0.5
        self.vx = 0
        self.vy = 0
        self.color = RED
        self.predator = True
        self.time_attack = 1
        self.freq_attack = 1.5

    def update(self):
        """Function updates position cell"""
        self.center[0] += self.vx
        self.center[1] += self.vy
        if self.center[0] >= WIDTH or self.center[0] <= 0:
            self.vx = 0
        if self.center[1] >= HEIGHT or self.center[1] <= 0:
            self.vy = 0
