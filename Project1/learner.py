import matplotlib.pyplot as plt
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
        self.episode = 0
        self.vals_for_learning_graph = []
        self.least_steps = []


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
            number_steps = 0

            # Executing the steps for the episode
            for step in range(self.max_steps):
                number_steps += 1

                # Adds all states and actions to the actor
                self.actor.state_handler(state, legal_moves)

                # Adds all states in the table critic
                if isinstance(self.critic, Table_critic):
                    self.critic.state_handler(state)

                # Retrieves info for the next step in the episode
                next_state, reward, done, legal_moves = self.sim_world.step(action)
                episode_reward += reward

                if done or legal_moves == []:
                    # print(done)
                    #print("Game is done")
                    break

                # Set eligibilities to 1
                # Actor needs SAP-based eligibilites
                self.actor.set_initial_eligibility(state, action)
                if isinstance(self.critic, Table_critic):
                    # Critic needs state-based eligibilities
                    self.critic.set_initial_eligibility(state)

                # Calculating temporal difference error as well as the target- and current state value
                target_val, curr_state_val, td_error = self.critic.calc_td_error(state, reward, next_state)

                # Update policy for actor
                self.actor.update_eligibilities_and_policy(episode_actions, td_error, state)

                # print("STEP!!!")
                next_action = self.actor.get_action(next_state, legal_moves)

                episode_actions.append((state, td_error, action))

                # Update table or NN
                if isinstance(self.critic, Table_critic):
                    self.critic.update_eligibilities_and_values(episode_actions, td_error)
                else:
                    self.critic.update_weights(episode_actions, target_val, curr_state_val)

                state = next_state
                action = next_action

            self.episode += 1
            self.actor.update_epsilon()
            self.vals_for_learning_graph.append((self.episode + 1, number_steps))
            self.least_steps.append(number_steps)
            # print("End state", state, "Episode reward:", episode_reward, "Number steps:", number_steps)

    def show_learning_graph(self):
        x = list(map(lambda x: x[0], self.vals_for_learning_graph))
        y = list(map(lambda x: x[1], self.vals_for_learning_graph))
        print("Least amount of steps",min(self.least_steps))

        plt.plot(x, y)
        plt.xlabel("Episode")
        plt.ylabel("Number of steps")
        plt.show()
        

