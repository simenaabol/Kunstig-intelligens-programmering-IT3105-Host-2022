config = {
    'game': 'hex',
    'num_actual_games': 300,
    'num_search_games': 50,
    'starting_player': 1
}

hex_config = {
    'board_size': 2,

    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layer_size': (256, 128, 64),
        'activation_function': 'relu',
        'output_act': 'softmax',
        'optimizer': 'adam',
        'loss_function': 'cross_entropy',

        'epsilon': 1, 
        'epsilon_decay': 0.9
    },

    'mcts_config': {
        'minibatch_size': 5,
        'exploration_weight': 1,
        'epochs': 100,
        'timout_max_time': 2
    }
}

nim_config = {

    'num_stones': 12,
    'max_removal': 3,
    'starting_player': 1,

    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layer_size': (4, 5, 3),
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

topp_config = {
    'game': 'nim',
    'number_of_games': 50
    
}