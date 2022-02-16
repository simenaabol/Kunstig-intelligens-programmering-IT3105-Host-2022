import random
import math
import matplotlib.pyplot as plt
from parameters import cartConfig

class Cart():
    def __init__(self, L, Mp, g, t, Mc, x0, thM, nX, pX, T, F):
        """

        Class representing the cart pole problem

        PARAMS: pole length, pole mass, gravity, timestep, mass of the cart, horizontal location of the cart, 
                maximum magnitude of θ/th0, the left bound on the horizontal cart position, the right bound on the horizontal cart position
                the length of an episode, the length of an episode, in timesteps, F is the magnitude of that force.
                
        """

        self.L = L # length of the pole, in meter
        self.Mp = Mp # mass of the pole, in kg
        self.g = g # gravity m/sec^2
        self.t = t # the timestep for the simulation, in seconds

        # Pre-defined in the task
        self.Mc = Mc # mass of the cart, in kg
        self.x0 = x0 # horizontal location of the cart . 0 is the center
        self.thM = thM # maximum magnitude of th0. Above this (i.e. when |th0| > thM ) the pole is officially 'unbalances' and the episode fails. (thM = 0.21 radians) 
        self.nX = nX # the left bound on the horizontal cart position
        self.pX = pX # the right bound on the horizontal cart position
        self.T = T # the length of an episode, in timesteps 
        self.F = F # F is the magnitude of that force. (F = 10)

        self.step = 0

        self.th0 = random.uniform(-(self.thM), self.thM) # angle of the pole (in radians) with respect to the vertical // Theta
        self.Fs = [[-self.F], [self.F]]
            
        self.th1 =  0.0 # first temporal derivative of the pole angle
        self.th2 = 0.0 # second temporal derivate of the pole

        self.x1 = 0.0 # horizontal velocity of the cart
        self.x2 = 0.0 # horizontal acceleration of the cart

        self.screen = None

        self.first_game = []
        self.this_game = []
        self.best_game = []

        self.reset = 0


    def reset_game(self):
        """

        Method for reseting the game to its initial state. Much like the init-method.

        """

        self.L = cartConfig['game_config']['L']
        self.Mp = cartConfig['game_config']['Mp']
        self.g = cartConfig['game_config']['g']
        self.t = cartConfig['game_config']['t']
        self.Mc = cartConfig['game_config']['Mc']
        self.x0 = cartConfig['game_config']['x0']
        self.thM = cartConfig['game_config']['thM'] 
        self.nX = cartConfig['game_config']['nX']
        self.pX = cartConfig['game_config']['pX']
        self.T = cartConfig['game_config']['T']
        self.F = cartConfig['game_config']['F']
    
        self.th0 = random.uniform(-(self.thM), self.thM)
        self.Fs = [[-self.F], [self.F]]
        
        self.th1 =  0.0
        self.th2 = 0.0

        self.x1 = 0.0
        self.x2 = 0.0
  
        self.screen = None

        self.this_game = []   

        self.reset += 1

    def get_legal_moves(self):
        """

        Returns all legal moves to the sim world

        """

        return self.Fs


    def take_action(self, action):
        """

        Method that does the action the Sim World gives to the cart pole game.

        PARAMS: action

        """
        
        # Update this_game
        self.this_game.append(self.th0)

        if self.reset == 1:
            self.first_game.append(self.th0)

        # 1. The controller chooses a value for B (either F or -F),
        self.B = action[0]

        # 2. The 6 variables are updated via 2 complex and 4 simple relationships 

        # 2.1 -> update/set th2
        self.th2 =  self.update_th2(self.g, self.th0, self.Mp, self.B, self.L, self.th1, self.Mc)

        #2.2  -> update/set x2
        self.x2 = self.update_x2(self.Mp, self.B, self.th1, self.th0, self.Mc, self.th2, self.L)

        #2.3  -> update/set th1
        self.th1 = self.th1+(self.t*self.th2)

        #2.4  -> update/set  x1
        self.x1 = self.x1+(self.t*self.x2)

        #2.5  -> update/set  th0
        self.th0 += (self.t*self.th1)

        #2.6  -> update/set
        self.x0 = self.x0 + (self.t*self.x1)

        self.step = self.step+1


    # 2.1 -> update/set th2
    def update_th2(self, g, th0, Mp, B, L, th1, Mc):
        """

        Method for updating the second temporal derivate of the pole

        PARAMS: gravity, angle of the pole, first temporal derivative of the pole angle, the force, length of the pole,
                first temporal derivative of the pole angle, mass of the cart

        RETURNS: the second temporal derivate of the pole

        """

        
        return ((g * math.sin(th0) + ( ( math.cos(th0) * ((- B - Mp * L * (th1**2) * math.sin(th0)) ) / (Mc + Mp) ) ) )/         
                (L * (4.0 / 3.0 - (   (Mp * math.cos(th0)**2)    / (Mc + Mp)))))       


    #2.2  -> update/set x2
    def update_x2(self, Mp, B, th1, th0, Mc, th2, L):
        """

        Method for updating the horizontal acceleration of the cart

        PARAMS: mass of the cart, the force, first temporal derivative of the pole angle, 
        angle of the pole, mass of the cart, second temporal derivate of the pole, 
        length of the pole

        RETURNS: the horizontal acceleration of the cart

        """
        
        return (B + Mp * L * ((th1**2) * math.sin(th0)-th2*math.cos(th0))   )/(Mc+Mp)




    def get_state_key(self): 
        """

        Method for getting the state for which the sim world will send to the learner.

        RETURNS: a tuple of the state

        """        

        ret_list = []

        ret_list.append(round(self.th0, 1))

        # ret_list.append(round(self.th1, 0)) # It may be a good idea to use this for NN

        # ret_list.append(round(self.th2, 0)) # It may be a good idea to use this for NN

        ret_list.append(round(self.x0, 0))

        ret_list.append(round(self.x1, 1))

        ret_list.append(round(self.x2, 0))
                
        return tuple(ret_list)  


    def game_done(self):
        """

        Method that returns if the game is done or not, in addition to the reward
        for the action.

        RETURNS: list of reward and bool

        """

        th0 = self.th0
        thM = self.thM
        step = self.step
        x0 = self.x0
        nX = self.nX
        pX = self.pX    

        ret = [-1, False]

        if (nX < x0 and pX > x0 and thM> th0 and th0 > -thM and step == self.T):
            ret[1] = True
    
            # Update best_game to the latest win
            if self.this_game != []:
                self.best_game = self.this_game

            # Reset this_game
            self.this_game = []            

            if (nX/10 < x0 and pX/10 > x0 and thM/10> th0 and th0/10 > -thM):
                ret[0] = 2
            elif (nX/5 < x0 and pX/5 > x0 and thM/5> th0 and th0/5 > -thM):
                ret[0] = 0.8
            elif (nX/2 < x0 and pX/2 > x0 and thM/2> th0 and th0/2 > -thM):
                 ret[0] = 0.5
            else:
                 ret[0] = 0.1
            return ret

        elif(nX < x0 and pX > x0 and thM> th0 and th0 > -thM):
            # (1 - (x0 ** 2) / 11.52 - (th0 ** 2) / 288) Try to use this if step is not limited to a number
            ret[1] = False
            if (nX/10 < x0 and pX/10 > x0 and thM/10> th0 and th0/10 > -thM):
                ret[0] = 1.1 # 2
            elif (nX/5 < x0 and pX/5 > x0 and thM/5> th0 and th0/5 > -thM):
                ret[0] = 0.8 # 0.8
            elif (nX/2 < x0 and pX/2 > x0 and thM/2> th0 and th0/2 > -thM):
                 ret[0] = 0.6 # 0.5
            else:
                 ret[0] = 0.4 # 0.1
            return ret                           
        else:

            return [-225, True] 


    def get_graphic(self):
        """

        Method for visualizing the first and latest best game of a run.

        """

        # First try
        graph_vals = []

        for i, state in enumerate(self.first_game):

            graph_vals.append((i + 1, state))


        x = list(map(lambda x: x[0], graph_vals))
        y = list(map(lambda x: x[1], graph_vals))

        plt.plot(x, y)
        plt.xlabel("Timesteps")
        plt.ylabel("Angle")
        plt.show()

        # Best/latest try
        graph_vals = []

        for i, state in enumerate(self.best_game):

            graph_vals.append((i + 1, state))


        x = list(map(lambda x: x[0], graph_vals))
        y = list(map(lambda x: x[1], graph_vals))

        plt.plot(x, y)
        plt.xlabel("Timesteps")
        plt.ylabel("Angle")
        plt.show()


    def visualize(self, _, ep_step_count, __):
        """

        Method for visualizing the learning graph.

        PARAMS: list of episodes and steps
        RETURNS: list of episodes and steps, x label, y label

        """


        x_label = "Episodes"
        y_label = "Steps"

        return ep_step_count, x_label, y_label, None
        


