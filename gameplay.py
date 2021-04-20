import random

import gym
import numpy as np
import pygame
from stable_baselines3 import A2C

from ball import Ball
from bot import Bot
from environment import DOWN, UP
from matka import Matka

WIDTH = 800
HEIGHT = 600

BAT_DISTANCE_FROM_SCREEN = 11

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    env = gym.make('CartPole-v1')

    model = A2C('MlpPolicy', env, verbose=1)

    env.reset()

    ball = Ball(50, 0, np.array([0.01, 0.01]))
    left_bat = HEIGHT / 2
    right_bat = HEIGHT / 2

    rain = [[random.random() * WIDTH * 1.1 * 100, random.random() * 10] for _ in range(10)]

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
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, HEIGHT), 5)

        ball.x += 0.001
        ball.y += 0.0025
        pygame.draw.circle(screen, (200, 200, 200), (ball.x, ball.y), 13)
        pygame.draw.circle(screen, (51, 133, 161), (ball.x, ball.y), 11)

        decision = Bot().decide(ball, Matka(0, left_bat, 3, 3))

        if decision == UP:
            left_bat += 0.01
        elif decision == DOWN:
            left_bat -= 0.01

        if random.random() < 0.05:
            rain.append([random.random() * WIDTH * 1.1 - 100, random.random() * 10])

        for droplet in rain:
            droplet[0] += 0.025
            droplet[1] += 0.1

            pygame.draw.line(screen, (200, 200, 200),
                             (droplet[0], droplet[1]),
                             (droplet[0] + 5, droplet[1] + 20), 1)

        for i in range(len(rain) - 1, -1, -1):
            if rain[i][1] > HEIGHT:
                del rain[i]

        pygame.draw.line(screen, (180, 180, 180),
                         (BAT_DISTANCE_FROM_SCREEN, left_bat - 50),
                         (BAT_DISTANCE_FROM_SCREEN, left_bat + 50), 7)

        pygame.draw.line(screen, (180, 180, 180),
                         (WIDTH - BAT_DISTANCE_FROM_SCREEN, right_bat - 50),
                         (WIDTH - BAT_DISTANCE_FROM_SCREEN, right_bat + 50), 7)

        pygame.display.flip()

    pygame.quit()
