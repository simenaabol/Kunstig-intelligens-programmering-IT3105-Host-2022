config = {
    'game': 'hex',
    'num_actual_games': 100,
    'num_search_games': 500
}

hex_config = {
    'board_size': 7,

    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layers': (4, 5, 3),
        'activation_function': 'relu',
        'output_act': 'softmax',
        'optimizer': 'adam',
        'loss_function': 'cross_entropy',

        'epsilon': 1, 
        'epsilon_decay': 0.99
    },

    'mcts_config': {
        'minibatch_size': 5,
        'exploration_weight': 0,
        'epochs': 100,
        'timout_max_time': 2
    }
}

nim_config = {

    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layers': (4, 5, 3),
        'activation_function': 'relu',
        'output_act': 'softmax',
        'optimizer': 'adam',
        'loss_function': 'cross_entropy',

        'epsilon': 1, 
        'epsilon_decay': 0.99
    },

    'mcts_config': {
        'minibatch_size': 5,
        'exploration_weight': 0,
        'epochs': 100,
        'timout_max_time': 2
    }
}