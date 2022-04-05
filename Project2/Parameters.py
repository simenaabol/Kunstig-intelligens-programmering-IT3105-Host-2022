config = {
    'game': 'hex',
    'num_actual_games': 10000,
    'num_search_games': 1000,
    'starting_player': 1,
    
    'network_folder_name': 'natt_test' # Folder name for saving and loading the networks for TOPP
}

hex_config = {
    
    'board_size': 5,

    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layer_size': (256, 128, 64),
        'activation_function': 'relu', # relu, linear, sigmoid, tanh
        'output_act': 'softmax',
        'optimizer': 'adam', # adam, rmsprop, sgd, adagrad
        'loss_function': 'cross_entropy',

        'epsilon': 1, 
        'epsilon_decay': 0.95
    },

    'mcts_config': {
        'minibatch_size': 10,
        'exploration_weight': 0.75,
        'epochs': 100,
        'timout_max_time': 50
    }
}

nim_config = {

    'num_stones': 12,
    'max_removal': 3,
    'starting_player': 1,

    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layer_size': (4, 5, 3),
        'activation_function': 'relu', # relu, linear, sigmoid, tanh
        'output_act': 'softmax',
        'optimizer': 'adam', # adam, rmsprop, sgd, adagrad
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
    'number_of_games': 50
    
}