import numpy as np

class Ball:

    def __init__(self, x: float, y: float, speed: np.ndarray):

        self.x = x
        self.y = y
        self.speed = speed

    @property
    def location(self) -> np.ndarray:
        return np.array([self.x, self.y])

    def set_location(self, location: np.ndarray):
        self.x = location[0]
        self.y = location[1]