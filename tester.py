from environmant import FragilePackagesStore
from support import plot_test_results
from datetime import datetime
from agent import Agent

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
    
class Tester:  
    def test(model_patch, gamma_value, negative_reward_value, test_time):
        start_time = datetime.now().strftime("%H:%M:%S")
        start_time = datetime.strptime(start_time, "%H:%M:%S")
        plot_accuracey_scores = []
        agent = Agent(model_patch = model_patch)
        store = FragilePackagesStore(negative_reward_value)
        missed = 0
        catch = 0
        accuracey_score = 100
        while True:
            # get old state
            state_old = agent.get_state(store)
            
            # get move
            final_move = agent.get_action(state_old, False)
            
            # use move
            reward, done, score = store.monitor_store(final_move)
            
            if reward > 0:
                catch += 1
                
            if done:
                missed += 1
            
            if reward > 0 or done:
                plot_accuracey_scores.append(accuracey_score)
                accuracey_score =  catch / (catch + missed + 1) * 100
                
            
            if done:
                store.setup_store()
                agent.n_episodes += 1
                 
                plot_title = "Testing - Time: 12hours Gamma: {gamma_value} -veReward: {negative_reward_value} Catch: {catch} Missed: {missed} Episodes: {n_episodes} Package Count: {n_packages}".format(
                    test_time = (test_time / 60)/60,
                    gamma_value = gamma_value,
                    negative_reward_value = negative_reward_value,
                    catch = catch,
                    missed = missed,
                    n_episodes = agent.n_episodes,
                    n_packages = catch + missed
                    )
                plot_test_results(plot_accuracey_scores, plot_title)
                current_time = datetime.now().strftime("%H:%M:%S")
                current_time = datetime.strptime(current_time, "%H:%M:%S")
                if (current_time - start_time).total_seconds() >= test_time :
                    print("------Done testing for ", (test_time / 60)/60, "hours------")
                    plot_test_results(plot_accuracey_scores, plot_title, True)
                    store.exit()
                    return