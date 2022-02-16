from actor_critic.actor import Actor
from actor_critic.sim_world import Sim_world
from actor_critic.NN_critic import NN_critic
from actor_critic.table_critic import Table_critic

import matplotlib.pyplot as plt

class RL_learner():
    def __init__(self, config):
        """ 

        Initializing the learning process with the Sim World, Actor, and Critic depending
        on which critic is chosen. ALL parameters are retrieved from a single file, called
        'parameters.py'.

        The Sim World is acting like a central hub for all of the toy problems.

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
                                    self.parameters["anncritic_config"]["hidden_layers"])

        else:
            raise Exception("Choose either 'table' or 'nn'")

        # Variables for limiting how many runs and episodes the system runs
        self.num_episodes = self.parameters["num_episodes"]
        self.max_steps = self.parameters["max_steps"]

        # Lists for visualization
        self.ep_step_count = []
        self.least_steps_list = []

    def training(self):
        """ 

        Runs a training loop for the system depending on the amount of episodes and steps
        from the parameters.

        """
        
        for episode in range(self.num_episodes):

            # Another list for visualization
            list_of_states = []
 
            # Print some episodes to keep track of progress
            if episode % 10 == 0:
                print("Episode nr. ", episode)

            # Reset eligibilities in actor and table-based critic
            self.actor.reset_eligibilites()
            if isinstance(self.critic, Table_critic):
                self.critic.reset_eligibilites()

            # Retrieve initial state from the Sim World chosen.
            from_state, is_finished, legal_moves = self.sim_world.get_initial_game_state()

            # Check for legal moves
            if legal_moves == []:
                print("No legal moves", from_state)
                break

            # Retrieves ONE action based on the actor's policy or a random move
            action = self.actor.get_action(from_state, legal_moves)

            episode_actions = []
            episode_reward = 0

            # Executing the steps/actions for the episode
            for step in range(self.max_steps):

                # Initializing the actor policy with states, and legal moves, with 0's
                self.actor.state_handler(from_state, legal_moves)
                # adding all states, and their legal moves into the actor's policy.
                # Setter alt inn i policyen basicly, setter alt til null

                # Initializing the value table with small random values (0,1)
                if isinstance(self.critic, Table_critic):
                    self.critic.state_handler(from_state)
                    # Inne i state_handler: Legger kun inn states og en random verdi på nye states

                # Retrieve new values after a action
                current_state, reward, is_finished, legal_moves = self.sim_world.step(action, self.actor, self.parameters, episode )
                episode_reward += reward

                # Set eligibilities to 1
                # Actor needs SAP-based eligibilites -> State-Action-Pairs
                self.actor.set_initial_eligibility(from_state, action)

                if isinstance(self.critic, Table_critic):   # Hvis Table brukes, så kommen man vell inn hit uansett?
                    # Table critic needs state-based eligibilities
                    self.critic.set_initial_eligibility(from_state) # Disse settes også til 1

                # Calculating temporal difference error as well as the target- and current state value
                # hø? ->   as well as the target- and current state value
                td_error = self.critic.calc_td_error(from_state, reward, current_state)

                # Append the SAP with the td error
                episode_actions.append((from_state, td_error, action))
                # print('episode_actions: ', episode_actions)
                # episode_actions:  [(((4, 3, 2, 1), (), ()), 1.0761952615116628, (0, 1)),

                # Update the eligibilities and policy for the actor
                self.actor.update_eligibilities_and_policy(episode_actions, td_error, from_state)
                

                # Update values for the table critic or the NN-critic
                if isinstance(self.critic, Table_critic):
                    self.critic.update_eligibilities_and_values(episode_actions, td_error)
                    # Her er det bare Table-critic som trenger episode_actions
                else:
                    self.critic.update_weights(td_error) #Dette må være for NN?

                # Checks if the game is finished
                if is_finished or legal_moves == []:

                    # Append the last state for visualization
                    from_state = current_state
                    list_of_states.append(current_state)

                    break    

                # Retrieve the next action based on the current state, and legal moves.
                next_action = self.actor.get_action(current_state, legal_moves)
                # next_action er et move - ikke flere

                # Set state and action for next step cycle
                from_state = current_state
                action = next_action
                #Tar vare på den gamle action-en for å?
                # Spør Marcy her
                # self.sim_world.step bruker jo action, så man ligger evt alltid en bak?#
                # Man henter inn action ved slutten av hver step, hvorfor ikke i starten?

                # For visualization
                list_of_states.append(current_state)
                
            # Decrease the epsilon at the end of an episode
            self.actor.update_epsilon(-1)

            # For visualization
            self.ep_step_count.append((episode + 1, step + 1))
            self.least_steps_list.append(step)

            # print("End state", from_state, "Episode reward:", episode_reward, "Number steps:", step)

    def show_learning_graph(self, visualize=False):
        """ 

        Shows the learning graph as well as visualizing the best episode if this option is chosen.

        PARAMS: visualizer bool

        """

        vals_for_graph, x_label, y_label, least_steps = self.sim_world.get_visualizing_data(self.actor, self.ep_step_count, self.least_steps_list)

        x = list(map(lambda x: x[0], vals_for_graph))
        y = list(map(lambda x: x[1], vals_for_graph))

        if least_steps:
            print("Least amount of steps", least_steps)

        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

        if visualize:
            self.sim_world.render()