from random import randrange
import random
import math


class Cart():
    def __init__(self, L, Mp, g, t): #
        #
        self.L = L # length of the pole, in meter
        self.Mp = Mp # mass of the pole, in kg
        self.g = g # gravity m/sec^2
        self.t = t # the timestep for the simulation, in seconds

        #Pre-defined in the task
        self.Mc = 1.0 # mass of the cart, in kg
        self.x0 = 0.0 # horizontal location of the . 0 is the center
        self.thM = 0.21 # maximum magnitude of th0. Above this (i.e. when |th0| > thM ) the pole is officially 'unbalances' and the episode fails. (thM = 0.21 radians) 
        self.nX = -2.4 # the left bound on the horizontal cart position
        self.pX = 2.4 # the right bound on the horizontal cart position
        self.T = 300.0 # the length of an episode, in timesteps 
        self.step = 0.0
        self.nF = -10 # F is the magnitude of that force. (F = 10)
        self.pF = 10
        self.th0 = random.uniform(-(self.thM), self.thM) # angle og the pole (in radians) with respect to the vertical // Theta
        self.Fs = [self.nF, self.pF]
        

        
        self.th1 =  0.0 # first temporal derivative of the pole angle
        self.th2 = 0.0 # second temporal derivate of the pole

        self.x1 = 0.0 # horizontal velocity of the cart
        self.x2 = 0.0 # horizontal acceleration of the cart

        self.B = 0 # the bang-bang force, eithre F or -F, where F is the magnitude of that force. (F=10)
        #self.B = random.choice(Fs)

    def get_th0(self):
        return self.th0


    # 2.1 -> update/set th2
    def update_th2(self,g, th0, pF, Mp, B, th1, Mc, L):

        return (g*math.sin(th0)+math.cos(th0)* (( (-pF-Mp*L*(th1**2)*math.sin(th0)) )  / (Mp+Mc)  )    / (L*(4.0/3.0 -( (Mp*math.cos(th0)**2 )/(Mp+Mc)  )) )   )
        

    #2.2  -> update/set x2
    def update_x2(self, pF, Mp, L, th1, th0, Mc, th2):

        return (pF+Mp*L*    ((th1**2)*math.sin(th0)-th2*math.cos(th0))   )/(Mc+Mp)

    def take_action(self):
        # 1. The controller chooses a value for B (either F or -F),
        nF = self.nF
        pF = self.pF
        Fs = [nF, pF]
        B = random.choice(Fs)
        B = self.B
        

        # 2. The 6 variables are updated via 2 complex and 4 simple relationships 
        # 2.1 -> update/set th2
        th2 = self.th2

        g = self.g
        pF = self.pF
        Mp = self.Mp
        L = self.L
        th0 = self.th0
        th1 = self.th1
        Mc = self.Mc

        th2 =  self.update_th2(g, th0, pF, Mp, L, th1, Mc, L)
        print ('th2: ', th2)

        #2.2  -> update/set x2
        x2 = self.x2
        th1 = self.th1

        x2 = self.update_x2(pF, Mp, L, th1, th0, Mc, th2)
        print('x2: ', x2)


        #2.3  -> update/set th1
        t = self.t
        th1 = th1+(t*th2)
        print('th1: ',th1)

        #2.4  -> update/set  x1
        x1 = self.x1
        x1 = x1+(t*x2)

        #2.5  -> update/set  th0

        th0 = th0 + (t*th1)

        #2.6  -> update/set

        x0 = self.x0
        x0 = x0 + (t*x1)
        print('x0: ', x0)
         
             

        



    def get_state(self):
        return self.th0

    def get_state_key(self):
        return tuple(self.th0)  

    def get_legal_moves(self):
        raise self.Fs

    def game_done(self):
        th0 = self.th0
        thM = self.thM
        step = self.step
        T = self.T
        
        if (thM> th0 and th0 > -thM and step == T):
            return [1000, True]
        elif (thM> th0 and th0 > -thM):
            return [10, False]
        else:
            return [-1, False]






Step = Cart(0.5 , 0.1 , 9.8 , 0.002 )
Step.take_action()
