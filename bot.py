from ball import Ball

from matka import Matka

DOWN = 0
STAND = 1
UP = 2


class Bot:
    def decide(self, ball: Ball, bat: Matka) -> int:
        if bat.y < ball.y:
            return UP
        elif bat.y > ball.y:
            return DOWN

        return STAND
