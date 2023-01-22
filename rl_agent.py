import tensorflow as tf
import random
import numpy as np
from collections import deque

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
    
    def _build_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='relu'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate), metrics=['mse'])
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            action = [random.random() for _ in range(13)]
            action = [i/sum(action) for i in action]
            action = [round(a, 2) for a in action]
        else:
            action = self.model.predict(state)
            action = [round(a, 2) for a in action[0]]

        return action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        states = np.array([i[0] for i in minibatch]).reshape(batch_size, self.state_size)
        rewards = np.array([i[2] for i in minibatch]).reshape(batch_size, self.action_size)
        self.model.fit(states, rewards, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay




