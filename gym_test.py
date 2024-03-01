import gym
import gym_tetris
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env


class CustomTetrisWrapper(gym.Wrapper):
    def __init__(self, env):
        super(CustomTetrisWrapper, self).__init__(env)

    def reset(self, **kwargs):
        # Capture all return values and keep only the observation
        observation, *_ = self.env.reset(**kwargs)
        return observation

def main():
    # Create the Tetris environment
    env = gym.make('TetrisA-v0')
    env = CustomTetrisWrapper(env)

    # Wrap it for vectorized environments
    env = make_vec_env(lambda: env, n_envs=1)

    # Create the PPO agent
    model = PPO("MlpPolicy", env, verbose=1)

    # Train the agent
    model.learn(total_timesteps=10000)

    # Test the trained agent
    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = env.step(action)
        env.render()

    env.close()

if __name__ == "__main__":
    main()
