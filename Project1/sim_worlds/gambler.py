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
        print('Ditt bet',bet[0])
        wP = self.get_wP()
        coins = self.get_state()

        if wP>= random.random():
            coins+=bet[0]
            print('Du vant betten din!:)')
        else:
            coins-=bet[0]
            print('Du tapte betten din:(')
        self.update_coin(coins)
        return None
        

    def game_done(self):
        if self.get_state() == 1000:
            return [True, 1]
        elif self.get_state() == 0:
            return [True, 0]
        else:
            return [False, -1]

    def get_wP(self): #get_win_probability
        return self.wP
    
    def update_coin(self, coin): #get_win_probability
        self.coins = coin
        
    def get_state(self):
        return self.coins

    def get_reward(self):
        coin = self.get_state()

        if coin != 100:
            return coin
        else:
            return 1000




# B = Gambler(0.5)
# #print(B.get_wP())
# print('Du starter med kr:',B.get_state())
# print('Din vinnersannsynlighet er: ', B.get_wP())

# #print(B.game_done())
# moves = B.get_legal_moves()
# B.take_action(random.choice(moves))
# print(B.get_state())
# print(B.get_state())
# print(B.game_done())
