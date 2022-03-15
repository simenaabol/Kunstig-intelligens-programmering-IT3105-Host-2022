from NeuralNetwork import NeuralNet

import numpy as np

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

    """ MEGA DANGER ZONE """
    def get_action(self, state, player): # BRUKES I MCTS
        
        probability_distribution = self.get_actor_policy(state, player)
        print("ETTER GET", probability_distribution)
        probability_distribution = self.remove_illegal_moves_from_dist(probability_distribution, state)
        print("ETTER REMOVE", probability_distribution)
        
        action = np.unravel_index(np.argmax(probability_distribution), self.state_manager.get_state().shape)
        
        if self.epsilon > np.random.random():
            
            indices = np.random.choice(
                a=np.arange(len(probability_distribution)),
                p=probability_distribution
            )
            
            action = np.unravel_index(indices, self.state_manager.get_state().shape)
            
        return action
        
    """ DANGER ZONE """
    def get_actor_policy(self, state, player):
        
        var = np.concatenate(([player], state), axis=None)
        var = var.reshape((1,) + var.shape)
        
        action_prob_arr = self.model(var)
        action_prob_arr = action_prob_arr.numpy()
        action_prob_arr = action_prob_arr.reshape(action_prob_arr.shape[-1])
        
        return action_prob_arr

    """ MER DANGER ZONE """
    def remove_illegal_moves_from_dist(self, probability_distribution, state):
        
        print("BEFORE", probability_distribution)
        
        for i in range(len(probability_distribution)):
            action = np.unravel_index(i, self.state_manager.get_state().shape)
            
            print()
            print("FOR", probability_distribution)
            print("ACTION", action)
            print()
            
            if not self.state_manager.check_if_legal_action(state, action):
                probability_distribution[i] = 0
                probability_distribution = probability_distribution / probability_distribution.sum()
                
        return probability_distribution

    