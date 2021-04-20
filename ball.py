import numpy as np

class Ball:

    def __init__(self, x: float, y: float, speed: np.ndarray):

        self.x = x
        self.y = y
        self.speed = speed