import gym
import pygame.key
from gymnasium.spaces import Box
from gym.utils.play import play
from nes_py.wrappers import JoypadSpace
import gym_tetris
from gym_tetris.actions import MOVEMENT

# env = gym_tetris.make('TetrisA-v0', render_mode="human")
# env = JoypadSpace(env, MOVEMENT)
# play(gym.make('TetrisA-v0'))
#
# done = True
# for step in range(5000):
#     if done:
#         state = env.reset()
#     #AS = env.action_space.
#     state, reward, done, info = env.step(env.action_space.sample())
#     env.render()
#
# env.close()
#
if __name__ == "__main__":
    pygame.init()
    print(pygame.key.key_code("left") == pygame.K_LEFT)
    print(MOVEMENT)



