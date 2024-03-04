import gym
from nes_py.wrappers import JoypadSpace
from gym_tetris.actions import SIMPLE_MOVEMENT
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import torch
from stable_baselines3.ppo import MlpPolicy

if torch.cuda.is_available():
    print("Using GPU:", torch.cuda.get_device_name(0))
    device = torch.device("cuda")
else:
    print("CUDA is not available. Using CPU instead.")
    device = torch.device("cpu")

# Define a wrapper function that discards unexpected keyword arguments
def wrap_env(env):
    class WrappedEnv(gym.Env):
        def __init__(self, e):
            self.env = e
            self.action_space = e.action_space
            self.observation_space = e.observation_space

        # def reset(self, **kwargs):
        #     return self.env.reset()  # Ignore any keyword arguments

        def reset(self):
            return self.env.reset()

        def step(self, action):
            return self.env.step(action)

        def render(self, mode='human'):
            return self.env.render(mode)

        def close(self):
            return self.env.close()

    return WrappedEnv(env)

model = None

class ModelTrainer:
    def __init__(self) -> None:
        self.model = None

    def train(self):
        # Create and wrap the original environment
        env = gym.make('TetrisA-v3')
        env = JoypadSpace(env, SIMPLE_MOVEMENT)
        env = wrap_env(env)  # Apply the wrapper that handles reset

        # Use the wrapped environment to create a vectorized environment
        vec_env = DummyVecEnv([lambda: env])

        self.model = PPO(MlpPolicy, vec_env, verbose=1,
                learning_rate=0.00025,
                n_steps=2048,
                batch_size=64,
                n_epochs=10,
                gamma=0.99,
                gae_lambda=0.95,
                clip_range=0.2,
                ent_coef=0.01, device=device)

        self.model.learn(total_timesteps=150000)
        self.model.save("tetris_model_improved")

        # Instantiate the PPO agent
        # model = PPO("MlpPolicy", vec_env, verbose=1, device=device)
        #
        #
        # # Train the agent
        # model.learn(total_timesteps=25000)
        # model.save("tetris_model6")

        # Test the agent
        obs = vec_env.reset()
        for _ in range(1000):
            action, _states = model.predict(obs.copy(), deterministic=True)
            obs, rewards, dones, info = vec_env.step(action)
            vec_env.render(mode='human')
            if dones:
                obs = vec_env.reset()

        vec_env.close()
    
    def save(self, name):
        if self.model is not None:
            self.model.save(name)

trainer = ModelTrainer()

try:
    if __name__ == "__main__":
        trainer.train()
finally:
    trainer.save("CRASH_SAVED_MODEL")