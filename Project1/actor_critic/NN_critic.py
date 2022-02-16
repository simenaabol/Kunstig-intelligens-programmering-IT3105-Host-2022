import numpy as np
import tensorflow as tf
import keras.layers as klayers
import keras.losses as losses


class NN_critic():

    def __init__(self, learning_rate, discount_factor, input_size, hidden_layers):
        """

        Class representing the neural network critic.

        PARAMS: learning rate, discount factor, input size, hidden layers

        """

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.input_size = input_size
        self.hidden_layer_size = hidden_layers

        self.model = tf.keras.Sequential()

        self.model.add(tf.keras.Input(shape=self.input_size))

        for size in self.hidden_layer_size:
            self.model.add(klayers.Dense(size, activation='relu'))

        self.model.add(klayers.Dense(1))

        self.model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=self.learning_rate), 
                            loss=losses.MeanSquaredError())


    def calc_td_error(self, from_state, reward, current_state):
        """

        Method for calculating the temporal difference error.

        PARAMS: from state, reward, current state
        RETURNS: temporal difference error

        """

        target_val = reward + self.discount_factor * self.state_value(current_state)
        from_state_val = self.state_value(from_state)

        td_error = target_val - from_state_val

        return td_error


    def state_value(self, state):
        """

        Method for using tensors to help evaluate the td_error

        PARAMS: state
        RETURNS: float

        """

        # Try this code to use if the state is multiple elements
        try:
            state = [list(i) for i in state]

            max_len = float('-inf')

            for i in state:

                if len(i) != 0:
                    if max_len < max(i):
                        max_len = max(i)

            for i in state:
                if len(i) != max_len:
                    for j in range(max_len):
                        if len(i) != max_len:
                            i.append(0)

            state = np.asarray([np.asarray(i) for i in state])

        except:

            state = np.asarray(state)

        state = tf.convert_to_tensor(state)

        return self.model(state).numpy()[0][0]


    def update_weights(self, td_error):
        """

        Method for recompiling the neural network using the new loss function as td_error squared.

        PARAMS: temporal difference error

        """

        loss_func = td_error ** 2

        self.model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=self.learning_rate), 
                            loss=loss_func)
