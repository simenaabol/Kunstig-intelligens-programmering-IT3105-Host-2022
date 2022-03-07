

class ANET:
    def __init__(self) -> None:
        pass

    def save_net(self):
        raise NotImplementedError

    def update_epsilon(self):
        raise NotImplementedError

    def fit_network(self):
        raise NotImplementedError