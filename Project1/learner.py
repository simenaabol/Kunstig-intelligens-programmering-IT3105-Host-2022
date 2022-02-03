import matplotlib.pyplot as plt
from actor_critic.actor import Actor
from actor_critic.sim_world import Sim_world
from actor_critic.NN_critic import NN_critic
from actor_critic.table_critic import Table_critic

class RL_learner():
    def __init__(self, config):
        self.sim_world = Sim_world()

        # Initialize pi(s, a) <- 0 /forall s, a
        self.actor = Actor(config)

        # Initialize V(s) with small random values
        if config["type_critic"] == "table":
            self.critic = Table_critic(config) # retrieve relevant parameters from config

        elif config["type_critic"] == "nn":
            self.critic = NN_critic(config) # retrieve relevant parameters from config


        self.num_episodes = config["num_episodes"]
        self.max_steps = config["max_steps"]


    def training(self):
        
        for episode in range(self.num_episodes):

            # Print every tenth episode to keep track
            if episode % 10 == 0:
                print("Episode nr. ", episode)

            # Reset eligibilities in actor and critic
            self.actor.reset_eligibilites()
            if self.critic == Table_critic():
                self.critic.reset_eligibilites()

            # Set initial state for sim world

            



            sim_world, state, done, legal_moves = self.sim_world.reset_game_state() # retrieve relevant values for the world


            """ Check for legal moves here """

            action = 

            for step in range(self.max_steps):
                # Do action a from state s, moving the system to state s'
                # and recieving reinforcement r
                pass
                

            

