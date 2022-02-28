from Learner import RL_learner
from Parameters import config

def main():

    rl = RL_learner(config)
    rl.training()

if __name__ == '__main__':
    main()