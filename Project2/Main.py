from Learner import RL_learner
from Topp import Topp
from Parameters import config
from Parameters import topp_config

def main():

    # rl = RL_learner(config)
    # rl.training()
    topp = Topp()
    topp.play_round_robin()
    # topp.bestVSbest()
    

if __name__ == '__main__':
    main()