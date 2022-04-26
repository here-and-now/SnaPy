import os
import time
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv

from board_env import SnapyEnv


name = 'score2'
version = '820000'

# model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)
model = PPO.load(f'models/{name}/{version}', verbose=1)

model.set_env(DummyVecEnv([lambda: SnapyEnv(rend=True, rendrate=10)]))
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

obs = model.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = model.step(action)
    # env.render()

