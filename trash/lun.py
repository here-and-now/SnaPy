import gym

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy


# Create environment
env = gym.make('LunarLander-v2')

# Instantiate the agent
model = PPO('MlpPolicy', env,  verbose=1, device='cuda')
# Train the agent
model.learn(total_timesteps=int(2e5))
