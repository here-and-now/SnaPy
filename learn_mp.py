from stable_baselines3 import PPO
import os

from board_env import SnapyEnv
import time
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv, VecNormalize, VecMonitor


if __name__ == '__main__':

    name = 'snapy8bs'
    models_dir = f'models/{name}/'
    logdir = f'logs/{name}/'
    num_cpu = 20
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    # reward parameters dict
    reward_dict = {
            'food_reward': 5,
            'step_reward': 1,  
            'ouroboros_reward': 0.1,  
            'wall_reward': 0
            }

    #iniate env with rewards
    env = SnapyEnv(**reward_dict)
    # create n_cpu SubprocVecEnv for multiprocessing
    env = SubprocVecEnv([lambda: env for i in range(num_cpu)])
    # add envs to VecMonitor to get rollout logging data
    env = VecMonitor(env, logdir)
    
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

    TIMESTEPS = 50000
    iters = 0
    while True:
        iters += 1
        
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
        model.save(f"{models_dir}/{TIMESTEPS*iters}")
        

