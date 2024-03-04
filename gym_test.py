import gym
from nes_py.wrappers import JoypadSpace
from gym_tetris.actions import SIMPLE_MOVEMENT
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import torch

if torch.backends.mps.is_available():
    print("Using ROCm")
    device = torch.device("mps")
else:
    print("ROCm is not available. Using CPU instead.")
    device = torch.device("cpu")

# Define a wrapper function that discards unexpected keyword arguments
def wrap_env(env):
    class WrappedEnv(gym.Env):
        def __init__(self, e):
            self.env = e
            self.action_space = e.action_space
            self.observation_space = e.observation_space

        def reset(self, **kwargs):
            return self.env.reset()  # Ignore any keyword arguments

        def step(self, action):
            return self.env.step(action)

        def render(self, mode='human'):
            return self.env.render(mode)

        def close(self):
            return self.env.close()

    return WrappedEnv(env)

def main():
    # Create and wrap the original environment
    env = gym.make('TetrisA-v0')
    env = JoypadSpace(env, SIMPLE_MOVEMENT)
    env = wrap_env(env)  # Apply the wrapper that handles reset

    # Use the wrapped environment to create a vectorized environment
    vec_env = DummyVecEnv([lambda: env])

    # Instantiate the PPO agent
    model = PPO("MlpPolicy", vec_env, verbose=1, device=device)


    # Train the agent
    model.learn(total_timesteps=25000)
    model.save("tetris_model6")

    # Test the agent
    obs = vec_env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs.copy(), deterministic=True)
        obs, rewards, dones, info = vec_env.step(action)
        vec_env.render()
        if dones:
            obs = vec_env.reset()

    vec_env.close()

if __name__ == "__main__":
    main()
