from collections import defaultdict
import numpy as np

class Node: 
    def __init__(self, state, parent, player):
        """

        Class for a node, which is to be used in the Monte Carlo Searc Tree -class

        PARAMS: state, parent, player

        """   

        self.state = state
        self.player = player
        self.parent = parent
        # self.kids = {} # main-kok 
        self.kids = defaultdict(lambda: None) # main-kok 
        # kids[action] = en kid-node
        self.kids_rollout = defaultdict(lambda: None) # main-kok
        # self.kids_rollout = {} # main-kok

        self.evaluate = 0
        self.count = 0



    def update_count(self):
        """

        Method - Increment the visits-counter of the node. 

        PARAMS: nothing

        RETURNS: nothing 

        """
        self.count +=1


    def update_evaluate(self, eval):
        """

        Method - Update the evaluation of a node. 

        PARAMS: eval

        RETURNS: nothing 

        """
        self.evaluate += eval


    def get_player(self):
        """

        Method - Fetch the player int. 

        PARAMS: nothing

        RETURNS: int 

        """
        return self.player


    def get_state(self):
        """

        Method - Fetch the node state 

        PARAMS: nothing

        RETURNS: int? 

        """
        return self.state


    def get_kids(self):
        """

        Method - Fetch the kids for the node 

        PARAMS: nothing

        RETURNS: dict of kids 

        """
        return self.kids
    
    def get_roll_kids(self):
        """

        Method - Fetch the kids for the node 

        PARAMS: nothing

        RETURNS: dict of kids 

        """
        return self.kids_rollout

    def add_kid(self, kid, action, rollout = False): #kok siste del
        """

        Method - Add a kid to to node 

        PARAMS: kid, action, rollout
  
        RETURNS: nothing

        """
        
        # print("ADD KID", kid, "ACTION", action)
        
        if rollout == True:
            self.kids_rollout[action] = kid
        else:
            self.kids[action] = kid
            


    def get_kid_with_action(self, action, rollout = False): # kok siste del
        """

        Method - Fetch a kid with a action 

        PARAMS: action, rollout

        RETURNS: kid node

        """
        
        # print("KIDS ROLLOUT", self.kids_rollout)
        # print("VANLIGE KIDS", self.kids)
        
        
        # print('get_kid', action)
        # print('get_kid', self.kids_rollout)
        if rollout == True:
            return self.kids_rollout[action]
        else:
            return self.kids[action]
        
        
          


    def remove_kid(self, action, rollout = False): # kok siste del
        """

        Method - Remove the kid with the action from the input

        PARAMS: action, rollout

        RETURNS: kid node

        """
        if rollout == True:
            self.kids_rollout[action] = None
        else:
            print('---------------------------------------------------------------')
            self.kids[action] = None
        

    
    def get_action_count(self, action):
        """

        Method - Fetch the action count from the kid with the action input

        PARAMS: action

        RETURNS: kid, or 0

        """

        if self.kids[action]:
            return self.kids[action].count
        else:
            return 0
            # Denne burde egt endres til None

    
    def get_kids_count(self):
        """

        Method - Fetch the numbers of kids the node have
        
        PARAMS: nothinh

        RETURNS: int

        """

        return len(self.kids)

    
    def get_parent(self):
        """

        Method - Fetch the parent of the node 

        PARAMS: nothing

        RETURNS: parent

        """

        return self.parent


    def get_q_value(self, action):
        """

        Method - Fetch the q-value

        PARAMS: action

        RETURNS: int

        """
        
        # print("ACTION", action)

        if self.get_action_count(action) != 0:
            # kok, endre på oppsettet?
            """ TIL SIMEN, get_kids() tar ingen argumenter """
            return ( self.get_kid_with_action(action).evaluate )  /  ( self.get_action_count(action) )
        else: 
            return 0

    
    def get_u_value(self, action, exploration_weight):
        """

        Method - Fetch the u-value

        PARAMS: action, exploration_weight

        RETURNS: int (flooat?)

        """

        # rein kok på oppsettet - ich - mye likt her på de fleste 
        
        return (  np.sqrt( np.log( self.count ) ) * exploration_weight  )  / ( 1 + self.get_action_count(action)   )


    

        
        