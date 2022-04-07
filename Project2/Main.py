from Learner import RL_learner
from Topp import Topp
from Parameters import config, topp_config

def main():
    
    if config['mode'] == 'learn':
        rl = RL_learner(config)
        rl.training()
        
    elif config['mode'] == 'learn_topp':
        rl = RL_learner(config)
        rl.training()
        topp = Topp()
        topp.play_round_robin()
        
    elif config['mode'] == 'topp':
        topp = Topp(config, topp_config)
        topp.play_round_robin()
        
    else:
        raise ValueError("Enter correct mode!")
    

if __name__ == '__main__':
    main()