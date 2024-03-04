# import time
#
# import gym
# from gym import spaces
# import gym_tetris
# from gym_tetris.actions import SIMPLE_MOVEMENT
# from stable_baselines3 import PPO
# from nes_py.wrappers import JoypadSpace
#
# import gym
# import numpy as np
#
# class TetrisWrapper(gym.Env):
#     def __init__(self, env):
#         self.env = env
#         self.action_space = self.env.action_space
#         self.observation_space = self.env.observation_space
#
#     def reset(self):
#         #obs = self.env.reset()
#         #return obs, {}  # Add an empty info dictionary
#         return self.env.reset()
#
#     def step(self, action):
#         obs, reward, done, info = self.env.step(action)
#         if isinstance(done, bool):
#             done = (done, False)  # Convert to a tuple if necessary
#         return obs, reward, done, info
#
#     def render(self, mode='human', **kwargs):
#         return self.env.render(mode=mode, **kwargs)
#
#     def close(self):
#         self.env.close()
#
#
# def main():
#     env = TetrisWrapper(gym.make('TetrisA-v3'))
#     env = JoypadSpace(env, SIMPLE_MOVEMENT)
#     model = PPO.load("tetris_model_improved.zip")
#
#     # Adjust here: Unpack the tuple and get only the observation
#     obs, _ = env.reset()
#
#     for _ in range(1000):
#         action, _states = model.predict(obs.copy(), deterministic=True)
#         obs, rewards, done, info = env.step(action)
#         env.render()
#
#         if done:
#             # Again, unpack the tuple
#             obs, _ = env.reset()
#
#     env.close()
#
# if __name__ == "__main__":
#     main()

import gym
import numpy as np
from gym_tetris.actions import SIMPLE_MOVEMENT
from stable_baselines3 import PPO
from nes_py.wrappers import JoypadSpace

class TetrisWrapper(gym.Env):
    def __init__(self, env):
        self.env = env
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def reset(self):
        return self.env.reset()  # Return only the observation

    def step(self, action):
        return self.env.step(action)  # Forward the call to the original env

    def render(self, mode='human', **kwargs):
        return self.env.render(mode=mode, **kwargs)

    def close(self):
        self.env.close()


def main():
    env = TetrisWrapper(gym.make('TetrisA-v3'))
    env = JoypadSpace(env, SIMPLE_MOVEMENT)
    model = PPO.load("tetris_model_improved.zip")

    obs = env.reset()

    for _ in range(1000):
        action, _states = model.predict(obs.copy(), deterministic=True)
        # Directly convert the action to an integer
        action = int(action)
        obs, rewards, done, info = env.step(action)
        env.render()

        if done:
            print("Game over, resetting...")
            obs = env.reset()

    env.close()

if __name__ == "__main__":
    main()
