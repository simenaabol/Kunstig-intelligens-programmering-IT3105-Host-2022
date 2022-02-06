"""
Your system must provide two different implementations for the critic: a simple table of assocations (e.g.,
Python dictionary) between states and values, and a neural network that maps states to values.
The neural network must be implemented in one of the standard deep-learning packages, such as Tensorflow
or PyTorch. See the section entitled Function Approximators in the Critic in actor-critic.pdf for details of
this implementation.

"""

class NN_critic():
    def __init__(self) -> None:
        pass

    def reset_eligibilites(self):
        raise NotImplementedError

    def calc_td_error(self, state, reward, next_state):
        raise NotImplementedError

    def update_weights(self, episode_actions, target_val, curr_state_val):
        raise NotImplementedError