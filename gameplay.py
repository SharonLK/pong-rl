from typing import NamedTuple

import gym
import pygame
from stable_baselines3 import A2C


class Ball(NamedTuple):
    x: float
    y: float


WIDTH = 800
HEIGHT = 600

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    env = gym.make('CartPole-v1')

    model = A2C('MlpPolicy', env, verbose=1)

    env.reset()

    ball = Ball(0, 0)
    left_bat = 0
    right_bat = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            right_bat += 0.1
        if keys[pygame.K_UP]:
            right_bat -= 0.1

        screen.fill((25, 25, 25))

        # ball = env.get_ball()
        ball = Ball(ball.x + 0.01, ball.y + 0.0025)
        pygame.draw.circle(screen, (200, 200, 200), (ball.x, ball.y), 13)
        pygame.draw.circle(screen, (51, 133, 161), (ball.x, ball.y), 11)

        left_bat += 0.1
        pygame.draw.line(screen, (180, 180, 180), (5, left_bat - 50), (5, left_bat + 50), 7)

        pygame.draw.line(screen, (180, 180, 180), (WIDTH - 5, right_bat - 50), (WIDTH - 5, right_bat + 50), 7)

        pygame.display.flip()

    pygame.quit()
