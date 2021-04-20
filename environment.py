import gym
from gym import spaces
import numpy as np

from ball import Ball
from game_board import GameBoard
from matka import Matka

DOWN = 0
STAND = 1
UP = 2


class Environment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, board: GameBoard, ball: Ball, left_matka: Matka, right_matka: Matka) -> None:
        super(Environment, self).__init__()

        self.board = board
        self.ball = ball
        self.left_matka = left_matka
        self.right_matka = right_matka

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Tuple((
            spaces.Box(low=left_matka.length / 2, high=board.width - left_matka.length / 2, shape=1),
            spaces.Box(low=right_matka.length / 2, high=board.width - right_matka.length / 2, shape=1),
            spaces.Box(low=0, high=board.length, shape=1),
            spaces.Box(low=0, high=board.width, shape=1),
            spaces.Box(low=0, high=ball.speed, shape=2),
        ))


    def reset(self) -> np.ndarray:
        return np.array([self.left_matka.y, self.right_matka.y, self.ball.x, self.ball.y, self.ball.speed])

    def step(self, action):
        if action == UP:
            self.

