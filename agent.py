import torch
import random
import numpy as np
from collections import deque
from environmant import FragilePackagesStore
from model import Linear_QNet, QTrainer
from support import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        self.n_games = 1
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # pops left when memory is full
        self.model = Linear_QNet(6, 256, 3)
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
    
    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games #The more games we play the smaller our epsilon gets hence the less randome moves we make untill we stop making random move
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
    
    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    store = FragilePackagesStore()
    while True:
        # get old state
        state_old = agent.get_state(store)
        
        # get move
        final_move = agent.get_action(state_old)
        
        # perform move and get new state
        reward, done, score = store.monitor_store(final_move)
        state_new = agent.get_state(store)
        
        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        
         # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        
        print('Reword', reward)
        
        if done:
            # train long memory, plot result
            store.setup_store()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                    record = score
                    agent.model.save()
            
            print('Game', agent.n_games, 'Score', score, 'Record:', record, 'Done :', done)
            #plot model progress
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            


if __name__ == '__main__':
    train()