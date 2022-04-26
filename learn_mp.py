from stable_baselines3 import PPO
import os

from board_env import SnapyEnv

import time
# from stable_baselines3.common.policies import MlpPolicy
# from stable_baselines3.common import set_global_seeds, make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv

def make_env(seeds=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        # env = gym.make(env_id)
        env = SnapyEnv()
        # env.seed(seed + rank)
        return env
    # set_global_seeds(seed)
    return _init



if __name__ == '__main__':

    name = 'score2_mp'
    models_dir = f'models/{name}{int(time.time())}/'
    logdir = f'logs/{name}{int(time.time())}/'


    num_cpu = 4  # Number of processes to use
    # Create the vectorized environment
    env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

    TIMESTEPS = 10000

    # model.learn(total_timesteps=TIMESTEPS)
    iters = 0
    while True:
        iters += 1
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
        model.save(f"{models_dir}/{TIMESTEPS*iters}")

