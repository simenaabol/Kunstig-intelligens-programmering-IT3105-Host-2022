# Import and initialize your own actor
from Actor import ANET
import tensorflow as tf
from NeuralNetwork import custom_cross_entropy
from StateManager import StateManager
from Parameters import config
import time
from LiteModel import LiteModel
import copy

from Parameters import config, hex_config
from LiveCarlo.MonteCarloTreeSearch import MCTS

#  Husk å endre her
# path = "TrainedNets/Alle/9999400"

path = "Project2/TrainedNets/best/10"


model = tf.keras.models.load_model(path, custom_objects={"custom_cross_entropy": custom_cross_entropy})
state_manager = StateManager(config)
actor = ANET(model, None, None, None, None, None, 0, 1, state_manager)





# Import and override the `handle_get_action` hook in ActorClient
from Environment.Tournament.ActorClient import ActorClient
class MyClient(ActorClient):
    def handle_get_action(self, state):

        current_state = copy.deepcopy(state)

        # print('player', self.intPlayer)
        # oss = self.intPlayer
        starter = self.startin
        # # print('state1', state)

        if starter == 2:

            flipped = state_manager.flip_board(state)
            state = flipped

    
        


        # print('state2', state)
        row, col = actor.get_action2(False, state, False) # Your logic       
        return row, col

# Initialize and run your overridden client when the script is executed
if __name__ == '__main__':
    # Marcus
    # client = MyClient(auth="90b459360688431b8fc9e1e4cf6a77ec")

    # Simen    
    client = MyClient(auth="eba119845dbe40bea7a335dd52cb1009")

    # client.run()
    client.run(mode='league')
    