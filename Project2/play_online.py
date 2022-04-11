# Import and initialize your own actor
from Actor import ANET
import tensorflow as tf
from NeuralNetwork import custom_cross_entropy
from StateManager import StateManager
from Parameters import config

path = "./TrainedNets/OHT/5"
model = tf.keras.models.load_model(path, custom_objects={"custom_cross_entropy": custom_cross_entropy})
state_manager = StateManager(config)
actor = ANET(model, None, None, None, None, None, 0, 1, state_manager)

# Import and override the `handle_get_action` hook in ActorClient
from Environment.Tournament.ActorClient import ActorClient
class MyClient(ActorClient):
    def handle_get_action(self, state):
        
        row, col = actor.get_action2(False, state, False) # Your logic
        
        # print(row, col)
        
        return row, col

# Initialize and run your overridden client when the script is executed
if __name__ == '__main__':
    client = MyClient(auth="90b459360688431b8fc9e1e4cf6a77ec")
    client.run(mode='league')