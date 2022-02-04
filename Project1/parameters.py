config = {
    'problem': 'hanoi',
}


hanoiConfig = {

    'game_config': {
        'pegs': 3,
        'discs': 3,
    },

    'num_episodes': 1000,
    'critic': 'ann',

    'actor_config': {
        'learning_rate': 0.1,
        'gamma': 0.9,
        'epsilon': 1,
        'goal_epsilon': 0.001,
        'eligibility_decay': 0.99
    },

    'critic_config': {
        'learning_rate': 0.1,
        'gamma': 0.90,
        'eligibility_decay': 0.99
    },

    'anncritic_config': {
        'learning_rate': 1e-3,
        'gamma': 0.90,
        'eligibility_decay': 0.99,
        'layers': [25]
  
    }
} 

gamblerConfig = {}

cartConfig = {}

