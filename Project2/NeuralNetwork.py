import tensorflow as tf
import keras.layers as kerlayers

class NeuralNet:
    def __init__(self, learning_rate, hidden_layers, activation_function, output_act, optimizer):
        """Class for the neural nets created

        Args:
            learning_rate (float): Learning rate for the neural net
            hidden_layers (tuple): The size of each hidden layer
            activation_function (string): The activation function for the hidden layers
            output_act (string): The activation function for the output layer
            optimizer (string): The optimizer used for compiling the network
        """        
        
        self.learning_rate = learning_rate
        self.hidden_layers = hidden_layers
        self.activation_function = activation_function
        self.optimizer = optimizer
        self.output_act = output_act

    def init_model(self, state_manager): 
        """Method for initalizing the network

        Args:
            state_manager (state manager object): Used to get input and output size

        Raises:
            ValueError: If wrong optimizer is chosen from the parameters

        Returns:
            tensorflow model: Tensorflow model with the neural net
        """        
        
        model = tf.keras.Sequential()

        input_size = state_manager.get_input_size()
        output_size = state_manager.get_output_size()

        model.add(kerlayers.Input(shape=(input_size,)))

        for size in self.hidden_layers:
            model.add(kerlayers.Dense(size, activation=self.activation_function))
        
        model.add(kerlayers.Dense(units=output_size, activation=self.output_act))

        # Check for optimizer
        if self.optimizer == "adam":
            compiler_opt = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        elif self.optimizer == "rmsprop":
            compiler_opt = tf.keras.optimizers.RMSprop(learning_rate=self.learning_rate)
        elif self.optimizer == "sgd":
            compiler_opt = tf.keras.optimizers.SGD(learning_rate=self.learning_rate)
        elif self.optimizer == "adagrad":
            compiler_opt = tf.keras.optimizers.Adagrad(learning_rate=self.learning_rate)
        else:
            raise ValueError("Choose a different optimizer!")

        model.compile(optimizer=compiler_opt, loss=custom_cross_entropy)

        return model
    
    
# Custom cross entropy function found online
def custom_cross_entropy(targets, outs):
    return tf.reduce_mean(tf.reduce_sum(-1 * targets * safelog(outs), axis=[1]))

def safelog(tensor, base=0.0001):
    return tf.math.log(tf.math.maximum(tensor, base))
    