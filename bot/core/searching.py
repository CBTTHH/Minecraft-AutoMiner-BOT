import minescript
import bot.core.constants as C
from bot.core.player import player

def searchForOres_old(off_xz = 7, off_y = 6, cache=None, ore = 'diamond') -> set: 
    # Facing east: xyz normal coordinate plane
    coords_with_ores = set()
    if not cache: cache = set()
    
    def search_nearby(bx,by,bz): # searches blocks around a diamond block
        for dx in [-1, 0 , 1]:
            for dy in [-1, 0 , 1]:
                for dz in [-1, 0 , 1]:
                    _x, _y, _z = bx+dx, by+dy, bz+dz
                    if _y < -59: continue
                    if not minescript.getblock(_x,_y,_z).endswith(f'{ore}_ore'): continue
                    if (_x,_y,_z) not in coords_with_ores:
                        coords = (_x,_y,_z)
                        coords_with_ores.add(coords) and cache.add(coords)
                        search_nearby(_x,_y,_z)
                    
    for x in range(player.x-off_xz, player.x+off_xz+1):
        for y in range(player.y-2, player.y+off_y+1):
            for z in range(player.z-off_xz, player.z+off_xz+1):
                if (x,y,z) in cache: continue
                cache.add((x,y,z))
                if (y % 2 == 0 and ((x % 2 == 0 and z % 2 == 0) or (x % 2 == 1 and z % 2 == 1))) or \
                   (y % 2 == 1 and ((x % 2 == 0 and z % 2 == 1) or (x % 2 == 1 and z % 2 == 0))):
                    if minescript.getblock(x,y,z).endswith(f'{ore}_ore'):
                        search_nearby(x,y,z)

                    
    if not coords_with_ores:
        minescript.echo(f'No {ore}s nearby, increasing searching radius to a off set of {off_xz+3}')
        return searchForOres_old(off_xz+3, off_y+2, cache)
    
    minescript.echo(coords_with_ores, len(coords_with_ores))
    return coords_with_ores


def searchForOres(r=7, ore='diamond') -> set: 
    
    def search_nearby(bx,by,bz): # searches blocks around a diamond block
        for dx in [-1, 0 , 1]:
            for dy in [-1, 0 , 1]:
                for dz in [-1, 0 , 1]:
                    
                    coord_neighbor = (_x, _y, _z) = (bx + dx, by + dy, bz + dz)
                    
                    if not minescript.getblock(_x,_y,_z).endswith(f'{ore}_ore') or _y <= C.INVALID_Y_LEVEL[0]: 
                        continue
                    
                    if coord_neighbor not in coords_with_ores:
                        coords_with_ores.add(coord_neighbor) 
                        cache.add(coord_neighbor)
                        search_nearby(_x,_y,_z)
                        
    # Facing east: xyz normal coordinate plane
    coords_with_ores = set()
    cache = set()
    prev_r = 0 ## xz and y separated #################################
    
    while True:          
    
        for dx in range(-r, r + 1):
            for dy in range(max(C.INVALID_Y_LEVEL[0] + 1 - player.y, -r), r + 1):
                for dz in range(-r, r + 1):
                    
                    if max(abs(dx), abs(dy), abs(dz)) <= prev_r:
                        continue
                    
                    coord = (x, y, z) = (player.x + dx, player.y + dy, player.z + dz)
                    
                    if coord in cache: 
                        continue
                    
                    cache.add(coord)
                    
                    if (y % 2 == 0 and ((x % 2 == 0 and z % 2 == 0) or (x % 2 == 1 and z % 2 == 1))) or \
                       (y % 2 == 1 and ((x % 2 == 0 and z % 2 == 1) or (x % 2 == 1 and z % 2 == 0))):
                        if minescript.getblock(x,y,z).endswith(f'{ore}_ore'):
                            search_nearby(x,y,z)
    
        if coords_with_ores:
            minescript.echo(coords_with_ores, len(coords_with_ores))
            return coords_with_ores
        
        prev_r = r
        r += 3
        minescript.echo(f'No {ore}s nearby, increasing searching radius to a off set of {r}')
   




def clusters(ores_coords:set) -> list:
    clusters = []
    seen = set()
    
    def neighbors(coords_main:tuple, ores_coords:set): #check diamond neighbors
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
            
    # print(clusters, len(clusters))
    return clusters


