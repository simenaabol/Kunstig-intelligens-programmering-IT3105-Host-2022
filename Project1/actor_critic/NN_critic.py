import numpy as np
import tensorflow as tf
import keras
import keras.layers as klayers
import keras.optimizers as optimizer
import keras.losses as losses

class NN_critic():

    def __init__(self, learning_rate, discount_factor, input_size, hidden_layers_size):

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.input_size = input_size
        self.hidden_layer_size = hidden_layers_size

        self.model = keras.Sequential()

        self.model.add(keras.Input(shape=self.input_size))

        for size in self.hidden_layer_size:
            self.model.add(klayers.Dense(size, activation='relu'))

        self.model.add(klayers.Dense(1))

        self.model.compile(optimizer=optimizer.adam_v2(learning_rate=self.learning_rate), 
                            loss=losses.MeanSquaredError())


    def calc_td_error(self, state, reward, next_state):

        target_val = reward + self.discount_factor * self.model.predict([next_state], batch_size=1)
        curr_state_val = self.model.predict([state], batch_size=1)
        td_error = target_val - curr_state_val

        return target_val, curr_state_val, td_error

    def update_weights(self, episode_actions, target_val, curr_state_val):
        raise NotImplementedError