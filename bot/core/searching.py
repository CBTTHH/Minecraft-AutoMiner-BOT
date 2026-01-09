import minescript as m
import bot.core.constants as C
from bot.core.decision import findingMinableNodes
from bot.core.player import player

def searchOresLava(r=16, ore='diamond') -> tuple[set[tuple], set[tuple]]:
    sx, sy, sz = player.x, player.y, player.z
    
    prev_r = 0    
    ores_coords = set()
    lava_coords = set()
    region_coord = set()
    min_y = C.INVALID_Y_LEVEL[0] + 1
    
    
    while True:
        min_dy = max(min_y - sy, - r)
        pos1 = (sx - r, min_y, sz - r)
        pos2 = (sx + r, sy + r, sz + r)
        
        m.await_loaded_region(sx - r, sz - r, sx + r, sz + r)
        
        region = m.get_block_region(pos1, pos2)
        
        for dx in range(-r, r + 1):
            for dy in range(min_dy, r + 1):
                for dz in range(-r, r + 1):
                    
                    if max(abs(dx), abs(dy), abs(dz)) <= prev_r: # Shell expansion
                        continue
                    
                    coord = (x, y, z) = (sx + dx, sy + dy, sz + dz)
                    block = region.get_block(x, y, z)
                    region_coord.add(coord)
                    
                    if not block: continue
                    
                    if block.endswith(f"{ore}_ore"):
                        ores_coords.add(coord)
                    elif block.startswith("minecraft:lava") and (C.Y_LEVEL_LAVA_CHECK[0] <= y <= C.Y_LEVEL_LAVA_CHECK[1]):
                        lava_coords.add(coord)
                        
        if ores_coords:
            return ores_coords, findingMinableNodes(lava_coords, region_coord)
        
        prev_r = r
        r += 4
        m.echo(f'No {ore}s nearby, increasing searching radius to a offset of {r}')
    


def clusters(ores_coords:set) -> list[dict]:
    clusters = []
    seen = set()
    
    def neighbors(coords_main:tuple, ores_coords:set): # check diamond neighbors
        x_main, y_main, z_main = coords_main
        seen.add(coords_main)
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    
                    if dx == dy == dz == 0: 
                        continue
                    
                    coords_neighbor = (x_main+dx, y_main+dy, z_main+dz)
                    
                    if (coords_neighbor in ores_coords) and (coords_neighbor not in seen):
                        cluster['coords'].append(coords_neighbor)
                        seen.add(coords_neighbor)
                        neighbors(coords_neighbor, ores_coords)
    
    for coords in ores_coords:
        if coords not in seen:
            cluster = {'coords': [],
                       'size' : 0,
                       'center': (0, 0, 0)}
            
            cluster['coords'].append(coords)
            neighbors(coords, ores_coords)
            
            xs, ys, zs = zip(*cluster['coords'])     
            cluster['size'] = size = len(cluster['coords'])
            cluster['center'] = (sum(xs)//size, sum(ys)//size, sum(zs)//size)
            clusters.append(cluster)
            
    # m.echo(clusters, len(clusters))
    return clusters


