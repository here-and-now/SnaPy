from stable_baselines3 import PPO
import os

from board_env import SnapyEnv

import time
# from stable_baselines3.common.policies import MlpPolicy
# from stable_baselines3.common import set_global_seeds, make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv


if __name__ == '__main__':

    name = 'snapy_3test'

    models_dir = f'models/{name}/'
    logdir = f'logs/{name}/'
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    num_cpu = 8
    

    # from stable_baselines3.common.vec_env import VecMonitor
    # env = SubprocVecEnv([lambda: SnapyEnv() for i in range(num_cpu)])
    # env = VecMonitor(env, logdir)
    
    from stable_baselines3.common.monitor import Monitor
    env = SnapyEnv()
    env = Monitor(env, logdir)
    env = DummyVecEnv([lambda: env])
    print(env)

    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir )

    TIMESTEPS = 10000

    # model.learn(total_timesteps=TIMESTEPS)
    iters = 0
    while True:
        iters += 1
        
        # if TIMESTEPS*iters > 10000000:
            # break
        
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
        model.save(f"{models_dir}/{TIMESTEPS*iters}")
        print()
        

