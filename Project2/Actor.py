from NeuralNetwork import NeuralNet

import numpy as np
import random
import tensorflow as tf
from Parameters import config

class ANET:
    def __init__(self,
                 model, 
                 learning_rate, 
                 hidden_layer_size, 
                 activation_function, 
                 output_act, optimizer, 
                 epsilon, 
                 epsilon_decay, 
                 state_manager):
        
        if model:
            self.model = model
            
        else:
            self.net = NeuralNet(learning_rate, 
                                hidden_layer_size, 
                                activation_function,
                                output_act, 
                                optimizer)

            self.model = self.net.init_model(state_manager)

        self.state_manager = state_manager
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        
        self.gameconfig = state_manager.get_parameters()
        
    def save_net(self, name):
        """ MULIG DU MÅ ENDRE DENNE SIMEN """
        
        self.model.save("./TrainedNets/{folder}/{name}".format(name=name, folder=config['network_folder_name']))
        
    def get_model(self):
        
        return self.model

    def update_epsilon(self, just_policy=False):
        
        self.epsilon *= self.epsilon_decay

        if just_policy:
            self.epsilon = 0

    def fit_network(self, x, y, epochs):
        
        self.model.fit(x=x, y=y, epochs=epochs, batch_size=self.gameconfig['actor_config']['anet_batch_size'])
        
    def get_action(self, lite_model, state, player, do_random_move=True):
        
        legal_actions = self.state_manager.get_legal_moves(state)
        all_actions = self.state_manager.get_all_moves()
        
        state_for_model = np.concatenate(([player], state), axis=None)
        
        state_for_model = tuple(state_for_model.tolist())
        
        if lite_model:
            distribution = lite_model.predict_single(state_for_model)
        else:
            distribution = self.model(tf.convert_to_tensor([state_for_model])).numpy()
        
        distribution = distribution.reshape(distribution.shape[-1])
        
        for i, move in enumerate(all_actions):
            if move not in legal_actions:
                distribution[i] = 0
                
                distribution /= np.sum(distribution) # Renormalize
                
        distribution = np.array(distribution)
        
        if sum(distribution.flatten()) <= 0:
            return random.choice(legal_actions)
           
        if random.uniform(0,1) < self.epsilon and do_random_move:
            indices, = np.nonzero(distribution.flatten())
            ind = np.random.choice(indices)
        else:
            ind = np.argmax(distribution)
        
        return all_actions[ind]