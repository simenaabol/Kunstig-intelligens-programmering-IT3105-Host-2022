from learner import RL_learner
from parameters import config

def main():
    rl = RL_learner(config)
    rl.training()
    rl.show_learning_graph()

if __name__ == '__main__':
    main()