import matplotlib.pyplot as plt
from numpy import isin
from actor_critic.actor import Actor
from actor_critic.sim_world import Sim_world
from actor_critic.NN_critic import NN_critic
from actor_critic.table_critic import Table_critic

class RL_learner():
    def __init__(self, config):
    
        self.sim_world = Sim_world()

        # Initialize pi(s, a) <- 0 /forall s, a
        """ Expand config to add the right values """
        self.actor = Actor(config)

        # Initialize V(s) with small random values
        if config["type_critic"] == "table":
            """ Expand config to add the right values """
            self.critic = Table_critic(config) # retrieve relevant parameters from config

        elif config["type_critic"] == "nn":
            """ Expand config to add the right values """
            self.critic = NN_critic(config) # retrieve relevant parameters from config


        self.num_episodes = config["num_episodes"]
        self.max_steps = config["max_steps"]
        self.config = config


    def training(self):
        
        for episode in range(self.num_episodes):

            # Print every tenth episode to keep track
            if episode % 10 == 0:
                print("Episode nr. ", episode)

            # Reset eligibilities in actor and critic
            self.actor.reset_eligibilites()
            if isinstance(self.critic, Table_critic):
                self.critic.reset_eligibilites()

            # Retrieve initial state for sim world
            state, done, legal_moves = self.sim_world.reset_game_state()

            if not legal_moves:
                break

            action = self.actor.get_action(state, legal_moves)

            while not done:

                # Set eligibilities to 1
                self.actor.set_initial_eligibility(state, action)
                if isinstance(self.critic, Table_critic):
                    self.critic.set_initial_eligibility(state)

                next_state, reward, done, legal_moves = self.sim_world.step(action)

                next_action = self.actor.get_action(next_state, legal_moves)

                # Calculating temporal difference error as well as the target- and current state value
                target_val, curr_state_val, td_error = self.critic.calc_td_error()

                






                # Stores the states for the episode
                self.actor.state_handler(state, legal_moves)
                if isinstance(self.critic, Table_critic):
                    self.critic.state_handler(state, legal_moves)





            


            

