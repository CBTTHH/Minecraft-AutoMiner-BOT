import time

import bot.core.searching as searching
import bot.core.decision as decision
import bot.core.constants as C
from bot.core.player import player

# while not player.stop_tracking:
#     ore_coords, walkable_2d_coords = searching.searchOresLava()
    
#     cluster = searching.clusters(ore_coords)
#     best_cluster = decision.priorityGroup(cluster)
    
#     target_coord = (x, _, z) = best_cluster["center"]

#     time.sleep(C.ONE_TICK_TIME * 3)