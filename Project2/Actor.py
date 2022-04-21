from NeuralNetwork import NeuralNet

import numpy as np
import random
import tensorflow as tf
from Parameters import config

class ANET:
    def __init__(self,
                 model, 
                 learning_rate, 
                 hidden_layers, 
                 activation_function, 
                 output_act, optimizer, 
                 epsilon, 
                 epsilon_decay, 
                 state_manager):
        
        """Class for the Actor

        Args:
            model (tensorflow model): If Topp is ran, then the model is passed into the actor
            learning_rate (float): Learning rate for the neural net
            hidden_layers (tuple): The size of each hidden layer
            activation_function (string): The activation function for the hidden layers
            output_act (string): The activation function for the output layer
            optimizer (string): The optimizer used for compiling the network
            epsilon (int/float): The epsilon used in the run
            epsilon_decay (int/float): The decay rate for the epsilon each run
            state_manager (object): The state manager object
        """        
        
        # Set model to the model given
        if model:
            self.model = model
            
        # Initialize a neural network
        else:
            self.net = NeuralNet(learning_rate, 
                                hidden_layers, 
                                activation_function,
                                output_act, 
                                optimizer)

            self.model = self.net.init_model(state_manager)

        self.state_manager = state_manager
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        
        self.gameconfig = state_manager.get_parameters()
        
    def save_net(self, name):
        """Method for saving the neural net

        Args:
            name (string): Folder name for the net
        """        
        
        self.model.save("Project2/TrainedNets/{folder}/{name}".format(name=name, folder=config['network_folder_name']))
        
    def get_model(self):
        """Method for returning the model

        Returns:
            tensorflow model: The model from the Actor
        """        
        
        return self.model

    def update_epsilon(self, just_policy=False):
        """Method for updating the epsilon

        Args:
            just_policy (bool, optional): If we want to run purely greedy from the policy. Defaults to False.
        """        
        
        self.epsilon *= self.epsilon_decay

        if just_policy:
            self.epsilon = 0

    def fit_network(self, x, y, epochs):
        """Method for training the network

        Args:
            x (numpy array): The training features
            y (numpy array): The target features
            epochs (int): How many epochs to run
        """        
        
        self.model.fit(x=x, y=y, epochs=epochs, batch_size=self.gameconfig['actor_config']['anet_batch_size'])
        
    def get_action(self, lite_model, state, player, do_random_move=True):
        #  Mulig med false  for lite_model
        """Method for retrieving an action from the network

        Args:
            lite_model (lite_model object): The lite model from BB
            state (numpy array): The state to retrieve an action from
            player (int): Which players' turn it is
            do_random_move (bool, optional): If we will allow random moves. Defaults to True.

        Returns:
            tuple: An action from the action distribution depending on the default policy 
        """        
        
        legal_actions = self.state_manager.get_legal_moves(state)
        all_actions = self.state_manager.get_all_moves()
        
        # Concat the player with the state to represent the input to the network
        state_for_model = np.concatenate(([player], state), axis=None)
        
        # If we want to use the lite_model or not
        if lite_model:
            distribution = lite_model.predict_single(state_for_model)
        else:
            state_for_model = tf.cast(tf.convert_to_tensor([state_for_model]), dtype=tf.float32)
            distribution = self.model(state_for_model).numpy() # Får feil her
        
        distribution = distribution.reshape(distribution.shape[-1])
          
        # Remove the illegal actions, and renormalize the action distribution
        for i, move in enumerate(all_actions):
            if move not in legal_actions:
                distribution[i] = 0
                
                distribution /= np.sum(distribution) # Renormalize
                
        distribution = np.array(distribution)
        
        if sum(distribution.flatten()) <= 0:
            return random.choice(legal_actions)
           
        # The default policy:
        # - Do random if epsilon is below a random float between 0 and 1
        # - Else do the best move from the distribution
        if random.uniform(0,1) < self.epsilon and do_random_move:
            indices, = np.nonzero(distribution.flatten())
            ind = np.random.choice(indices)
        else:
            ind = np.argmax(distribution)
        
        return all_actions[ind]
    
    
    def get_action2(self, lite_model, state, do_random_move=True):
        #  Mulig med false  for lite_model
        """Method for retrieving an action from the network

        Args:
            lite_model (lite_model object): The lite model from BB
            state (numpy array): The state to retrieve an action from
            player (int): Which players' turn it is
            do_random_move (bool, optional): If we will allow random moves. Defaults to True.

        Returns:
            tuple: An action from the action distribution depending on the default policy 
        """        
        
        if np.count_nonzero(state == 1) > np.count_nonzero(state == 2):
            player = 2
        else:
            player = 1
        
        legal_actions = self.state_manager.get_legal_moves(state)
        all_actions = self.state_manager.get_all_moves()
        
        # Concat the player with the state to represent the input to the network
        state_for_model = np.concatenate(([player], state), axis=None)
        
        # If we want to use the lite_model or not
        if lite_model:
            distribution = lite_model.predict_single(state_for_model)
        else:
            state_for_model = tf.cast(tf.convert_to_tensor([state_for_model]), dtype=tf.float32)
            distribution = self.model(state_for_model).numpy()
        
        distribution = distribution.reshape(distribution.shape[-1])
          
        # Remove the illegal actions, and renormalize the action distribution
        for i, move in enumerate(all_actions):
            if move not in legal_actions:
                distribution[i] = 0
                
                distribution /= np.sum(distribution) # Renormalize
                
        distribution = np.array(distribution)
        
        if sum(distribution.flatten()) <= 0:
            return random.choice(legal_actions)
           
        # The default policy:
        # - Do random if epsilon is below a random float between 0 and 1
        # - Else do the best move from the distribution
        if random.uniform(0,1) < self.epsilon and do_random_move:
            indices, = np.nonzero(distribution.flatten())
            ind = np.random.choice(indices)
        else:
            ind = np.argmax(distribution)
            
        # print("0", all_actions[ind][0], "1", all_actions[ind][1])
        
        # print(distribution)
        
        # # print("action", all_actions[ind])
        # print("all actions", all_actions)
        # print("index", ind)
        
        return all_actions[ind][0], all_actions[ind][1]