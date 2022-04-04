import tensorflow as tf
from Actor import ANET
import os

class Topp:
    def __init__(self, config):
        
        path_list = [anet_path for anet_path in os.scandir("./NeuralNets")]
        
        self.anets = self.get_anets(path_list)
        # self.number_of_anets = len(self.anets)
        # self.number_of_games = config['number_of_games']
        
        
        
    def get_anets(self, path_list):
        
        print(path_list)
        
        anets = {}
        
        for path in path_list:
            
            model = tf.keras.models.load_model(path)
            
            anet = ANET(model, None, None, None, None, None, None, None, None, None)
            
            anets[path] = anet
            
        print(anets)
            
            
    
    def play_one_game(self):
        pass
    
    def run_tournament(self):
        pass
    
    def visualize(self):
        pass
    
    
    
# toppytop = Topp(None)
# toppytop.get_anets()