from stable_baselines3 import PPO
import os

from board_env import SnapyEnv
import time
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv, VecNormalize, VecMonitor


if __name__ == '__main__':

    name = 'snapy6'

    models_dir = f'models/{name}/'
    logdir = f'logs/{name}/'
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    num_cpu = 8
    
    env = SnapyEnv()
    env = SubprocVecEnv([lambda: env for i in range(num_cpu)])
    env = VecMonitor(env, logdir)

    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

    TIMESTEPS = 50000

    iters = 0
    while True:
        iters += 1
        
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
        model.save(f"{models_dir}/{TIMESTEPS*iters}")
        

