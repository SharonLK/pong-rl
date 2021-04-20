import random
from typing import Optional

import numpy as np

from ball import Ball
from matka import Matka

DOWN = 0
STAND = 1
UP = 2


class Game:
    def __init__(self, width: int, height: int, matka_length: float, speed: float, step_size: float):
        self.ball: Optional[Ball] = None
        self.left_matka: Optional[Matka] = None
        self.right_matka: Optional[Matka] = None

        self.width = width
        self.height = height
        self.matka_length = matka_length
        self.matka_step_size = step_size
        self.speed = speed

        self.reset()

        self.ended = False

    def reset(self) -> None:
        ball_x = self.width / 2
        ball_y = self.height / 2
        speed_direction = np.random.random() * 2 * np.pi
        speed = self.speed * np.array([random.random() * 0.5 + 0.5, random.random() * 0.5 + 0.5])
        if random.random() <= 0.5:
            speed[0] = -speed[0]
        if random.random() <= 0.5:
            speed[1] = -speed[1]

        left = Matka(0, self.height / 2, self.matka_length, self.matka_step_size)
        right = Matka(self.width, self.height / 2, self.matka_length, self.matka_step_size)

        self.ball = Ball(ball_x, ball_y, speed)
        self.left_matka = left
        self.right_matka = right
        self.ended = False

    def _move_matka(self, matka: Matka, action: int) -> None:
        if action == UP:
            matka.set_location(matka.y - matka.step_size)
            if matka.y < matka.length // 2:
                matka.set_location(matka.length // 2)
        elif action == DOWN:
            matka.set_location(matka.y + matka.step_size)
            if matka.y + matka.length // 2 > self.height:
                matka.set_location(self.height - matka.length // 2)

    def advance(self, left_action: int, right_action: int) -> None:
        self._move_matka(self.left_matka, left_action)
        self._move_matka(self.right_matka, right_action)

        self.ball.set_location(self.ball.location + self.ball.speed)

        if self.ball.location[1] >= self.height:
            self.ball.location[1] = 2 * self.height - self.ball.location[1]
            self.ball.speed[1] = -abs(self.ball.speed[1])

        if self.ball.location[1] <= 0:
            self.ball.location[1] = -self.ball.location[1]
            self.ball.speed[1] = abs(self.ball.speed[1])

        if self.ball.location[0] <= 0:
            lower_matka = self.left_matka.y - self.left_matka.length // 2
            upper_matka = self.left_matka.y + self.left_matka.length // 2
            if lower_matka <= self.ball.location[1] <= upper_matka:
                self.ball.location[0] = abs(self.ball.location[0])
                self.ball.speed[0] = abs(self.ball.speed[0])
            else:
                self.ended = True

        if self.ball.location[0] >= self.width:
            lower_matka = self.right_matka.y - self.right_matka.length // 2
            upper_matka = self.right_matka.y + self.right_matka.length // 2
            if lower_matka <= self.ball.location[1] <= upper_matka:
                self.ball.location[0] = self.width - abs(self.ball.location[0])
                self.ball.speed[0] = -abs(self.ball.speed[0])
            else:
                self.ended = True

    def has_ended(self) -> bool:
        return self.ended
