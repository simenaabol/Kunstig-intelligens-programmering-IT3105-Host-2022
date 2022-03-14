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
        

    def save_net(self, name):
        
        self.model.save("./NeuralNets/{name}".format(episode=name))

    def update_epsilon(self, just_policy=False):
        
        self.epsilon *= self.epsilon_decay

        if just_policy:
            self.epsilon = 0

    def fit_network(self, x, y, epochs):
        
        self.model.fit(x, y, epochs)