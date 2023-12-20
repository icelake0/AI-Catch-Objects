from trainer import Trainer            

if __name__ == '__main__':
    train_gamma_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    train_negative_reward_values = [-10, -20, -30, -40, -50]
    for train_gamma_value in train_gamma_values:
        for train_negative_reward_value in train_negative_reward_values:
            Trainer.train(train_gamma_value, train_negative_reward_value, 60 * 60)