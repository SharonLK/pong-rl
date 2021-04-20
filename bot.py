from ball import Ball
from environment import DOWN, STAND, UP
from matka import Matka


class Bot:
    def decide(self, ball: Ball, bat: Matka) -> int:
        if bat.y < ball.y:
            return UP
        elif bat.y > ball.y:
            return DOWN

        return STAND
