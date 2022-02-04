"""
On-policy RL -> policyen som brukes for søk gjennom states gjennom hver episode (behavior policy) er også policyen som systemet 
                bruker for å lære (target policy)

To insure a balance between exploration and exploitation, the actor should use its policy in an -greedy
manner (see actor-critic.pdf), where  is either a constant, user-supplied parameter, or a dynamic variable
that changes (i.e. decreases) from earlier to later episodes. By setting  = 0 at run’s end, the behavior policy
essentially becomes the target policy. By displaying one game played with this policy, the user sees the best
moves that the actor has found for the states of an episode.

The actor’s policy should be represented as a table (or Python dictionary) that maps state-action pairs (s,a)
to values that indicate the desirability of performing action a when in state s. For any state s, it is wise to
normalize the values across all legal actions from s, thus yielding a probability distribution over the possible
actions to take from s. The  greedy policy would then choose the action with the highest probability, or a
random value

parametere:

learning_rate
gamma
epsilon
goal_epsilon
eligibility_decay

"""

class Actor():
    def __init__(self, learning_rate, discount_factor, epsilon, eligibility_decay): # evt goal_epsilon og num_episodes
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.eligibility_decay = eligibility_decay

        
    def reset_eligibilites():
        raise NotImplementedError

    def get_action():
        raise NotImplementedError

    def state_handler(state, legal_moves):
        raise NotImplementedError

    def set_initial_eligibility(state, action):
        raise NotImplementedError