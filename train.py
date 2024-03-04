import gym
from nes_py.wrappers import JoypadSpace
from gym_tetris.actions import SIMPLE_MOVEMENT
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import torch
import os

class ModelTrainer:
    def __init__(self, model_path=None) -> None:
        self.model_path = model_path
        self.model = None

    def train(self, total_timesteps=2500000):
        if torch.cuda.is_available():
            print("Using GPU:", torch.cuda.get_device_name(0))
            device = torch.device("cuda")
        else:
            print("CUDA is not available. Using CPU instead.")
            device = torch.device("cpu")
        # Create and wrap the original environment
        env = gym.make('TetrisA-v3')
        env = JoypadSpace(env, SIMPLE_MOVEMENT)
        env = self.wrap_env(env)  # Apply the wrapper that handles reset

        # Use the wrapped environment to create a vectorized environment
        vec_env = DummyVecEnv([lambda: env])

        # Load existing model or create a new one
        if self.model_path and os.path.exists(self.model_path):
            print("Loading existing model from", self.model_path)
            self.model = PPO.load(self.model_path, vec_env)
        else:
            print("Creating a new model")
            self.model = PPO("MlpPolicy", vec_env, verbose=1,
                             learning_rate=0.000002,
                             n_steps=2048,
                             batch_size=64,
                             n_epochs=15,
                             gamma=0.99,
                             gae_lambda=0.95,
                             clip_range=0.2,
                             ent_coef=0.1,
                             device=device)

        self.model.learn(total_timesteps=total_timesteps)
        self.model.save("tetris_model_improved")

    @staticmethod
    def wrap_env(env):
        class WrappedEnv(gym.Env):
            def __init__(self, e):
                self.env = e
                self.action_space = e.action_space
                self.observation_space = e.observation_space

            def reset(self):
                return self.env.reset()

            def step(self, action):
                return self.env.step(action)

            def render(self, mode='human'):
                return self.env.render(mode)

            def close(self):
                return self.env.close()

        return WrappedEnv(env)

    def save(self, name):
        if self.model is not None:
            self.model.save(name)

trainer = ModelTrainer(model_path="testing_model.zip")

try:
    if __name__ == "__main__":
        trainer.train()
finally:
    trainer.save("testing_model")
