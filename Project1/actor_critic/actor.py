import random

class Actor():
    def __init__(self, learning_rate, discount_factor, epsilon, epsilon_decay, eligibility_decay): # evt goal_epsilon og num_episodes
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.eligibility_decay = eligibility_decay
        self.eligibilities = {}
        self.policy = {}

        
    def state_handler(self, state, legal_moves):
        if state not in self.policy.keys():
            self.policy[state] = {}
            for move in legal_moves:
                self.policy[state][move] = 0

    def reset_eligibilites(self):
        """ 
        Resets the eligibilities for the actor policy to 0
        """
        self.eligibilities = {}

    def get_action(self, state, legal_moves):

        if state not in self.policy.keys():
            # print('Legal: ', legal_moves)
            choice = random.choice(legal_moves)
            choice = tuple(choice)
            self.policy[state] = {}
            return choice

        elif random.uniform(0, 1) < self.epsilon:
            return tuple(random.choice(legal_moves))

        greedy_action = None
        highest_val = float('-inf')

        """ THIS ELSE IS SHIT I THINK """
        for action, value in self.policy[state].items():
            print('Action: ', action)
            
            if value > highest_val and value != 0:
                highest_val = value
                greedy_action = action
                print('oppe')

            # else:
                # print('nede')
                # greedy_action = random.choice(legal_moves)
        print('hæhhæ', self.policy[state].items())
        greedy_action = max(self.policy[state].items(), key=lambda x: x[0])[0] if greedy_action is None else greedy_action
        return greedy_action


    def set_initial_eligibility(self, state, action):
        action = tuple(action)
        self.eligibilities[state] = {action: 1}


    def update_policy(self, state, action, td_error):

        action = tuple(action)

        if state not in self.policy.keys():

            self.policy[state] = {
                action: 0
            }

        if self.policy[state].get(action) is None:

            self.policy[state] = {
                action: 0
            }


        """ Try to change this one """
        # self.policy[state][action] += self.learning_rate * td_error * self.eligibilities[state][action]

        """ Denne linja er 100% koka """
        self.policy[state][action] = self.policy[state].get(action, 0) + self.learning_rate * td_error * self.eligibilities.get(state, {}).get(action, 1)

    def update_eligibilities(self, state, action, current_state):
        action = tuple(action)

        if state == current_state:
            self.eligibilities[state][action] = 1
        else:
            self.eligibilities[state][action] *= self.discount_factor * self.eligibility_decay


    def update_eligibilities_and_policy(self, episode_actions, td_error, current_state):

        for state, _, action in episode_actions:
            self.update_policy(state, action, td_error)
            self.update_eligibilities(state, action, current_state)

    def update_epsilon(self):
        self.epsilon *= self.epsilon_decay