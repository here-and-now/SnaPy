from stable_baselines3 import PPO
import os

from board_env import SnapyEnv

import time


name = 'score2'
models_dir = f'models/{name}{int(time.time())}/'
logdir = f'logs/{name}{int(time.time())}/'

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = SnapyEnv(rend=True, rendrate=100)
env.reset()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10000
iters = 0
while True:
    iters += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
    model.save(f"{models_dir}/{TIMESTEPS*iters}")

