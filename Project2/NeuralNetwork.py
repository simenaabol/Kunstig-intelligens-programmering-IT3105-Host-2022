import numpy as np
import tensorflow as tf
import keras.layers as kerlayers
import keras.losses as klosses

class NeuralNet:
    def __init__(self, learning_rate, hidden_layer_size, activation_function, output_act, optimizer):
        
        self.learning_rate = learning_rate
        self.hidden_layer_size = hidden_layer_size
        self.activation_function = activation_function
        self.optimizer = optimizer
        self.output_act = output_act

    def init_model(self, state_manager):
        
        model = tf.keras.Sequential()

        input_size = state_manager.get_input_size()
        output_size = state_manager.get_output_size()

        model.add(kerlayers.Input(shape=(input_size,)))

        for size in self.hidden_layer_size:
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

        model.compile(optimizer=compiler_opt, loss=cross_entropy_loss)

        return model
    
""" EVENTUELT KJØRE EN STANDARD LOSS FUNCTION FOR Å UNNGÅ DETTE """
def cross_entropy_loss(targets, outs):
    return tf.reduce_mean(tf.reduce_sum(-1 * targets * safelog(outs), axis=[1]))

def safelog(tensor, base=0.0001):
    return tf.math.log(tf.math.maximum(tensor, base))
    