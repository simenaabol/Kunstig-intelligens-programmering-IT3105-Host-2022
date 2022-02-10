config = {
    # 'problem': 'hanoi',
    'problem': 'gambler',
    #'problem': 'cart',
}


hanoiConfig = {

    'game_config': {
        'pegs': 3, 
        'discs': 3
    },

    'num_episodes': 100,
    'max_steps': 300,
    'critic': 'table',

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
        'eligibility_decay': 0.99,
        'layers': [25]
  
    }
} 

gamblerConfig = {
    
        'game_config': {
        'win_prob': 0.4, 
    },

    'num_episodes': 15000,
    'max_steps': 300,
    'critic': 'table',

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
        'eligibility_decay': 0.99,
        'layers': [25]
  
    }
}

cartConfig = {}

