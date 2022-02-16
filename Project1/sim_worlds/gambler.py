import random

class Gambler():
    def __init__(self, win_prob):
        """

        Class representing the Gambler problem.

        PARAMS: win probability

        """

        self.win_prob = win_prob
        self.coins = random.randint(1, 99)

        # For visualization
        self.vals_for_gambler = []


    def get_legal_moves(self):
        """

        Method for retrieving all legal moves for a state.

        RETURNS: legal moves

        """

        coin = self.coins
        moves = []

        if coin == 0:
            moves.append([-1])

        elif coin<51:
            for low_coin in range(coin):
                moves.append([low_coin + 1])

        else: # Coin > 51:
            for high_coin in range(100-coin):
                moves.append([high_coin + 1])  
        
        return moves

    def take_action(self, bet):
        """

        Method that does the action (bet), from the sim world.

        PARAMS: bet/action

        RETURNS

        """


        if self.win_prob > random.random():
            self.coins += bet[0]

        else:
            self.coins -= bet[0]
        

    def game_done(self):
        """

        Method for checking if the game is over or not.

        RETURNS: list with reward and bool

        """

        if self.coins == 100:
            return [1000, True]

        elif self.coins == 0:
            return [self.coins, True]

        else:
            return [-1, False]


    def get_state_key(self):
        """

        Method for returning the state of the game to the sim world

        RETURNS: a tuple with the amount of coins in a list

        """

        list = [self.coins]
        return tuple(list)


    def reset_game(self):
        """

        Method for reseting the game. Sets the coin to a random value between 1 and 99.

        """

        self.coins = random.randint(1, 99)


    def visualize(self, actor, _, __):
        """

        Method for visualizing the actor's policy, for the gambler problem.

        PARAMS: the actor
        RETURNS: list of x and y values, x label, y label

        """

        pol = actor.get_actor_policy()

        for act, value in pol.items():
            highest_val = float('-inf')
            picked_key = None

            for key, value2 in value.items():

                if value2 != 0:
                    if value2 > highest_val:
                        highest_val = value2
                        picked_key = key

            self.vals_for_gambler.append((act[0], picked_key[0]))

        self.vals_for_gambler.sort(key=lambda x: x[0])

        x_label = "State"
        y_label = "Wager"

        return self.vals_for_gambler, x_label, y_label, None