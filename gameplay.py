import random

import pygame
from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticPolicy

from environment import DOWN, Environment, STAND, UP
from game import Game

WIDTH = 800
HEIGHT = 600

BAT_DISTANCE_FROM_SCREEN = 3

if __name__ == '__main__':
    game = Game(WIDTH, HEIGHT, 100, 15, 30)
    game.reset()

    env = Environment(game)
    model = PPO(ActorCriticPolicy, env, verbose=1)
    model.learn(total_timesteps=15000)

    obs = env.reset()

    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    rain = [[random.random() * WIDTH * 1.1 * 100, random.random() * 10] for _ in range(10)]

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        action = STAND
        if keys[pygame.K_DOWN]:
            action = DOWN
        if keys[pygame.K_UP]:
            action = UP

        obs = env._pull_observation()
        print('=' * 20)
        print(obs)
        rl_action, _states = model.predict(obs, deterministic=True)
        print(env._pull_observation())

        game.advance(rl_action, action)

        screen.fill((25, 25, 25))
        # pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, HEIGHT), 5)

        pygame.draw.circle(screen, (200, 200, 200), (game.ball.x, game.ball.y), 13)
        pygame.draw.circle(screen, (51, 133, 161), (game.ball.x, game.ball.y), 11)

        if random.random() < 0.05:
            rain.append([random.random() * WIDTH * 1.1 - 100, random.random() * 10])

        for droplet in rain:
            droplet[0] += 0.025
            droplet[1] += 0.1

            pygame.draw.line(screen, (200, 200, 200),
                             (droplet[0], droplet[1]),
                             (droplet[0] + 2.5, droplet[1] + 10), 1)

        for i in range(len(rain) - 1, -1, -1):
            if rain[i][1] > HEIGHT:
                del rain[i]

        pygame.draw.line(screen, (180, 180, 180),
                         (BAT_DISTANCE_FROM_SCREEN, game.left_matka.y - game.matka_length // 2),
                         (BAT_DISTANCE_FROM_SCREEN, game.left_matka.y + game.matka_length // 2), 7)

        pygame.draw.line(screen, (180, 180, 180),
                         (WIDTH - BAT_DISTANCE_FROM_SCREEN, game.right_matka.y - game.matka_length // 2),
                         (WIDTH - BAT_DISTANCE_FROM_SCREEN, game.right_matka.y + game.matka_length // 2), 7)

        if env.game.has_ended():
            running = False

        pygame.display.flip()

    pygame.quit()
