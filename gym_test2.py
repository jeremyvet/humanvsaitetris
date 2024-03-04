import gym
import gym_tetris
from stable_baselines import PPO2
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


def main():
    # Create the environment
    env = gym.make('TetrisA-v3')

    # Create the PPO agent
    model = PPO2('MlpPolicy', env)

    # Train the agent
    model.learn(total_timesteps=10000)

    # Test the agent
    obs = env.reset()
    for _ in range(1000):
        action, _ = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()

    env.close()

if __name__ == "__main__":
    main()