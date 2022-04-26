from stable_baselines3 import PPO
import os
from stable_baselines3.common.evaluation import evaluate_policy
import gym

from board_env import SnapyEnv

import time


name = 'score2'
models_dir = f'models/{name}{int(time.time())}/'
logdir = f'logs/{name}{int(time.time())}/'

# env = SnapyEnv(rend=True, rendrate=25)
# print(env)
# env.reset()

# model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)
from stable_baselines3.common.vec_env import DummyVecEnv
model = PPO.load('models/score21650991374/750000', verbose=1)

model.set_env(DummyVecEnv([lambda: SnapyEnv(rend=True)]))
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

# obs = env.reset()
# for i in range(1000):
    # action, _states = model.predict(obs)
    # obs, rewards, dones, info = env.step(action)
    # env.render()

