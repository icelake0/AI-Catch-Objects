import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from support import plot
from datetime import datetime

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self, gamma_value = None, model_patch = None):
        self.n_episodes = 1
        self.epsilon = 0 # randomness
        self.gamma = gamma_value # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # pops left when memory is full
        self.model = Linear_QNet(6, 256, 3)
        if model_patch != None :
            self.model.load_state_dict(torch.load(model_patch))
            self.model.eval()
        else :
            self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
        
    def get_state(self, store):
        return np.array(store.get_state(), dtype=int)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # pops left when memory is full
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_action(self, state, allow_explore = True):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_episodes
        final_move = [0,0,0]
        if allow_explore and random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move