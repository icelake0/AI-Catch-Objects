import torch
import random
import numpy as np
from collections import deque
from environmant import FragilePackagesStore
from model import Linear_QNet, QTrainer
from support import plot
from datetime import datetime

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self, gamma_value):
        self.n_episodes = 1
        self.epsilon = 0 # randomness
        self.gamma = gamma_value # discount rate
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
        self.epsilon = 80 - self.n_episodes
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
    
    
def train(train_gamma_values, train_negative_reward_value):
    start_time = datetime.now().strftime("%H:%M:%S")
    start_time = datetime.strptime(start_time, "%H:%M:%S")
    training_time = 20 #train for 60 mins 
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent(train_gamma_values)
    store = FragilePackagesStore(train_negative_reward_value)
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
        
        # print('Reword', reward)
        
        if done:
            # train long memory, plot result
            store.setup_store()
            agent.n_episodes += 1
            agent.train_long_memory()
            
            if score > record:
                    record = score
                    agent.model.save()
            
            print('Episode', agent.n_episodes, 'Score', score, 'Record:', record, 'Done :', done)
            #plot model progress
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_episodes
            plot_mean_scores.append(mean_score)
            plot_title = "Training Gamma: {train_gamma_value} Negative Reward: {train_negative_reward_value}".format(
                train_gamma_value = train_gamma_value, train_negative_reward_value = train_negative_reward_value
                )
            plot(plot_scores, plot_mean_scores, plot_title)
            current_time = datetime.now().strftime("%H:%M:%S")
            current_time = datetime.strptime(current_time, "%H:%M:%S")
            if (current_time - start_time).total_seconds() >= training_time :
                print("------Done training for ", training_time/60, "min(s)------")
                plot(plot_scores, plot_mean_scores, plot_title, True)
                store.exit()
                return
            


if __name__ == '__main__':
    train_gamma_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 0.9, 1]
    train_negative_reward_values = [-10, -20, -30, -40, -50]
    for train_gamma_value in train_gamma_values:
        for train_negative_reward_value in train_negative_reward_values:
            train(train_gamma_value, train_negative_reward_value)