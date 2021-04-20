import math

import numpy as np
import gym

from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticPolicy

from environment import Environment


def step_decay(epoch):
   initial_lrate = 0.1
   drop = 0.5
   epochs_drop = 10.0
   lrate = initial_lrate * math.pow(drop, math.floor((1+epoch)/epochs_drop))
   return lrate


def something():
    game = Game(width=800, height=600, matka_length=100, speed=0.01, step_size=0.005)
    env = Environment(game)
    pong_policy = ActorCriticPolicy(observation_space=env.observation_space,
                                    action_space=env.action_space,
                                    lr_schedule=step_decay)
    model = PPO(pong_policy, env, verbose=1)

    model.learn(total_timesteps=10000)

    obs = env.reset()
    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()

    env.close()