config = {
    'problem': 'hanoi',
    #'problem': 'gambler',
    #'problem': 'cart',
}


hanoiConfig = {

    'game_config': {
        'pegs': 3,
        'discs': 4,
    },

    'num_episodes': 100,
    'max_steps': 300,
    'critic': 'table',

    'actor_config': {
        'learning_rate': 0.1,
        'discount_factor': 0.9,
        'epsilon': 1,
        'epsilon_decay': 0.95,
        'goal_epsilon': 0.001,
        'eligibility_decay': 0.95
    },

    'critic_config': {
        'learning_rate': 0.1,
        'discount_factor': 0.90,
        'eligibility_decay': 0.99
    },

    'anncritic_config': {
        'learning_rate': 1e-3,
        'discount_factor': 0.90,
        'eligibility_decay': 0.99,
        'layers': [25]
  
    }
} 

gamblerConfig = {}

cartConfig = {}

