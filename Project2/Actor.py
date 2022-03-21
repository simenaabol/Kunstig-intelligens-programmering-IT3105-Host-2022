from NeuralNetwork import NeuralNet

import numpy as np
import random
import tensorflow as tf

class ANET:
    def __init__(self, 
                 learning_rate, 
                 hidden_layer_size, 
                 activation_function, 
                 output_act, optimizer, 
                 loss_function, epsilon, 
                 epsilon_decay, 
                 state_manager):
        
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
        

    def save_net(self, name):        
        
        self.model.save("./NeuralNets/{name}".format(name=name))

    def update_epsilon(self, just_policy=False):
        
        self.epsilon *= self.epsilon_decay

        if just_policy:
            self.epsilon = 0

    def fit_network(self, x, y, epochs):
        
        self.model.fit(x, y, epochs)
        
    def get_action(self):
        legal_actions = self.state_manager.get_legal_moves()
        all_actions = self.state_manager.get_all_moves()
        state = tuple(self.state_manager.get_state())
        
        # print("STATE", state)
        
        #  distribution = self.state_manager.get_normalized_distribution()
        #  Hent fra selve nettverket ANN
        # distribution = self.ANET.predict_val(state).tolist()
        # print("TENSOR", tf.convert_to_tensor([state]))
        
        # Sander  -> dis til nettet, ikke hex
        distribution = self.model(tf.convert_to_tensor([state])).numpy()  # type: ignore
        distribution = distribution * np.array(legal_actions)
        distribution = distribution.flatten()
        distribution /= np.sum(distribution)  # normalize probability distribution
        
        # print(distribution)
        
        
        
        
        
        
        
        # Sander
        
        for i, move in enumerate(all_actions):
            if move not in legal_actions:
                distribution[i] = 0

        if sum(distribution) <= 0:
            return random.choice(legal_actions)

        # distribution = [i/sum(distribution) for i in distribution]
           
        if random.uniform(0,1) < self.epsilon:
            ind = distribution.tolist().index(random.choices(population=distribution, weights=distribution)[0])
        else:
            ind = distribution.tolist().index(np.argmax(distribution))
            
        return all_actions[ind]
        
        
        
        

    # """ MEGA DANGER ZONE """
    # def get_action(self, state, player): # BRUKES I MCTS
        
    #     probability_distribution = self.get_actor_policy(state, player)
    #     print("ETTER GET", probability_distribution)
    #     probability_distribution = self.remove_illegal_moves_from_dist(probability_distribution, state)
    #     print("ETTER REMOVE", probability_distribution)
        
    #     action = np.unravel_index(np.argmax(probability_distribution), self.state_manager.get_state().shape)
        
    #     if self.epsilon > np.random.random():
            
    #         indices = np.random.choice(
    #             a=np.arange(len(probability_distribution)),
    #             p=probability_distribution
    #         )
            
    #         action = np.unravel_index(indices, self.state_manager.get_state().shape)
            
    #     return action
        
    # """ DANGER ZONE """
    # def get_actor_policy(self, state, player):
        
    #     var = np.concatenate(([player], state), axis=None)
    #     print("ETTER CONCAT", var)
    #     var = var.reshape((1,) + var.shape)
    #     print("ETTER RESHAPE", var)
        
    #     action_prob_arr = self.model(var)
    #     print("ETTER self.model(var)", action_prob_arr)
    #     action_prob_arr = action_prob_arr.numpy()
    #     print("ETTER NUMPY", action_prob_arr)
    #     action_prob_arr = action_prob_arr.reshape(action_prob_arr.shape[-1])
    #     print("SISTE", action_prob_arr)
        
    #     return action_prob_arr

    # """ MER DANGER ZONE """
    # def remove_illegal_moves_from_dist(self, probability_distribution, state):
        
    #     print("BEFORE", probability_distribution)
        
    #     for i in range(len(probability_distribution)):
    #         action = np.unravel_index(i, self.state_manager.get_state().shape)
            
    #         print()
    #         print("FOR", probability_distribution)
    #         print("ACTION", action)
    #         print("I", i, "SHAPE", self.state_manager.get_state().shape)
    #         print()
            
    #         if not self.state_manager.check_if_legal_action(state, action):
    #             probability_distribution[i] = 0
    #             print("ETTER REMOVE 1", probability_distribution, probability_distribution.sum())
    #             print(probability_distribution.sum())
    #             probability_distribution = probability_distribution / probability_distribution.sum()
                
    #     return probability_distribution

    