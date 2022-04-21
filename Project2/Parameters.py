config = {
    'game': 'hex',
    'num_actual_games': 10,
    'num_search_games': 1,
    'starting_player': 1,
    
    'lite_model_interval': 2,
    
    'saving_interval': 5,
    'save_nets': True,
    
    'mode': 'topp', # learn, learn_topp, topp
    

    # 'network_folder_name': 'anets' # 

    # 'network_folder_name': '7_anets1' # 
    # 'network_folder_name': '7_amd2' # 800 best
    # 'network_folder_name': '7_anets3' # 1480 best
    # 'network_folder_name': '7_bu1' # 40 er best
    # 'network_folder_name': '7_bu2' # søppel
    # 'network_folder_name': '7_bu1' # Folder name for saving and loading the networks for TOPP

    'network_folder_name': 'best' # Folder name for saving and loading the networks for TOPP
}

#  anets -> nr.5             1. litt bedre

#  7_anets1 -> nr.7             1. litt bedre
#  7_amd2 -> nr.             1. litt bedre
#  7_anets3-> nr. 16. og litt 28.           1. litt bedre

#  7_bu1-> nr.  11. og litt 16.          2. litt bedre'
#  7_bu2-> nr.   for liten


#  Samlet -> tror 25 fra topp er best


hex_config = {
    
    'board_size': 7, 


    'actor_config': {
        'learning_rate': 0.01, 
        'hidden_layer_size': (367, 94, 94,),
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
    'number_of_games': 2,
    'visualize_game': False,
    'visualize_robin': True
}