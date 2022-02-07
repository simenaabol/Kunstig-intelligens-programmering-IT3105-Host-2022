import matplotlib.pyplot as plt
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

        """ Used for reward graph if we want """
        rewards = []
        
        for episode in range(self.num_episodes):

            # Print every tenth episode to keep track
            if episode % 10 == 0:
                print("Episode nr. ", episode)

            # Reset eligibilities in actor and table-based critic
            self.actor.reset_eligibilites()
            if isinstance(self.critic, Table_critic):
                self.critic.reset_eligibilites()

            """ Dont know if we need to reset the game itself also? Or only use these variables """
            # Retrieve initial state for sim world
            state, done, legal_moves = self.sim_world.get_initial_game_state()

            # Gets the best action from the current policy
            action = self.actor.get_action(state, legal_moves)

            if not legal_moves:
                print("No legal moves")
                break

            episode_actions = []
            episode_reward = 0

            # Executing the steps for the episode
            while not done:

                """ IDK """
                self.actor.state_handler(state, legal_moves)
                if isinstance(self.critic, Table_critic):
                    self.critic.state_handler(state, legal_moves)

                # Set eligibilities to 1
                # Actor needs SAP-based eligibilites
                self.actor.set_initial_eligibility(state, action)
                if isinstance(self.critic, Table_critic):
                    # Critic needs state-based eligibilities
                    self.critic.set_initial_eligibility(state)

                # Retrieves info for the next step in the episode
                next_state, reward, done, legal_moves = self.sim_world.step(action)
                episode_reward += reward

                next_action = self.actor.get_action(next_state, legal_moves)

                # Calculating temporal difference error as well as the target- and current state value
                target_val, curr_state_val, td_error = self.critic.calc_td_error(state, reward, next_state)

                episode_actions.append((state, td_error, action))
    
                # Update policy for actor
                self.actor.update_eligibilities_and_policy(episode_actions, td_error, state)

                # Update table or NN
                if isinstance(self.critic, Table_critic):
                    self.critic.update_eligibilities_and_values(episode_actions, td_error)
                else:
                    self.critic.update_weights(episode_actions, target_val, curr_state_val)

                state = next_state
                action = next_action

            self.actor.update_epsilon()


