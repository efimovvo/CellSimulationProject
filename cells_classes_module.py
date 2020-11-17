import random
WIDTH = 600
HEIGHT = 600


class FirstCell():
    """First type of cell.
    attributes:     multiply - float from 0 to 1. 0 - the most possible to multiply, 1 - dont multiply at all
                    center - type : tuple, center of cell
                    r - type : int, radius of cell
                    time_multiply - integer(or float) - time when cell multiplies
                    multiply_freq - type : float, frequency of multiply
                    vx, xy - type : float, velocity of cell"""
    def __init__(self):
        self.multiply = 0.6
        self.center = [WIDTH//2, HEIGHT//2]
        self.r = 10
        self.time_multiply = 1
        self.multiply_freq = 0.1
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def update(self):
        """Function updates position cell"""
        self.center[0] += self.vx
        self.center[1] += self.vy
        if self.center[0] >= WIDTH or self.center[0] <= 0:
            self.vx = 0
        if self.center[1] >= HEIGHT or self.center[1] <= 0:
            self.vy = 0

