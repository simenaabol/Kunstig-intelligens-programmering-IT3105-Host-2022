config = {
    'game': 'hex',
    'num_actual_games': 5000,
    'num_search_games': 500,
    'starting_player': 1,
    
    'lite_model_interval': 5,
    
    'saving_interval': 5,
    'save_nets': True,
    
    'mode': 'topp', # learn, learn_topp, topp
    
    'network_folder_name': 'thom' # Folder name for saving and loading the networks for TOPP
}

hex_config = {
    
    'board_size': 4,

    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layer_size': (512, 256, 128, 64),
        'activation_function': 'relu', # relu, linear, sigmoid, tanh
        'output_act': 'softmax',
        'optimizer': 'adam', # adam, rmsprop, sgd, adagrad
        # 'loss_function': 'cross_entropy', BRUKES IKKE
        
        'anet_batch_size': 64,

        'epsilon': 1, 
        'epsilon_decay': 0.95
    },

    'mcts_config': {
        'minibatch_size': 512,
        'exploration_weight': 1,
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
        'hidden_layer_size': (512, 256, 128, 64),
        'activation_function': 'relu', # relu, linear, sigmoid, tanh
        'output_act': 'softmax',
        'optimizer': 'adam', # adam, rmsprop, sgd, adagrad
        # 'loss_function': 'cross_entropy', BRUKES IKKE
        
        'anet_batch_size': 64,

        'epsilon': 1, 
        'epsilon_decay': 0.95
    },

    'mcts_config': {
        'minibatch_size': 512,
        'exploration_weight': 1,
        'epochs': 10,
        'timout_max_time': 50
    }
}

topp_config = {
    'number_of_games': 50
}