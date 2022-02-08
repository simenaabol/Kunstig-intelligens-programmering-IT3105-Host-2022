import random

class Actor():
    def __init__(self, learning_rate, discount_factor, epsilon, eligibility_decay): # evt goal_epsilon og num_episodes
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.eligibility_decay = eligibility_decay
        self.eligibilities = {}
        self.policy = {}

        
    def state_handler(self, state, legal_moves):
        raise NotImplementedError

    def reset_eligibilites(self):
        """ 
        Resets the eligibilities for the actor policy to 0
        """
        self.eligibilities = {}

    def get_action(self, state, legal_moves=[]):

        if state not in self.policy.keys():
            return random.choice(legal_moves)

        elif random.uniform(0, 1) < self.epsilon:

            return random.choice(list(self.policy[state].keys()))

        greedy_action = None
        highest_val = float('-inf')

        for action, value in self.policy[state].items():
            
            if value > highest_val and value != 0:
                highest_val = value
                greedy_action = action

        return greedy_action


    def set_initial_eligibility(self, state, action):
        
        """ Look for numpy arrays to strings """
        self.eligibilities[state][action] == 1

    def update_policy(self, state, action, td_error):

        if state not in self.policy.keys():

            self.policy[state] = {
                action: 0
            }

        """ Try to change this one """
        self.policy[state][action] = self.policy[state].get(action) \
                                    + self.learning_rate * td_error \
                                    * self.eligibilities[state].get(action)

    def update_eligibilities(self, state, action, current_state):

        if state == current_state:
            self.eligibilities[state][action] = 1
        else:
            self.eligibilities[state][action] *= self.discount_factor * self.eligibility_decay


    def update_eligibilities_and_policy(self, episode_actions, td_error, current_state):

        for state, _, action in episode_actions:
            self.update_policy(state, action, td_error)
            self.update_eligibilities(state, action, current_state)

    def update_epsilon(self):
        raise NotImplementedError