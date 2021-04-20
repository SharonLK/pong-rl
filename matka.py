import numpy as np

from environment import UP


class Matka:

    def __init__(self, x: float, y: float, length: float, step_size: float):

        self.x = x
        self.y = y
        self.length = length
        self.step_size = step_size

    def set_location(self, y: float) -> None:
        self.y = y