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

    def __init__(self, game: Game) -> None:
        super(Environment, self).__init__()

        self.game = game

        self.action_space = spaces.Discrete(3)
        # left_matka center location, right_matka center location, ball loc, ball speed
        self.observation_space = spaces.Tuple((
            spaces.Box(low=game.left_matka.length / 2, high=game.board.height - game.left_matka.length / 2, shape=1),
            spaces.Box(low=game.right_matka.length / 2, high=game.board.height - game.right_matka.length / 2, shape=1),
            spaces.Box(low=np.array([0, 0]), high=np.array([game.board.width, game.board.height])),
            spaces.Box(low=0, high=game.ball.speed, shape=2),
        ))

    def _pull_observation(self):
        return np.array([self.game.left_matka.y, self.game.right_matka.y,
                         (self.game.ball.x, self.game.ball.y), self.game.ball.speed])

    def reset(self) -> np.ndarray:
        self.game.reset()
        return self._pull_observation()

    def step(self, action):
        self.game.advance(action)

        if self.game.game_over():
            if self.game.ball.x < self.game.width / 2:
                return self._pull_observation(), -1, 1, {}
            return self._pull_observation(), 1, 1, {}

        # Only if the ball is advancing on the enemy can we rest on our laurels
        reward = 0
        if self.game.ball.speed[0] > 0:
            reward += 1e-2
        # Reward for following the ball, always be ready
        if self.game.left_matka.y - self.game.left_matka.length / 2 < self.game.ball.y < \
            self.game.left_matka.y + self.game.left_matka.length / 2:
            reward += 1e-2

        return self._pull_observation(), reward, 0, {}
