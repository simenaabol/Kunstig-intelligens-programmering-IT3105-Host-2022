config = {
    'game': 'hex',
    'num_actual_games': 1,
    'num_search_games': 10,
    'starting_player': 1,
    
    'lite_model_interval': 5,
    
    'saving_interval': 5,
    'save_nets': True,
    
    'mode': 'topp', # learn, learn_topp, topp
    
    # 'network_folder_name': '4' # Folder name for saving and loading the networks for TOPP
    'network_folder_name': '4_hex_demo' # Folder name for saving and loading the networks for TOPP
}

hex_config = {
    
    'board_size': 4,

    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layer_size': (70, 50),
        'activation_function': 'tanh', # relu, linear, sigmoid, tanh
        'optimizer': 'adam', # adam, rmsprop, sgd, adagrad
        'output_act': 'softmax',
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
    'number_of_games': 16,
    'topp_eps': 0,
    'visualize_game': True,
    'visualize_robin': True
}