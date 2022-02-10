import random

class Gambler():
    def __init__(self, wP):
        self.wP = wP # win probability
        self.coins = random.randint(1, 99)

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
        wP = self.get_wP()
        coins = self.get_state()

        if wP>= random.random():
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
            return [0, True]
        else:
            return [-1, False]

    def get_wP(self): #get_win_probability
        return self.wP
    
    def update_coin(self, coin): #get_win_probability
        self.coins = coin
        
    def get_state_key(self):
        list = [self.coins]
        return tuple(list)
    
    def get_state(self):
        return self.coins

    def reset_game(self):
        self.coins = random.randint(1, 99)






B = Gambler(1.0)
print(B.get_wP())
# print('Du starter med kr:',B.get_state())
# print('Din vinnersannsynlighet er: ', B.get_wP())

#print(B.game_done())
# moves = B.get_legal_moves()
# B.take_action(random.choice(moves))


