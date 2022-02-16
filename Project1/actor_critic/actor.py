import random

class Actor():
    def __init__(self, learning_rate, discount_factor, epsilon, epsilon_decay, eligibility_decay):
        """  

        Class representing the actor in the actor-critic architecture. Contains methods mostly
        used in the learner.

        PARAMS: learning rate, discount factor, epsilon, epsilon decay, and eligibility decay

        """

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.eligibility_decay = eligibility_decay

        self.eligibility_dict = {}
        self.policy_dict = {}


    def state_handler(self, state, legal_moves): # ISH
        """  

        Method for adding all states, and their legal moves into the actor's policy.

        PARAMS: state, legal moves

        """

        if state not in self.policy_dict.keys():
            self.policy_dict[state] = {}

            for action in legal_moves:
                action = tuple(action)
                self.policy_dict[state][action] = 0


    def reset_eligibilites(self): # ISH 
        """  

        Method for reseting the eligibilites for the actor. Sets the eligibility for
        the state, action pair to zero.

        """

        for state in self.eligibility_dict:
            for action in self.eligibility_dict[state]:
                self.eligibility_dict[state][action] = 0


    def set_initial_eligibility(self, state, action): # ISH
        """

        Method for setting the eligibilites to 1, before they are updated
        later on, as the learner progresses.

        PARAMS: state, action

        """

        action = tuple(action)

        if state not in self.eligibility_dict.keys():
            self.eligibility_dict[state] = {action: 1}

        else:
            self.eligibility_dict[state][action] = 1


    def get_action(self, state, legal_moves):
        """

        Method for retrieving an action for the learner to use. The three different
        kinds of actions this method returns are:

        - A random action if the state is not in the policy
        - A random action if a random number between 0 and 1 is less than epsilon.
        - A greedy action (usually when the epsilon is low) that takes the best action
        according to the actors' policy.

        PARAMS: state, legal moves
        RETURNS: the action chosen

        """

        # Not seen state -> random action
        if state not in self.policy_dict.keys():
            choice = random.choice(legal_moves)
            choice = tuple(choice)
            return choice

        # Seen state, but random value is less than epsilon -> random action
        if random.uniform(0, 1) < self.epsilon:

            # Choose an (random) action that has not been tried before
            for find_state in self.policy_dict.keys():
                if find_state == state:
                    for action in self.policy_dict[state]:
                        if self.policy_dict[state][action] == 0:
                                return action
            
            # If it can't find a new move, choose a random move from legal moves.
            choice = random.choice(legal_moves)
            choice = tuple(choice)

            return choice
                            
        # Picks a greedy action from the policy if it should not be random.
        greedy_action = None
        highest_val = float('-inf')

        for action, value in self.policy_dict[state].items():
            
            if value > highest_val and value != 0:
                highest_val = value
                greedy_action = action    

        if greedy_action == None:
            choice = random.choice(legal_moves)
            greedy_action = tuple(choice)
        
        return greedy_action


    def update_eligibilities_and_policy(self, episode_actions, td_error, current_state): # ISH
        """

        Method for calling the update methods for the eligibilites and policy.

        PARAMS: list of from_state and action, the temporal difference error, and the current state

        """

        for from_state, _, action in episode_actions:
            self.update_policy(from_state, action, td_error)
            self.update_eligibility_dict(from_state, action, current_state)


    def update_policy(self, state, action, td_error):
        """

        Method for updating the actors' policy depending on the learning rate, temporal
        difference error and the value already in the policy.

        PARAMS: state, action, temporal difference error

        """

        action = tuple(action)

        self.policy_dict[state][action] += self.learning_rate * td_error * self.eligibility_dict[state][action]


    def update_eligibility_dict(self, from_state, action, current_state):
        """

        Method for updating the eligibility dictionary.

        PARAMS: from state, action, and the current state

        """

        action = tuple(action)

        # If the from state is the current state, set the eligibility to 1
        if from_state == current_state:
            self.eligibility_dict[from_state][action] = 1
            #why this?

        # If not, set the eligibility to the formula below.
        else:
            self.eligibility_dict[from_state][action] *= self.discount_factor * self.eligibility_decay


    def update_epsilon(self, forced):
        """

        Method for updating the epsilon.

        """
        if forced == 0:
            self.epsilon = 0
        else:
            self.epsilon *= self.epsilon_decay


    def get_actor_policy(self):
        """

        Method used for visualizing the gambler problem, since it needs the actor's policy.

        """
        
        return self.policy_dict
