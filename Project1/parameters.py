config = {
    # 'problem': 'hanoi',
    # 'problem': 'gambler',
    'problem': 'cart',


    'critic': 'table',
    # 'critic': 'nn'
}


hanoiConfig = {

    'game_config': {
        'pegs': 3, 
        'discs':3,
    },

    'num_episodes': 150,
    'max_steps': 300,

    'actor_config': {
        'learning_rate': 0.01,
        'discount_factor': 0.9,
        'epsilon': 1,
        'epsilon_decay': 0.99,
        'eligibility_decay': 0.99
    },

    'critic_config': {
        'learning_rate': 0.1,
        'discount_factor': 0.9,
        'eligibility_decay': 0.99
    },

    'anncritic_config': {
        'learning_rate': 1e-3,
        'discount_factor': 0.90,
        'input_size': 1,
        'num_layers': 25
    }
} 

gamblerConfig = {
    
    'game_config': {
        'win_prob': 0.4, 
    },

    'num_episodes': 15000,
    'max_steps': 300,

    'actor_config': {
        'learning_rate': 0.01,
        'discount_factor': 0.9,
        'epsilon': 1,
        'epsilon_decay': 0.99,
        'goal_epsilon': 0.001,
        'eligibility_decay': 0.99
    },

    'critic_config': {
        'learning_rate': 0.1,
        'discount_factor': 0.9,
        'eligibility_decay': 0.99
    },

    'anncritic_config': {
        'learning_rate': 1e-3,
        'discount_factor': 0.90,
        'input_size': 1,
        'num_layers': 25
    }
}


cartConfig = {

    'game_config': {
        'L': 0.5,
        'Mp': 0.1,
        'g': 9.8,
        't': 0.002,
        'Mc': 1.0,
        'x0': 0.0,
        'thM': 0.21,
        'nX': -2.4,
        'pX': 2.4,
        'T': 300,
        'step': 0,
        'nF': -10,
        'pF': 10
    },

    'num_episodes': 200,
    'max_steps': 300,

    'actor_config': {
        'learning_rate': 0.01,
        'discount_factor': 0.9,
        'epsilon': 1,
        'epsilon_decay': 0.99,
        'goal_epsilon': 0.001,
        'eligibility_decay': 0.99
    },

    'critic_config': {
        'learning_rate': 0.1,
        'discount_factor': 0.9,
        'eligibility_decay': 0.99
    },

    'anncritic_config': {
        'learning_rate': 1e-3,
        'discount_factor': 0.90,
        'input_size': 1,
        'num_layers': 25
    }
}

