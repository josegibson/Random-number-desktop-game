
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from RNG_core import RandomNumberGame

env = RandomNumberGame()
episodes = 10
env.train(episodes)