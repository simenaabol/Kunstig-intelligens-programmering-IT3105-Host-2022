from NeuralNetwork import NeuralNet

import numpy as np
import random
import tensorflow as tf
from Parameters import config

from LiteModel import LiteModel

class ANET:
    def __init__(self,
                 model, 
                 learning_rate, 
                 hidden_layer_size, 
                 activation_function, 
                 output_act, optimizer, 
                 loss_function, epsilon, 
                 epsilon_decay, 
                 state_manager):
        
        if model:
            self.model = model
            
        else:
            self.net = NeuralNet(learning_rate, 
                                hidden_layer_size, 
                                activation_function,
                                output_act, 
                                optimizer,
                                loss_function)

            self.model = self.net.init_model(state_manager)

        self.state_manager = state_manager
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        
        self.gameconfig = state_manager.get_parameters()
        
    def save_net(self, name):
        
        self.model.save("Project2/NeuralNets/{folder}/{name}".format(name=name, folder=config['network_folder_name']))
        
    def get_model(self):
        return self.model

    def update_epsilon(self, just_policy=False):
        
        self.epsilon *= self.epsilon_decay

        if just_policy:
            self.epsilon = 0

    def fit_network(self, x, y, epochs):
        
        self.model.fit(x=x, y=y, epochs=epochs, verbose=0, batch_size=self.gameconfig['actor_config']['anet_batch_size'])
        
    def get_action(self, lite_model, state, player, do_random_move=True):
        legal_actions = self.state_manager.get_legal_moves(state)
        all_actions = self.state_manager.get_all_moves()
        
        state = np.array(self.state_manager.get_state()) # Litt usikker på denne
        # state = tuple(self.state_manager.get_state())
        
        state_for_model = np.concatenate(([player], state), axis=None)
        
        # state_for_model = state_for_model.reshape((1,) + state_for_model.shape)
        
        # Variant for HEX under -> Retter opp feilmelidng som ligger i linje 75
        # state_for_model = np.concatenate((state.flatten()), axis=None)
        
        #  distribution = self.state_manager.get_normalized_distribution()
        #  Hent fra selve nettverket ANN
        # distribution = self.ANET.predict_val(state).tolist()

        state_for_model = tuple(state_for_model.tolist())
        # state_for_model = state_for_model.tolist()
        # print(state_for_model)
        
        # new_model = LiteModel.from_keras_model(self.model)
        
        # distribution = new_model.predict_single(state_for_model)
        
        if lite_model:
            distribution = lite_model.predict_single(state_for_model)
        else:
            distribution = self.model(tf.convert_to_tensor([state_for_model])).numpy()  
            
        # print(distribution)
        
        # distribution = distribution * np.array(all_actions)
        # distribution = distribution * np.array(all_actions)
        # distribution = distribution.flatten() # denne ødelegger kordinat-strukturen
        # distribution /= np.sum(distribution)  # normalize probability distribution
        
        # import math
        # _temp_distribution = []
        # for i in range(math.floor(len(distribution)/2)):
        #     _temp_distribution.append([distribution[i], distribution[i+1]])
        #     i+=1
        # distribution = _temp_distribution
        
        
        distribution = distribution.reshape(distribution.shape[-1])
        
        for i, move in enumerate(all_actions):
            if move not in legal_actions:
                distribution[i] = 0
                
                distribution /= np.sum(distribution) # Renormalize
                
        distribution= np.array(distribution)
        
        if sum(distribution.flatten()) <= 0:
            return random.choice(legal_actions)

        # distribution = [i/sum(distribution) for i in distribution]
           
        if random.uniform(0,1) < self.epsilon and do_random_move:
            # ind = distribution.tolist().index(random.choices(population=distribution, weights=distribution)[0])
            indices, = np.nonzero(distribution.flatten()) # Fungerer til nim
            # indices = np.transpose(np.nonzero(distribution)[0])
            ind = np.random.choice(indices)
            
        else:

            ind = np.argmax(distribution)
        
        return all_actions[ind]