import random

class Gambler():
    def __init__(self, win_prob):
        self.win_prob = win_prob # win probability
        self.coins = random.randint(1, 99)

        self.vals_for_gambler = []

    def get_legal_moves(self):
        coin = self.get_state()
        moves = []

        if coin == 0:
            moves.append([-1])

        elif coin<51:
            for lCoin in range(coin):
                moves.append([lCoin+1])

        else: # coin>51:
            for hCoin in range(100-coin):
                moves.append([hCoin+1])
                
        
        return moves

    def take_action(self, bet):
        # print('BET:', bet)
        # print('Ditt bet',bet[0])
        win_prob = self.get_win_prob()
        coins = self.get_state()

        if win_prob>= random.random():
            coins+=bet[0]
            # print('Du vant betten din!:)')
        else:
            coins-=bet[0]
            # print('Du tapte betten din:(')
        self.update_coin(coins)
        return None
        

    def game_done(self):
        if self.get_state() == 100:
            return [1000, True]
        elif self.get_state() == 0:
            return [self.coins, True]
        else:
            return [-1, False]

    def get_win_prob(self): #get_win_probability
        return self.win_prob
    
    def update_coin(self, coin): #get_win_probability
        self.coins = coin
        
    def get_state_key(self):
        list = [self.coins]
        return tuple(list)
    
    def get_state(self):
        return self.coins

    def reset_game(self):
        self.coins = random.randint(1, 99)


    def visualize(self, actor, _, __):

        pol = actor.get_actor_policy()

        for act, value in pol.items():
            # print("act", value)
            highest_val = float('-inf')
            picked_key = None
            for key, value2 in value.items():
                # print(value2)
                if value2 != 0:
                    if value2 > highest_val:
                        highest_val = value2
                        picked_key = key

            self.vals_for_gambler.append((act[0], picked_key[0]))

        self.vals_for_gambler.sort(key=lambda x: x[0])

        x_label = "State"
        y_label = "Wager"

        return self.vals_for_gambler, x_label, y_label, None