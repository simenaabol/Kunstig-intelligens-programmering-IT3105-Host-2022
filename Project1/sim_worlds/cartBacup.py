from random import randrange
import random
import math

from parameters import cartConfig


class Cart():
    def __init__(self, L, Mp, g, t, Mc, x0, thM, nX, pX, T, step, nF, pF):

        self.L = L # length of the pole, in meter
        self.Mp = Mp # mass of the pole, in kg
        self.g = g # gravity m/sec^2
        self.t = t # the timestep for the simulation, in seconds

        #Pre-defined in the task
        self.Mc = Mc # mass of the cart, in kg
        self.x0 = x0 # horizontal location of the . 0 is the center
        self.thM = thM # maximum magnitude of th0. Above this (i.e. when |th0| > thM ) the pole is officially 'unbalances' and the episode fails. (thM = 0.21 radians) 
        self.nX = nX # the left bound on the horizontal cart position
        self.pX = pX # the right bound on the horizontal cart position
        self.T = T # the length of an episode, in timesteps 
        self.step = step
        self.nF = nF # F is the magnitude of that force. (F = 10)
        self.pF = pF

        
        self.th0 = random.uniform(-(self.thM), self.thM) # angle og the pole (in radians) with respect to the vertical // Theta
        # self.th0 = 0.0
        self.Fs = [[self.nF], [self.pF]]
        

        
        self.th1 =  0.0 # first temporal derivative of the pole angle
        self.th2 = 0.0 # second temporal derivate of the pole

        self.x1 = 0.0 # horizontal velocity of the cart
        self.x2 = 0.0 # horizontal acceleration of the cart

        self.B = 0 # the bang-bang force, either F or -F, where F is the magnitude of that force. (F=10)
        self.step_reward = 0.0

        self.screen = None

    def reset_game(self):
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
        self.step = cartConfig['game_config']['step']
        self.nF = cartConfig['game_config']['nF']
        self.pF = cartConfig['game_config']['pF']
        
        self.th0 = random.uniform(-(self.thM), self.thM)
        # self.th0 = -0.19
        self.Fs = [[self.nF], [self.pF]]
        
        self.th1 =  0.0
        self.th2 = 0.0

        self.x1 = 0.0
        self.x2 = 0.0

        self.B = 0
        self.step_reward = 0.0

        self.screen = None

    def get_th0(self):
        return self.th0


    # 2.1 -> update/set th2
    def update_th2(self, g, th0, pF, Mp, B, L, th1, Mc):
        
        return ((g * math.sin(th0) + ( ( math.cos(th0) * ((- B - Mp * L * (th1**2) * math.sin(th0)) ) / (Mc + Mp) ) ) )/         
                (L * (4.0 / 3.0 - (   (Mp * math.cos(th0)**2)    / (Mc + Mp)))))       

    #2.2  -> update/set x2
    def update_x2(self, Mp, B, th1, th0, Mc, th2, L):
        
        return (B + Mp * L * ((th1**2) * math.sin(th0)-th2*math.cos(th0))   )/(Mc+Mp)

    def take_action(self, action):
        # 1. The controller chooses a value for B (either F or -F),
        # nF = self.nF
        
        pF = self.pF
        # Fs = [nF, pF]
        # B = random.choice(action)
        B = action[0]
        # print(B)

        # self.B = B
        

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

        th2 =  self.update_th2(g, th0, pF, Mp, B, L, th1, Mc)
        self.th2 = th2
        # print ('th2: ', th2)

        #2.2  -> update/set x2
        x2 = self.x2
        th1 = self.th1

        x2 = self.update_x2(Mp, B, th1, th0, Mc, th2, L)
        self.x2 = x2
        # print('x2: ', x2)


        #2.3  -> update/set th1
        t = self.t
        th1 = th1+(t*th2)
        self.th1=th1
        # print('th1: ',th1)

        #2.4  -> update/set  x1
        x1 = self.x1
        x1 = x1+(t*x2)
        self.x1=x1

        #2.5  -> update/set  th0

        th0 += (t*th1)
        self.th0 = th0

        #2.6  -> update/set

        x0 = self.x0
        x0 = x0 + (t*x1)
        self.x0 = x0
        # print('x0: ', x0)

        self.step = self.step+1
        # print(self.th0)


    def get_state(self):
        return self.th0

    def get_state_key(self): 
        # linear position, angular position, linear velocity, angular velocity
        ret_list = []
        
        th0 = (self.th0)
        # th0 = tuple(th0)
        ret_list.append(round(th0, 1))
        # ret_list.append(math.sin(th0))
        # ret_list.append(math.cos(th0))


        th1 = round(self.th1)
        # th1 = tuple(th1)
        # ret_list.append(th1)
        

        th2 = round(self.th2)
        # th1 = tuple(th1)
        # ret_list.append(th2)

        x0 = round(self.x0, 0) # bør være 0 når tho=1
        # x0 = tuple(x0)
        ret_list.append(x0)

        x1 = round(self.x1,0)# bør være 0 når tho=1 - gjerne være null
        # x1 = tuple(x1)
        ret_list.append(x1)

        x2 = round(self.x2,0) # Burde være null uansett egt?
        # x2 = tuple(x2)
        ret_list.append(x2)
                
        return tuple(ret_list)  

    def get_legal_moves(self):
        # print(self.x0)
        return self.Fs

    def game_done(self):
        th0 = self.th0
        thM = self.thM
        step = self.step
        # print('Angel: ', th0)
        x0 = self.x0
        nX = self.nX
        pX = self.pX    
    
        ret = [-1, False]


        T = self.T
        # print('T: ', step)
        if (nX < x0 and pX > x0 and thM> th0 and th0 > -thM and step == T):
            ret[1] = True
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
            # (1 - (x0 ** 2) / 11.52 - (th0 ** 2) / 288)
            # It's alive
            ret[1] = False
            if (nX/10 < x0 and pX/10 > x0 and thM/10> th0 and th0/10 > -thM):
                ret[0] = 1.1 # før 2
            elif (nX/5 < x0 and pX/5 > x0 and thM/5> th0 and th0/5 > -thM):
                ret[0] = 0.8 # før 0.8
            elif (nX/2 < x0 and pX/2 > x0 and thM/2> th0 and th0/2 > -thM):
                 ret[0] = 0.6 # før 0.5
            else:
                 ret[0] = 0.4 # før 0.1
            return ret                           
        else:
            return [-225, True]

    def visualize(self, _, ep_step_count, __):

        x_label = "Episodes"
        y_label = "Steps"

        return ep_step_count, x_label, y_label, None
