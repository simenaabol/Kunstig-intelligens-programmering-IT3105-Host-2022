

class Network():

    def __init__(self):
        pass


class NN_critic():
    def __init__(self) -> None:
        pass

    def reset_eligibilites(self):
        raise NotImplementedError

    def calc_td_error(self, state, reward, next_state):
        raise NotImplementedError

    def update_weights(self, episode_actions, target_val, curr_state_val):
        raise NotImplementedError