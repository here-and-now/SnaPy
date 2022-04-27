import os
import time
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv

from board_env import SnapyEnv
import glob


if __name__ == "__main__":
    name = 'snapy6_po'
        # version = '01890000'

    model_dir = f'/home/os/gits/SnaPy/models/{name}'
    
   

    def render_newest():
     
        files = [os.path.join(model_dir, x) for x in os.listdir(model_dir) if x.endswith(".zip")]
        newest = max(files, key=os.path.getctime)
        print(newest)

        model = PPO.load(newest, verbose=1)
        # model = PPO.load(f'models/{name}/{version}', verbose=1)

        # both working
        # model.set_env(SubprocVecEnv([lambda: SnapyEnv()]))
        # model.set_env(DummyVecEnv([lambda: SnapyEnv()]))


        # mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=1)
        # print('Mean reward', mean_reward)
        # print('Std reward', std_reward)

        env = SnapyEnv() 
        # env = DummyVecEnv([lambda: env])

        obs = env.reset()

        for _ in range(100):
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)
            env.render()
            if dones:
                env.reset()
        
        render_newest()
    render_newest()

