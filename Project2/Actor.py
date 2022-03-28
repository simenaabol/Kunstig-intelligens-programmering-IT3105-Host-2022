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
        
        # print("X", x)
        # print("Y", y)
        # print("EPO", epochs)
        
        # print(self.state_manager.get_input_size())
        
        self.model.fit(x=x, y=y, epochs=epochs)
        
    def get_action(self, leaf, player):
        legal_actions = self.state_manager.get_legal_moves(leaf)
        all_actions = self.state_manager.get_all_moves()
        
        state = np.array(self.state_manager.get_state()) # Litt usikker på denne
        # state = tuple(self.state_manager.get_state())
        
        state_for_model = np.concatenate(([player], state.flatten()), axis=None)
        # print("SFM", state_for_model)
        
        # print("STATE", state)
        
        #  distribution = self.state_manager.get_normalized_distribution()
        #  Hent fra selve nettverket ANN
        # distribution = self.ANET.predict_val(state).tolist()
        # print("TENSOR", tf.convert_to_tensor([state]))
        
        # Sander  -> dis til nettet, ikke hex
        distribution = self.model(tf.convert_to_tensor([state_for_model])).numpy()  # type: ignore - > error: raise e.with_traceback(filtered_tb) from None: ValueError: Input 0 of layer "sequential" is incompatible with the layer: expected shape=(None, 25), found shape=(1, 5, 5)
        distribution = distribution * np.array(all_actions)
        distribution = distribution.flatten()
        distribution /= np.sum(distribution)  # normalize probability distribution
        
        # print(distribution)
        
        
        # Sander
        
        # print("FØR FOR LØKKE LEGAL ACTIONS:", legal_actions)
        
        for i, move in enumerate(all_actions):
            # print("MOVES SOM SJEKKES MOT LEGAL ACTIONS:", move)
            if move not in legal_actions:
                # print("KOMMER VI NOEN GANGER HER???", distribution)
                distribution[i] = 0
                
                distribution /= np.sum(distribution) # Renormalize

        if sum(distribution) <= 0:
            # print("GET ACTION RANDOM FRA DISSE ACTIONSENE (SUM):", legal_actions)
            return random.choice(legal_actions)

        # distribution = [i/sum(distribution) for i in distribution]
           
        if random.uniform(0,1) < self.epsilon:
            """ EVENTUELT GJØR OM TIL NP """
            # ind = distribution.tolist().index(random.choices(population=distribution, weights=distribution)[0])
            indices, = np.nonzero(distribution)
            ind = np.random.choice(indices)
            # print("GET ACTION RANDOM (VANLIG RANDOM):", ind)
            
            """ KANSKJE ENDRE EPSILON HER """
            
        else:
            ind = np.argmax(distribution)
            # print("GET ACTION IKKE RANDOM:", ind)
            
        # print("SLUTT DISTRIBUTION", distribution)
        # print("VALGTE ACTION FRA GET ACTION", all_actions[ind])
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

    