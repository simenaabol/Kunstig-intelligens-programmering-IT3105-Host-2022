config = {
    'game': 'nim',
    'num_actual_games': 4000,
    'num_search_games': 500,
    'starting_player': 1,
    
    'saving_interval': 50,
    'save_nets': False,
    
    'mode': 'learn', # learn, learn_topp, topp
    
    'network_folder_name': 'test_niklas' # Folder name for saving and loading the networks for TOPP
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
        
        'anet_batch_size': 64,

        'epsilon': 1, 
        'epsilon_decay': 0.95
    },

    'mcts_config': {
        'minibatch_size': 10,
        'exploration_weight': 0.75,
        'epochs': 10,
        'timout_max_time': 50
    }
}

nim_config = {

    'num_stones': 12,
    'max_removal': 3,
    'starting_player': 1,

    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layer_size': (256, 128, 64),
        'activation_function': 'relu', # relu, linear, sigmoid, tanh
        'output_act': 'softmax',
        'optimizer': 'adam', # adam, rmsprop, sgd, adagrad
        'loss_function': 'cross_entropy',
        
        'anet_batch_size': 64,

        'epsilon': 1, 
        'epsilon_decay': 0.95
    },

    'mcts_config': {
        'minibatch_size': 10,
        'exploration_weight': 0.75,
        'epochs': 10,
        'timout_max_time': 50
    }
    

}

topp_config = {
    'number_of_games': 50
}