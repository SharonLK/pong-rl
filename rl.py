import numpy as np
import gym

from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticPolicy


def something():
    env = gym.make("CartPole-v1")

    pong_policy = ActorCriticPolicy(observation_space=env.observation_space,
                                    action_space=env.action_space,
                                    lr_schedule=lambda x: 0.01)

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