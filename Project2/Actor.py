from NeuralNetwork import NeuralNet

class ANET:
    def __init__(self, learning_rate, hidden_layer_size, activation_function, output_act, optimizer, loss_function, epsilon, epsilon_decay, state_manager):
        
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


    def save_net(self):
        raise NotImplementedError

    def update_epsilon(self):
        raise NotImplementedError

    def fit_network(self):
        raise NotImplementedError