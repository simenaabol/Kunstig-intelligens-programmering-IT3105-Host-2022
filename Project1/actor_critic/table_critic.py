import random

class Table_critic():
    def __init__(self, learning_rate, discount_factor, eligibility_decay):
        """

        Class representing the table critic in the actor-critic architecture. Contains methods
        for evauluation of actions performed by the actor. In addition to methods for updating
        eligibilites and the critics value dictionary.

        PARAMS: learning rate, discount factor, eligibility decay

        """

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.eligibility_decay = eligibility_decay

        self.eligibility_dict = {}
        self.value_dict = {}


    def state_handler(self, from_state):
        """

        Method for adding the states into the value dictionary if they have not 
        been seen, and assigning them a small, random value.

        PARAMS: from_state

        """

        if from_state not in self.value_dict.keys():
            self.value_dict[from_state] = random.uniform(0, 1)


    def reset_eligibilites(self):
        """

        Method for reseting the eligibilities for the critic. Sets the eligibilites
        to zero.

        """
        
        for state in self.eligibility_dict: 
            self.eligibility_dict[state] = 0


    def set_initial_eligibility(self, state):
        """

        Method for setting the eligibilites to 1, before they are updated
        later on, as the learner progresses.   

        PARAMS: state     

        """
        
        self.eligibility_dict[state] = 1


    def calc_td_error(self, from_state, reward, current_state):
        """

        Method for calculating the temporal difference error to be used for updating
        values later on.

        PARAMS: from state, reward, current state
        RETURNS: temporal difference error

        """
        
        if from_state not in self.value_dict.keys():
            self.add_state_to_value_dict(from_state)

        if current_state not in self.value_dict.keys():
            self.add_state_to_value_dict(current_state)

        # The reward plus the discounted future value state
        target_val = reward + (self.discount_factor * self.value_dict[current_state])

        # The current state value
        curr_state_val = self.value_dict[from_state]

        # Temporal difference error
        td_error = target_val - curr_state_val

        return td_error


    def update_eligibilities_and_values(self, episode_actions, td_error):
        """

        Method for calling the update methods for the eligibilites and value table.

        PARAMS: list of from states, temporal difference error

        """
        
        for from_state, _, _ in episode_actions:
            self.update_value_dict(from_state, td_error)
            self.update_eligibility_dict(from_state, episode_actions[-1][0])


    def update_eligibility_dict(self, from_state, current_state):
        """

        Method for updating the eligibility dictionary.

        PARAMS: from state, and the current state

        """

        # If the from state is the current state, set the eligibility to 1
        if from_state == current_state:
            self.eligibility_dict[from_state] = 1

        # If not, set the eligibility to the formula below.
        else:
            self.eligibility_dict[from_state] *= self.discount_factor * self.eligibility_decay


    def update_value_dict(self, from_state, td_error):
        """

        Method for updating the value dictionary depending on the learning rate, temporal
        difference error and the existing value in the dictionary.

        PARAMS: from_state, temporal difference error

        """

        if from_state not in self.value_dict.keys():
            self.add_state_to_value_dict(from_state)

        self.value_dict[from_state] += self.learning_rate * td_error * self.eligibility_dict.get(from_state)


    def add_state_to_value_dict(self, state):
        """ 

        Helping method for initializing the from_state in the value dictionary with a small,
        random value.

        PARAMS: state

        """

        self.value_dict[state] = random.uniform(0, 1)