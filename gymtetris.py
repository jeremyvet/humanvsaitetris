from nes_py.wrappers import JoypadSpace
import gym_tetris
from gym_tetris.actions import MOVEMENT

env = gym_tetris.make('TetrisA-v0')
env = JoypadSpace(env, MOVEMENT)

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
for step in range(5000):
    if done:
        state = env.reset()

    action = 8 if step % 2 == 1 else 0
    state, reward, done, info = env.step(action)
    env.render()

env.close()
