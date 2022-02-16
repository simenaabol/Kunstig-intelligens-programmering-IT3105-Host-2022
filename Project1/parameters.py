config = {

    'problem': 'hanoi',
    'critic': 'table',
    # 'critic': 'nn',
    'visualize': True, 
    'frame_delay': 0.1
}

hanoiConfig = {

    'game_config': {
        'pegs': 3, 
        'discs': 4,
    },

    'num_episodes': 210,
    'max_steps': 300,

    'actor_config': {
        'learning_rate': 0.1, #0.01
        'discount_factor': 0.9,
        'epsilon': 1,
        'epsilon_decay': 0.99,
        'eligibility_decay': 0.9
    },

    'critic_config': {
        'learning_rate': 0.1,#0.1
        'discount_factor': 0.9,
        'eligibility_decay': 0.9
    },

    'anncritic_config': {
        'learning_rate': 0.0001,
        'discount_factor': 0.9,
        'input_size': 6,
        'hidden_layers': (5,)
    }
} 

gamblerConfig = {
    
    'game_config': {
        'win_prob': 0.4, 
    },

    'num_episodes': 15000,
    'max_steps': 310,

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
        'learning_rate': 0.0001,
        'discount_factor': 0.90,
        'input_size': 1,
        'hidden_layers': (15,)
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
        'F': 10
    },

    'num_episodes': 200,
    'max_steps': 310,

    'actor_config': {
        'learning_rate': 0.0002,
        'discount_factor': 0.99,
        'epsilon': 0.99,
        'epsilon_decay': 0.99,
        'eligibility_decay': 0.99
    },

    'critic_config': {
        'learning_rate': 0.001,
        'discount_factor': 0.99,
        'eligibility_decay': 0.99
    },

    'anncritic_config': {
        'learning_rate': 0.0001,
        'discount_factor': 0.9,
        'input_size': 1,
        'hidden_layers': (2, 5, 3)
    }
}

