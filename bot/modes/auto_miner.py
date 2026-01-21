import bot.core.searching as searching
import bot.core.decision as decision
import bot.core.movement as move
import bot.core.mining as mining
from bot.core.player import player

import bot.modes.descend as descend

def run():
    autoMiner()
    
def autoMiner():
    descend.run()
    
    while not player.stop_tracking:
        ore_coords, walkable_2d_coords = searching.searchOresLava()
        
        cluster = searching.clusters(ore_coords)
        best_cluster = decision.priorityGroup(cluster)
        
        target_coord = (x, _, z) = best_cluster["center"]
        goal = (x, z)
        path = decision.AStarPathFinder(walkable_2d_coords, goal)
        
        move.goToTarget(path, target_coord)
        mining.mineCluster(best_cluster["coords"])

        move.finalizeDescent()