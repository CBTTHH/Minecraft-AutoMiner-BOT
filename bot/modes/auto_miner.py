import bot.core.searching as searching
import bot.core.decision as decision
from bot.core.player import player

import bot.modes.descend as descend

def run():
    autoMiner()
    
def autoMiner():
    descend.run()
    
    while player.stop_tracking:
        ore_coords, walkable_2d_coords = searching.searchOresLava()
        
        cluster = searching.clusters(ore_coords)
        best_cluster = decision.priorityGroup(cluster)
        
        (x, _, z) = best_cluster["center"]
        goal = (x, z)
        path = decision.AStarPathFinder(walkable_2d_coords, goal)
        
        # mine ores and go down
