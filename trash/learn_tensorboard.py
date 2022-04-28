from stable_baselines3 import PPO
import os

from board_env import SnapyEnv

import time
# from stable_baselines3.common.policies import MlpPolicy
# from stable_baselines3.common import set_global_seeds, make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv

from stable_baselines3.common.callbacks import BaseCallback

import tensorflow as tf
class TensorboardCallback(BaseCallback):
    """
    Custom callback for plotting additional values in tensorboard.
    """
    def __init__(self, verbose=0):
        self.is_tb_set = False
        super(TensorboardCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        # Log scalar value (here a random variable)
        import numpy as np
        value = np.random.random()
        summary = tf.summary(value=[tf.summary.value(tag='random_value', simple_value=value)])
        self.locals['writer'].add_summary(summary, self.num_timesteps)
        return True

if __name__ == '__main__':

    name = 'snapy_3test'

    models_dir = f'models/{name}/'
    logdir = f'logs/{name}/'
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    from stable_baselines3.common.monitor import Monitor
    env = SnapyEnv()
    env = Monitor(env, logdir)
    env = DummyVecEnv([lambda: env])
    print(env)
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir )

    TIMESTEPS = 10000

    iters = 0
    while True:
        iters += 1
        
        # if TIMESTEPS*iters > 10000000:
            # break
        
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO",callback=TensorboardCallback())
        model.save(f"{models_dir}/{TIMESTEPS*iters}")
        print()
        

