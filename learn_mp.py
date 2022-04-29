from stable_baselines3 import PPO
import os

# from board_env import SnapyEnv
from snapy_env import SnapyEnv
import time
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv, VecNormalize, VecMonitor
import json
import torch

if __name__ == '__main__':

    name = '9_pos_under_action'
    models_dir = f'models/{name}/'
    logdir = f'logs/{name}/'

    num_cpu = 20
 
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    # reward parameters dict
    reward_dict = {
            'food_reward': 1000,
            'step_reward': 0,  
            'ouroboros_reward': -5,  
            'wall_reward':-5, 
            }
    with open(models_dir + 'rewards', 'w') as f:
        f.write(json.dumps(reward_dict))


    # torch.multiprocessing.set_start_method('spawn')
    # iniate env with rewards
    # create n_cpu SubprocVecEnv for multiprocessing
    # add envs to VecMonitor to get rollout logging data
    env = SnapyEnv(**reward_dict)
    # env = env.to('cuda')
    env = SubprocVecEnv([lambda: env for i in range(num_cpu)])
    env = VecMonitor(env, logdir)

    # env = SnapyEnv(**reward_dict)
    
    # env = SnapyEnv(**reward_dict)
    # env = DummyVecEnv([lambda: env])
    # env = Monitor(env, logdir)

    # model stuff 
    # model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir, device='cuda')
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir, device='cpu')
    # model.learn(total_timesteps=10000)
    TIMESTEPS = 100000
    # max_iters = 25


    start = time.time() 
    iters = 0
    max_iters = 250
    # while iters < max_iters:
    while True:
        iters += 1
        
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
        model.save(f"{models_dir}/{TIMESTEPS*iters}")
    end = time.time()
    print('Final time:', end-start)
