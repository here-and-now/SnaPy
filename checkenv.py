from stable_baselines3.common.env_checker import check_env

from board_env import SnapyEnv

env = SnapyEnv()

check_env(env)
