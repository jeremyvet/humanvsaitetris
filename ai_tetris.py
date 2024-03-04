import gym
import gym_tetris
from stable_baselines3 import PPO
from nes_py.wrappers import JoypadSpace
from gym_tetris.actions import SIMPLE_MOVEMENT
import numpy as np

TETRIS_MODEL_FILE = "testing_model.zip"


def play_tetris(model_path):
    env = gym.make('TetrisA-v3')
    env = JoypadSpace(env, SIMPLE_MOVEMENT)
    model = PPO.load(model_path)

    obs = env.reset()

    while True:
        action, _states = model.predict(obs.copy(), deterministic=False)
        print(f"Original action: {action}, Type: {type(action)}")

        # Ensure that action is a single integer
        if isinstance(action, np.ndarray):
            action = action.item()  # or action = int(action[0])
        print(f"Processed action: {action}")

        obs, rewards, done, info = env.step(action)
        env.render()

        if done:
            print("Game over")
            break

    env.close()

play_tetris(TETRIS_MODEL_FILE)