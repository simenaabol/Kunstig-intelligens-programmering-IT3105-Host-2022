import numpy as np
import random

class Table_critic():
    def __init__(self, learning_rate, discount_factor, eligibility_decay):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.eligibility_decay = eligibility_decay
        self.eligibilites = {}
        self.value_table = {}

    def reset_eligibilites(self):
        """ 
        Resets the eligibilities for the table critic to 
        """
        self.eligibilites = {}

    def state_handler(self, state):
        raise NotImplementedError

    def set_initial_eligibility(self, state):
        
        """ Look for numpy arrays to strings """
        self.eligibilites[state] == 1

    def add_state_to_value_table(self, state):
        """ Initialize the state with a small, random value. """
        self.value_table[state] = random.uniform(0, 1)

    def calc_td_error(self, state, reward, next_state):
        
        if state not in self.value_table.keys():
            self.add_state_to_value_table(state)

        if next_state not in self.value_table(next_state):
            self.add_state_to_value_table(next_state)

        target_val = reward + (self.discount_factor * self.value_table[next_state])
        curr_state_val = self.value_table[state]
        td_error = target_val - curr_state_val

        return target_val, curr_state_val, td_error


    def update_eligibilities(self, state, current_state):

        if state == current_state:
            self.eligibilites[state] = 1
        else:
            self.eligibilites[state] *= self.discount_factor * self.eligibility_decay

    def update_values(self, state, td_error):

        if state not in self.value_table.keys():
            self.add_state_to_value_table(state)

        self.value_table[state] += self.learning_rate * td_error * self.eligibilites.get(state, 1)


    def update_eligibilities_and_values(self, episode_actions, td_error):
        
        for state, _, _ in episode_actions:
            self.update_eligibilities(state, episode_actions[-1][0])
            self.update_values(state, td_error)