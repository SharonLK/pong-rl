import gym
import numpy as np
from gym import spaces

from bot import Bot
from game import Game

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
        # low = np.array(
        #     [game.left_matka.length / 2, game.right_matka.length / 2,
        #      0, 0,
        #      -game.speed, -game.speed])
        # high = np.array(
        #     [game.height - game.left_matka.length / 2, game.height - game.right_matka.length / 2,
        #      game.width, game.height,
        #      game.speed, game.speed])

        low = np.array([-1, -1])
        high = np.array([1, 1])

        self.observation_space = spaces.Box(low=low, high=high, shape=(2,))

        self.bot = Bot()
        self.iterations = 0

    def _pull_observation(self):
        # return np.array([self.game.left_matka.y, self.game.right_matka.y,
        #                  self.game.ball.x, self.game.ball.y, self.game.ball.speed[0], self.game.ball.speed[1]])

        return np.array([(self.game.left_matka.y - self.game.ball.y) / self.game.height,
                         np.sign(self.game.ball.speed[1])])

    def reset(self) -> np.ndarray:
        self.game.reset()
        self.iterations = 0
        return self._pull_observation()

    def step(self, action: int):
        self.iterations += 1

        bot_action = self.bot.decide(self.game.ball, self.game.right_matka)
        self.game.advance(action, bot_action)

        if self.game.has_ended():
            if self.game.ball.x < self.game.width / 2:
                return self._pull_observation(), -0, 1, {}
            return self._pull_observation(), 0, 1, {}

        # if self.iterations > 200:
        #     return self._pull_observation(), 0, 1, {}

        # Only if the ball is advancing on the enemy can we rest on our laurels
        # reward = 0
        # if self.game.ball.speed[0] > 0:
        #     reward += 1e-2

        reward = 0

        if action != 1:
            reward = -0.1

        # Reward for following the ball, always be ready
        # if self.game.left_matka.y - self.game.left_matka.length / 2 < self.game.ball.y < \
        #         self.game.left_matka.y + self.game.left_matka.length / 2:
        #     reward += 1

        distance = abs(self.game.left_matka.y - self.game.ball.y) / (self.game.left_matka.length // 2)
        if distance <= 0.5:
            reward += 1
        elif distance <= 0.8:
            reward += 1 - distance

        return self._pull_observation(), reward, 0, {}
