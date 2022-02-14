from actor_critic.actor import Actor
from actor_critic.sim_world import Sim_world
from actor_critic.NN_critic import NN_critic
from actor_critic.table_critic import Table_critic

import matplotlib.pyplot as plt

class RL_learner():
    def __init__(self, config):
        self.sim_world = Sim_world(config)

        self.parameters = self.sim_world.get_parameters()

        self.actor = Actor(self.parameters["actor_config"]["learning_rate"], 
                            self.parameters["actor_config"]["discount_factor"], 
                            self.parameters["actor_config"]["epsilon"],
                            self.parameters["actor_config"]["epsilon_decay"], 
                            self.parameters["actor_config"]["eligibility_decay"])

        if config["critic"] == "table":
            self.critic = Table_critic(self.parameters["critic_config"]["learning_rate"], 
                                        self.parameters["critic_config"]["discount_factor"], 
                                        self.parameters["critic_config"]["eligibility_decay"])

        elif config["critic"] == "nn":
            """ Expand with the right values """
            self.critic = NN_critic(self.parameters["anncritic_config"]["learning_rate"], 
                                    self.parameters["critic_config"]["discount_factor"], 
                                    self.parameters["critic_config"]["input_size"], 
                                    self.parameters["critic_config"]["num_layers"])

        else:
            raise Exception("Choose either 'table' or 'nn'")


        self.num_episodes = self.parameters["num_episodes"]
        self.max_steps = self.parameters["max_steps"]
        self.ep_step_count = []
        self.least_steps_list = []


    def training(self):
        
        for episode in range(self.num_episodes):

            list_of_states = []
 
            # Print every tenth episode to keep track
            if episode % 10 == 0:
                print("Episode nr. ", episode)

            # Reset eligibilities in actor and table-based critic
            self.actor.reset_eligibilites()
            if isinstance(self.critic, Table_critic):
                self.critic.reset_eligibilites()

            # Retrieve initial state for sim world
            state, done, legal_moves = self.sim_world.get_initial_game_state()

            # Check for legal moves
            if legal_moves == []:
                print("No legal moves", state)
                break

            # Retrieves action based on policy/epsilon
            action = self.actor.get_action(state, legal_moves)

            episode_actions = []
            episode_reward = 0

            # Executing the steps for the episode
            for step in range(self.max_steps):

                # Initializing the actor policy with states, and legal moves.
                self.actor.state_handler(state, legal_moves)

                # Initializing the value table with small random values
                if isinstance(self.critic, Table_critic):
                    self.critic.state_handler(state)

                # Retrieves info for the next step in the episode
                next_state, reward, done, legal_moves = self.sim_world.step(action)
                episode_reward += reward

                # Checks if the game is done
                if done or legal_moves == []:
                    # print("GAME OVER", done)
                    break

                # Set eligibilities to 1
                # Actor needs SAP-based eligibilites
                self.actor.set_initial_eligibility(state, action)
                if isinstance(self.critic, Table_critic):
                    # Critic needs state-based eligibilities
                    self.critic.set_initial_eligibility(state)

                # Calculating temporal difference error as well as the target- and current state value
                target_val, curr_state_val, td_error = self.critic.calc_td_error(state, reward, next_state)

                # Append the SAP with the td error
                episode_actions.append((state, td_error, action))

                # Update the eligibilities and policy for the actor
                self.actor.update_eligibilities_and_policy(episode_actions, td_error, state)

                # Update values for the table critic or the NN-critic
                if isinstance(self.critic, Table_critic):
                    self.critic.update_eligibilities_and_values(episode_actions, td_error)
                else:
                    self.critic.update_weights(episode_actions, target_val, curr_state_val)

                # Retrieve the next action
                next_action = self.actor.get_action(next_state, legal_moves)

                # Set state and action for next step cycle
                state = next_state
                action = next_action

                list_of_states.append(state)

            self.actor.update_epsilon()

            # For visualization
            self.ep_step_count.append((episode + 1, step))
            self.least_steps_list.append(step)

            # print("Before end state", state, "Episode reward:", episode_reward, "Number steps:", step)


    def show_learning_graph(self):

        vals_for_graph, x_label, y_label, least_steps = self.sim_world.get_visualizing_data(self.actor, self.ep_step_count, self.least_steps_list)

        x = list(map(lambda x: x[0], vals_for_graph))
        y = list(map(lambda x: x[1], vals_for_graph))

        if least_steps:
            print("Least amount of steps", least_steps)

        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

