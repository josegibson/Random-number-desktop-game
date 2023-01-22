import random
import numpy as np
from rl_agent import DQNAgent

class RandomNumberGame:
    def __init__(self):
        self.balance = 10
        self.done = False
        self.state_size = 2
        self.action_size = 13
        self.agent = DQNAgent(self.state_size, self.action_size)
        self.batch_size = 64

    def set_win_matrix(self, number):
        win_matrix = [0] * 13
        win_matrix[number] = 9
        win_matrix[10] = 2 if number in [1, 3, 7, 9] else 1.5 if number == 5 else 0
        win_matrix[11] = 2 if number in [2, 4, 6, 8] else 1.5 if number == 0 else 0
        win_matrix[12] = 4.5 if number in [0, 5] else 0
        return win_matrix

    def play_round(self, bets_matrix):
        win_matrix = self.set_win_matrix(random.randint(0, 9))
        prize_matrix = [round(win_matrix[i] * bets_matrix[i] * 0.97, 2) for i in range(13)]
        return prize_matrix

    def step(self, action, round):
        bets_matrix = action
        reward = self.play_round(bets_matrix)
        self.balance += sum(reward) - sum(bets_matrix)
        self.done = self.balance <= 0
        next_state =[round + 1, self.balance]
        if len(self.agent.memory) > self.batch_size: 
            self.agent.replay(self.batch_size)
        return next_state, reward, self.done
    
    def reset(self):
        self.balance = 10
        self.done = False
        state = [1, self.balance]
        return state

    def train(self, episodes):
        for e in range(episodes):
            state = self.reset()
            state = np.reshape(state, [1, self.state_size])
            time = state[0, 0]
            while not self.done:
                
                action = self.agent.act(state)
                next_state, reward, done = self.step(action, time)
                next_state = np.reshape(next_state, [1, self.state_size])
                self.agent.remember(state, action, reward, next_state, done)
                state = next_state
                if len(self.agent.memory) > self.batch_size:
                    print(f"Dreaming at round {time}")
                    self.agent.replay(self.batch_size)
                time += 1
            print("episode: {}/{}, score: {}, e: {:.2}".format(e, episodes, time, self.agent.epsilon))

