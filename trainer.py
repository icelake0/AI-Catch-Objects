from environmant import FragilePackagesStore
from support import plot
from datetime import datetime
from agent import Agent

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
    
class Trainer:  
    def train(train_gamma_value, train_negative_reward_value, training_time, plot_title_prifix = ""):
        start_time = datetime.now().strftime("%H:%M:%S")
        start_time = datetime.strptime(start_time, "%H:%M:%S")
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        agent = Agent(gamma_value = train_gamma_value)
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
                
                current_time = datetime.now().strftime("%H:%M:%S")
                current_time = datetime.strptime(current_time, "%H:%M:%S")
                print('Episode', agent.n_episodes, 'Time', (current_time - start_time).total_seconds(), 'Score', score, 'Record:', record, 'Done :', done)
                #plot model progress
                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_episodes
                plot_mean_scores.append(mean_score)
                plot_title = "{plot_title_prifix}Gamma: {train_gamma_value} Negative Reward: {train_negative_reward_value}".format(
                    plot_title_prifix = plot_title_prifix,
                    train_gamma_value = train_gamma_value,
                    train_negative_reward_value = train_negative_reward_value
                    )
                plot(plot_scores, plot_mean_scores, plot_title)
                if (current_time - start_time).total_seconds() >= training_time :
                    print("------Done training for ", training_time/60, "min(s)------")
                    plot(plot_scores, plot_mean_scores, plot_title, True)
                    store.exit()
                    return