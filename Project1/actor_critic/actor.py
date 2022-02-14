import random
import matplotlib.pyplot as plt

class Actor():
    def __init__(self, learning_rate, discount_factor, epsilon, epsilon_decay, eligibility_decay):
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
                move = tuple(move)
                self.policy[state][move] = 0

    def reset_eligibilites(self):

        """ VELDIG LIKT, EVT SE PÅ ELIG = {} """
        """ DANGER ZONE """
        for state in self.eligibilities:
            for action in self.eligibilities[state]:
                self.eligibilities[state][action] = 0

    def get_action(self, state, legal_moves):


        # print(self.policy.keys())
        # Gir alle states som actor har sett. 

        # Gjør noe random hvis man ikke har sett staten
        if state not in self.policy.keys():
            choice = random.choice(legal_moves)
            choice = tuple(choice)
            return choice

        #Har ikke sett staten før, men velger å gjøre et ???
        if random.uniform(0, 1) < self.epsilon:

            """ DANGER ZONE """
            # print('self.policy[state].items()', self.policy[state].items())
            # Gir ut alle actions med en verdi bak. Verdien er hvor bra trekket er


            # print('self.policy[state].', self.policy[state])
            # Her så veit vi at state ligger i self.policy.keys():

            # Gjør et move som ikke er gjort før, hvis alle er testet, gjør noe random

            for find_state in self.policy.keys():
                if find_state == state:
                    for action in self.policy[state]:
                        if self.policy[state][action] == 0:
                                return action
                
            choice = random.choice(legal_moves)
            choice = tuple(choice)
            return choice
                            
           
        greedy_action = None
        highest_val = float('-inf')

        for action, value in self.policy[state].items():
            
            if value > highest_val and value != 0:
                highest_val = value
                greedy_action = action

        """ DANGER ZONE """
        greedy_action = max(self.policy[state].items(), key=lambda x: x[0])[0] if greedy_action is None else greedy_action
        return greedy_action

    """ DANGER ZONE """
    def set_initial_eligibility(self, state, action):
        action = tuple(action)
        if state not in self.eligibilities.keys():
            
            self.eligibilities[state] = {action: 1}

        else:

            self.eligibilities[state][action] = 1


    def update_policy(self, state, action, td_error):

        action = tuple(action)

        """ DANGER ZONE ish """
        if state not in self.policy.keys():

            self.policy[state] = {
                action: 0
            }

        if self.policy[state].get(action) is None:

            self.policy[state] = {
                action: 0
            }


        """ DANGER ZONE """
        self.policy[state][action] += self.learning_rate * td_error * self.eligibilities[state][action]

    def update_eligibilities(self, state, action, current_state):
        action = tuple(action)

        """ DANGER ZONE ish """
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

        # print("EPS", self.epsilon)

    def get_actor_policy(self):
        
        return self.policy
