import math
from queue import PriorityQueue

import minescript as m
import bot.core.searching as searching
import bot.core.decision as decision
from bot.core.player import player

def priorityGroup(clusters, ore = 'diamond') -> dict:
    if len(clusters) == 1: 
        m.echo(f'Going to group of {ore}s at {clusters[0]['center']} (closest)')
        return clusters[0]
    
    CLOSE_TO_PLAYER = 5
    
    for cluster in clusters:    # Calculate the distance from the player to the clusters
        x, y, z = cluster['center']
        dist = math.sqrt((player.x - x)**2 + (player.y - y)**2 + (player.z - z)**2)
        cluster['distance'] = dist
    
    clusters_close = [cluster for cluster in clusters if cluster['distance'] <= CLOSE_TO_PLAYER]
    
    if clusters_close:      # Mine closer clusters first
        best_cluster, best_score = clusters_close[0], float('inf')
        
        for cluster in clusters_close:
            score = (1.5 * cluster['distance']) - (cluster['size'] * 1.7)
            
            if score <= best_score:
                best_score = score
                best_cluster = cluster
        
        m.echo(f'Going to group of {ore}s at {best_cluster['center']} (closest)')
        return best_cluster
    
    #No diamonds close to the player, try to find the largest with with travel less distance
    best_cluster = min(clusters, key=lambda cluster: (-(cluster['size']), cluster['distance']))
    m.echo(f'Going to group of {ore}s at {best_cluster['center']} (largest and closest)')
    return best_cluster


# A* pathfinder 
def safely_transf_3D_to_2D(lava_coords:set[tuple], region:set[tuple]) -> set[tuple]:
    CRITICALS = (ABOVE_Y, PLAYER_HEAD_Y, PLAYER_Y, BOTTOM_Y) = (-56, -57, -58, -59)
    
    columns = {}
    walkable_2D = set()
    
    for x, y, z in region:
        if (x, z) not in columns:
            columns[(x, z)] = set()
        columns[(x, z)].add(y)
    
    for (x, z), ys in columns.items():

        if (PLAYER_HEAD_Y not in ys) or (PLAYER_Y not in ys):
            continue

        if any((x, y, z) in lava_coords for y in CRITICALS):
            continue

        walkable_2D.add((x, z))

    return walkable_2D
          

def findingMinableNodes(lava_coords:set[tuple], region:set[tuple]) -> set[tuple]:
    FLOW_DIRS = [( 1,  0,  0),
                 (-1,  0,  0),
                 ( 0,  0,  1),
                 ( 0,  0, -1),
                 ( 0, -1,  0)]
    
    unavailable_region = set(lava_coords)

    for lx, ly, lz in lava_coords:

        for dx, dy, dz in FLOW_DIRS:

            neighbor_coord = (lx + dx, ly + dy, lz + dz)
            if neighbor_coord in region:
                unavailable_region.add(neighbor_coord)
    
    for coord in unavailable_region:
        region.discard(coord)

    return safely_transf_3D_to_2D(lava_coords, region)


def h(pos: tuple[int, int], end_pos: tuple[int, int]) -> int:
    x1, z1 = pos
    x2, z2 = end_pos
    
    return abs(x2 - x1) + abs(z2 - z1)


def AStarPathFinder(grid_2d:set[tuple], goal:tuple[int, int], next_searching_r:int = 32) -> list[tuple]:
    NEIGHBOR_BLOCK = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    start = (player.x, player.z)
    g_score = {coord:float("inf") for coord in grid_2d}
    g_score[start] = 0
    f_score = {coord:float("inf") for coord in grid_2d}
    f_score[start] = h(start, goal)
    
    open_set = PriorityQueue()
    visited = set()
    inverse_path = {}
    found = False
    
    open_set.put((f_score[start], h(start, goal), start))
    
    while not open_set.empty():
        curr_coord = open_set.get()[2]
        
        if curr_coord == goal:
            found = True
            break
        
        if curr_coord in visited:
            continue

        visited.add(curr_coord)
        
        for dx, dz in NEIGHBOR_BLOCK:
            cx, cz = curr_coord
            neighbor = (cx + dx, cz + dz)
            
            if (neighbor not in grid_2d) or (neighbor in visited):
                continue
            
            temp_g = g_score[curr_coord] + 1
            temp_f = temp_g + h(neighbor, goal)
            
            if temp_f < f_score[neighbor]:
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_f
                
                open_set.put((f_score[neighbor], h(neighbor, goal), neighbor))
                inverse_path[neighbor] = curr_coord
    
    if not found:
        m.echo("Path not found, increasing region")
        
        diamond_coords, walkable_2D = searching.searchOresLava(next_searching_r)
        best_cluster = decision.priorityGroup(searching.clusters(diamond_coords))
        
        (x, _, z) = best_cluster["center"]
        goal = (x, z)
        
        return AStarPathFinder(walkable_2D, goal, next_searching_r + 4)
    
    path = []
    while goal != start:
        path.append(goal)
        goal = inverse_path[goal]
    
    return path