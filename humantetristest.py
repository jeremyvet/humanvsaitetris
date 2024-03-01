from nes_py.wrappers import JoypadSpace
import gym_tetris
from gym_tetris.actions import MOVEMENT
import pygame

env = gym_tetris.make('TetrisA-v0')
env = JoypadSpace(env, MOVEMENT)
pygame.init()
screen = pygame.display.set_mode((400, 300))
# button_map = {
#         'right':  0b10000000,
#         'left':   0b01000000,
#         'down':   0b00100000,
#         'up':     0b00010000,
#         'start':  0b00001000,
#         'select': 0b00000100,
#         'B':      0b00000010,
#         'A':      0b00000001,
#         'NOOP':   0b00000000,
#     }

done = True
# for step in range(5000):
#     if done:
#         state = env.reset()
#     action = 0
#     #pygame.event.pump()
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     print("Spacebar pressed")
#     # events = pygame.event.get()
#     # for event in events:
#     #     print(event)
#     #     if event.type == pygame.KEYDOWN:
#     #         if event.key == pygame.K_SPACE:
#     #             action = 8
#     #         else:
#     #             action = 0
#     #print("before: " + str(action))
#     state, reward, done, info = env.step(action)
#     env.render()
#     #print("after: " + str(action))
#
# env.close()
# pygame.quit()
spacebar_pressed = False  # Flag to track spacebar press

for step in range(5000):
    if done:
        state = env.reset()
    action = 0
    pygame.event.pump()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spacebar_pressed = True  # Set flag to true if spacebar pressed

    if spacebar_pressed:
        action = 8  # Set action to 8 if spacebar pressed
        spacebar_pressed = False  # Reset flag after processing

    state, reward, done, info = env.step(action)
    env.render()
    print(action)

env.close()