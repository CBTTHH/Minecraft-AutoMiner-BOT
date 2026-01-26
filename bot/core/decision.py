from queue import PriorityQueue

import minescript as m
import bot.core.minescript_extra as m_extra
import bot.core.searching as searching
import bot.core.constants as C
from bot.core import player


def priorityGroup(clusters, ore=C.MINING_ORE, caption=True) -> dict:
    if len(clusters) == 1: 
        if caption:
            m.echo(f"{m_extra.txt_clr('g')}Going to group of {ore}s at {m_extra.txt_clr('a')}{clusters[0]['center']} {m_extra.txt_clr('g')}(closest)")
        return clusters[0]
    
    CLOSE_TO_PLAYER = 10
    
    for cluster in clusters:    # Calculate the distance from the player to the clusters
        x, y, z = cluster['center']
        dist = abs(player.x - x) + abs(player.y - y) + abs(player.z - z)
        cluster['distance'] = dist
    
    clusters_close = [cluster for cluster in clusters if cluster['distance'] <= CLOSE_TO_PLAYER]
    
    if clusters_close:      # Mine closer clusters first
        best_cluster, best_score = clusters_close[0], float("inf")
        
        for cluster in clusters_close:
            score = (C.CLUSTER_SIZE_SCORE * cluster['distance']) - (cluster['size'] * C.CLUSTER_SIZE_SCORE)
            
            if score <= best_score:
                best_score = score
                best_cluster = cluster
        if caption:
            m.echo(f"{m_extra.txt_clr('g')}Going to group of {ore}s at {m_extra.txt_clr('a')}{best_cluster['center']} {m_extra.txt_clr('g')}(closest)")
        return best_cluster
    
    # No diamonds close to the player, try to find the largest with with travel less distance
    best_cluster = min(clusters, key=lambda cluster: (-(cluster['size']), cluster['distance']))
    
    if caption:
        m.echo(f"{m_extra.txt_clr('g')}Going to group of {ore}s at {m_extra.txt_clr('a')}{best_cluster['center']} {m_extra.txt_clr('g')}(largest and closest)")
    return best_cluster


def direction(target_coord:tuple|None) -> tuple[str]:
    if (not target_coord):
        return (None, None, None)
    
    px, py, pz = player.x, player.y, player.z
    tx, ty, tz = target_coord
    
    zs, xs, ys = "N/S: ", "W/E: ", "UP/DOWN: "
    dx, dy, dz = abs(px - tx), abs(py - ty) + 1, abs(pz - tz)
    
    xs += f"{m_extra.txt_clr('y')}east ({dx})" if px < tx else f"{m_extra.txt_clr('y')}west ({dx})" \
        if px > tx else f"{m_extra.txt_clr('g')}same"
    zs += f"{m_extra.txt_clr('y')}south ({dz})" if pz < tz else f"{m_extra.txt_clr('y')}north ({dz})" \
        if pz > tz else f"{m_extra.txt_clr('g')}same"
    ys += f"{m_extra.txt_clr('y')}up ({dy})" if py < ty else f"{m_extra.txt_clr('y')}down ({dy})" \
        if py > ty else f"{m_extra.txt_clr('g')}same"
    
    direction = (zs, xs, ys)
    return direction
    

## A* PATHFINDER
def safely_transf_3D_to_2D(lava_coords:set[tuple], region:set[tuple]) -> set[tuple]:
    CRITICALS = (_, PLAYER_HEAD_Y, PLAYER_Y, _) = (player.y + dy for dy in [2, 1, 0, -1]) # (-56, -57, -58, -59) normally
    
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


def AStarPathFinder(
    grid_2d:set[tuple], 
    goal:tuple[int, int], 
    next_searching_r=24
    ) -> list[tuple]:
    
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
        m.echo(f"{m_extra.txt_clr('r')}Path not found...")
        return None
    
    path = []
    while goal != start:
        path.append(goal)
        goal = inverse_path[goal]
    path.append(start)

    return path


## PATH HANDLING
def findReachableCluster(r=16, step=4):
    invalid_coords = set()

    while r <= C.MAX_SEARCHING_RADIUS:
        ore_coords, lava_coord, region_coords = searching.searchOresLava(r)
        ore_coords -= invalid_coords

        walkable_2d_coords = findingMinableNodes(lava_coord, region_coords)
        
        clusters = searching.clusters(ore_coords)
        best_cluster = priorityGroup(clusters)
        
        goal = (best_cluster['center'][0], best_cluster['center'][2])
        path = AStarPathFinder(walkable_2d_coords, goal)
        
        if r >= C.MAX_PATH_SEARCHING_RADIUS:
            invalid_coords |= (set(best_cluster['coords']))

        if path:
            return path, best_cluster

        r += step

    return None, None

