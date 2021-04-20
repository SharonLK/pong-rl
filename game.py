from typing import Tuple
import numpy as np

from ball import Ball
from board import Board
from environment import UP, DOWN
from matka import Matka


class Game:

    def __init__(self, board: Board, length: float, speed: float,, step_size: float, bot: Bot):

        self.board = board
        self.matka_length = length
        self.matka_step_size = step_size
        self.ball_speed = speed
        self.ball, self.right_matka, self.left_matka = None, None, None
        self.reset()
        self.bot = bot

        self.ended = False

    def reset(self) -> Tuple[Ball, Matka, Matka]:
        ball_x = np.random.random() * self.board.length
        ball_y = np.random.random() * self.board.width
        ball_speed_direction = np.random.random() * 2 * np.pi
        ball_speed = self.ball_speed * np.array(np.cos(ball_speed_direction), np.sin(ball_speed_direction))
        ball = Ball(ball_x, ball_y, ball_speed)
        left = Matka(0, np.random.random() * self.board.width, self.matka_length, self.matka_step_size)
        right = Matka(self.board.length, np.random.random() * self.board.width, self.matka_length, self.matka_step_size)
        return ball_x, right, left

    def _move_matka(self, matka: Matka, action: int) -> None:

        if action == UP:
            matka.set_location(matka.y + matka.step_size)
            if matka.y + matka.length // 2 > self.board.width:
                matka.set_location(self.board.width - matka.length // 2)

        if action == DOWN:
            matka.set_location(matka.y - matka.step_size)
            if matka.y < matka.length // 2:
                matka.set_location(matka.length // 2)

    def advance(self, rl_action: int) -> None:
        self._move_matka(self.left_matka, rl_action)
        self._move_matka(self.right_matka, self.bot.decide(self.ball, self.right_matka))

        # move the ball
        location = self.ball.location + self.ball.ball_speed

        if location[1] > self.board.width:
            access = location[1] - self.board.width
            location[1] = self.board.width - access

        if location[1] < 0:
            location[1] = -location[1]

        if location[0] < 0:
            y_of_hit = None # Compute
            if self.left_matka.y - self.left_matka.length // 2 <= y_of_hit <= self.left_matka.y - self.left_matka.length // 2:
                location[0] = -location[0]

            else:
                self.ended = True

        if location[1] > self.board.length:
            a = 1 # Do the same

    def has_ended(self) -> bool:
        return self.ended
