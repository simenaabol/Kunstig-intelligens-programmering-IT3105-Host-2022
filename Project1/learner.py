from actor_critic.actor import Actor
from actor_critic.sim_world import Sim_world
from actor_critic.NN_critic import NN_critic
from actor_critic.table_critic import Table_critic

import matplotlib.pyplot as plt

class RL_learner():
    def __init__(self, config):
        """ 
        
        """
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
            self.critic = NN_critic(self.parameters["anncritic_config"]["learning_rate"], 
                                    self.parameters["anncritic_config"]["discount_factor"], 
                                    self.parameters["anncritic_config"]["input_size"], 
                                    self.parameters["anncritic_config"]["num_layers"])

        else:
            raise Exception("Choose either 'table' or 'nn'")


        self.num_episodes = self.parameters["num_episodes"]
        self.max_steps = self.parameters["max_steps"]
        self.ep_step_count = []
        self.least_steps_list = []


    def training(self):
        
        for episode in range(self.num_episodes):

            list_of_states = []
 
            # Print some episodes to keep track of progress
            if episode % 10 == 0:
                print("Episode nr. ", episode)

            # Reset eligibilities in actor and table-based critic
            self.actor.reset_eligibilites()
            if isinstance(self.critic, Table_critic):
                self.critic.reset_eligibilites()

            # Retrieve initial state for sim world
            from_state, done, legal_moves = self.sim_world.get_initial_game_state()

            # Check for legal moves
            if legal_moves == []:
                print("No legal moves", from_state)
                break

            # Retrieves ONE action based on policy/epsilon (or a random one)
            action = self.actor.get_action(from_state, legal_moves)
            # print('action', action)

            episode_actions = []
            episode_reward = 0

            # Executing the steps for the episode
            for step in range(self.max_steps):

                # Initializing the actor policy with states, and legal moves, with 0's
                self.actor.state_handler(from_state, legal_moves)

                # Initializing the value table with small random values (0,1)
                if isinstance(self.critic, Table_critic):
                    self.critic.state_handler(from_state)

                # Retrieve new values after a action
                current_state, reward, done, legal_moves = self.sim_world.step(action)
                episode_reward += reward

                # Set eligibilities to 1
                # Actor needs SAP-based eligibilites (actor)
                self.actor.set_initial_eligibility(from_state, action)
                if isinstance(self.critic, Table_critic):
                    # Critic needs state-based eligibilities
                    self.critic.set_initial_eligibility(from_state)

                # Calculating temporal difference error as well as the target- and current state value
                target_val, curr_state_val, td_error = self.critic.calc_td_error(from_state, reward, current_state)

                # Append the SAP with the td error
                episode_actions.append((from_state, td_error, action))

                # Update the eligibilities and policy for the actor
                self.actor.update_eligibilities_and_policy(episode_actions, td_error, from_state)

                # Update values for the table critic or the NN-critic
                if isinstance(self.critic, Table_critic):
                    self.critic.update_eligibilities_and_values(episode_actions, td_error)
                else:
                    self.critic.update_weights(td_error)

                # list_of_states.append(from_state)

                # Checks if the game is done
                if done or legal_moves == []:
                    from_state = current_state
                    list_of_states.append(current_state)
                    # print("GAME OVER", done)
                    break    

                # Retrieve the next action
                next_action = self.actor.get_action(current_state, legal_moves)

                # list_of_states.append(from_state)

                # Set state and action for next step cycle
                from_state = current_state
                action = next_action

                list_of_states.append(current_state)

            self.actor.update_epsilon()

            # For visualization
            self.ep_step_count.append((episode + 1, step + 1))
            self.least_steps_list.append(step)

            # print("STATE:", episode_actions[0][0])

            self.sim_world.set_visualizing_data(list_of_states)


            # print("Before end state", from_state, "Episode reward:", episode_reward, "Number steps:", step)


    def show_learning_graph(self):

        # print(self.actor.get_actor_policy())

        self.sim_world.render()

        vals_for_graph, x_label, y_label, least_steps = self.sim_world.get_visualizing_data(self.actor, self.ep_step_count, self.least_steps_list)

        x = list(map(lambda x: x[0], vals_for_graph))
        y = list(map(lambda x: x[1], vals_for_graph))

        if least_steps:
            print("Least amount of steps", least_steps)

        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
