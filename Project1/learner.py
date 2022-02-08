import matplotlib.pyplot as plt
# from Project1 import parameters
from actor_critic.actor import Actor
from actor_critic.sim_world import Sim_world
from actor_critic.NN_critic import NN_critic
from actor_critic.table_critic import Table_critic

class RL_learner():
    def __init__(self, config):
        self.sim_world = Sim_world(config)

        self.parameters = self.sim_world.get_parameters()

        self.actor = Actor(self.parameters["actor_config"]["learning_rate"], 
                            self.parameters["actor_config"]["discount_factor"], 
                            self.parameters["actor_config"]["epsilon"],
                            self.parameters["actor_config"]["epsilon_decay"], 
                            self.parameters["actor_config"]["eligibility_decay"])

        if self.parameters["critic"] == "table":
            self.critic = Table_critic(self.parameters["critic_config"]["learning_rate"], 
                                        self.parameters["critic_config"]["discount_factor"], 
                                        self.parameters["critic_config"]["eligibility_decay"])

        elif self.parameters["critic"] == "nn":
            """ Expand with the right values """
            self.critic = NN_critic(self.parameters)

        else:
            raise Exception("Choose either 'table' or 'nn'")


        self.num_episodes = self.parameters["num_episodes"]
        self.max_steps = self.parameters["max_steps"]
        self.config = config


    def training(self):

        """ Used for reward graph if we want """
        rewards = []
        
        for episode in range(self.num_episodes):

            # Print every tenth episode to keep track
            # if episode % 10 == 0:
            #     print("Episode nr. ", episode)

            print("Episode nr:", episode)

            # Reset eligibilities in actor and table-based critic
            self.actor.reset_eligibilites()
            if isinstance(self.critic, Table_critic):
                self.critic.reset_eligibilites()

            # Retrieve initial state for sim world
            state, done, legal_moves = self.sim_world.get_initial_game_state()

            if len(legal_moves) == 0:
                print(state)
                break

            # Gets the best action from the current policy
            print("EPISODE!!!")
            action = self.actor.get_action(state, legal_moves)

            # if not legal_moves:
            #     print("No legal moves")
            #     break

            episode_actions = []
            episode_reward = 0
            
            # Executing the steps for the episode
            for step in range(self.parameters["max_steps"]):

                """ IDK """
                # self.actor.state_handler(state, legal_moves)
                # if isinstance(self.critic, Table_critic):
                #     self.critic.state_handler(state, legal_moves)

                # Retrieves info for the next step in the episode
                next_state, reward, done, legal_moves = self.sim_world.step(action)
                episode_reward += reward

                # Set eligibilities to 1
                # Actor needs SAP-based eligibilites
                self.actor.set_initial_eligibility(state, action)
                if isinstance(self.critic, Table_critic):
                    # Critic needs state-based eligibilities
                    self.critic.set_initial_eligibility(state)


                if done or legal_moves == []:
                    print("Game is done")
                    break


                # Calculating temporal difference error as well as the target- and current state value
                target_val, curr_state_val, td_error = self.critic.calc_td_error(state, reward, next_state)

                # Update policy for actor
                self.actor.update_eligibilities_and_policy(episode_actions, td_error, state)

                print("STEP!!!")
                next_action = self.actor.get_action(next_state, legal_moves)

                episode_actions.append((state, td_error, action))

                # Update table or NN
                if isinstance(self.critic, Table_critic):
                    self.critic.update_eligibilities_and_values(episode_actions, td_error)
                else:
                    self.critic.update_weights(episode_actions, target_val, curr_state_val)

                state = next_state
                action = next_action

            self.actor.update_epsilon()


