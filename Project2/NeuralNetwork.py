import numpy as np
import tensorflow as tf
import keras.layers as kerlayers
import keras.losses as klosses

class NeuralNet:
    def __init__(self, learning_rate, hidden_layer_size, activation_function, output_act, optimizer, loss_function):
        
        self.learning_rate = learning_rate
        self.hidden_layer_size = hidden_layer_size
        self.activation_function = activation_function
        self.optimizer = optimizer
        self.output_act = output_act
        self.loss_function = loss_function

    def init_model(self, state_manager):
        
        model = tf.keras.Sequential()

        input_size = state_manager.get_input_size()
        output_size = state_manager.get_output_size()
        
        # print(input_size)

        model.add(kerlayers.Input(shape=(input_size,)))

        for size in self.hidden_layer_size:
            model.add(kerlayers.Dense(size, activation=self.activation_function))

        """ FINN UT HVOR MANGE UNITS(=output) DENNE SKAL HA """
        
        model.add(kerlayers.Dense(units=output_size, activation=self.output_act))
        print('etter add: ', model)

        # Check for optimizer
        if self.optimizer == "adam":
            compiler_opt = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        elif self.optimizer == "rmsprop":
            compiler_opt = tf.keras.optimizers.RMSprop(learning_rate=self.learning_rate)
        elif self.optimizer == "sgd":
            compiler_opt = tf.keras.optimizers.SGD(learning_rate=self.learning_rate)
        else:
            compiler_opt = tf.keras.optimizers.Adagrad(learning_rate=self.learning_rate)
            
        # if self.loss_function == ""

        model.compile(optimizer=compiler_opt, loss=self.cross_entropy_loss)

        return model
    
    
    """ BLÅKOK """
    """ BÅDE SANDER OG THOMAS HAR KLISS LIK """
    def cross_entropy_loss(self, targets, outs):
        return tf.reduce_mean(tf.reduce_sum(-1 * targets * self.safelog(outs), axis=[1]))
 
    def safelog(self, tensor, base=0.0001):
        return tf.math.log(tf.math.maximum(tensor, base))