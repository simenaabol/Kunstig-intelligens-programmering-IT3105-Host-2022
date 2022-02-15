from learner import RL_learner
from parameters import config

def main():
    """ 

    Run this file to start the system.

    """
    rl = RL_learner(config)
    rl.training()
    rl.show_learning_graph(config['visualize'])

if __name__ == '__main__':
    main()