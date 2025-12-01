import time, minescript, math, threading

class PlayerTracker:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = -90
        self.x_velocity, self.y_velocity, self.z_velocity = 0, 0, 0
        self.targeted_block = None
        
        self.stop_tracking = False
        self.pos_update_thread = threading.Thread(target=self.update_position) 
        self.tool_update_thread = threading.Thread(target=self.update_tool_in_main_hand)
        self.pos_update_thread.daemon = True
        self.tool_update_thread.daemon = True
        self.pos_update_thread.start()
        self.tool_update_thread.start()
        time.sleep(0.1)
        
    
    def update_position(self):
        while not self.stop_tracking:
            px, py, pz = minescript.player().position
            self.x = math.floor(px)
            self.y = math.floor(py)
            self.z = math.floor(pz)
            
            yaw = ((minescript.player().yaw + 180) % 360) - 180

            if yaw >= -135 and yaw < -45: self.yaw = -90
            elif yaw >= -45 and yaw <= 45: self.yaw = 0 
            elif yaw > 45 and yaw <= 135: self.yaw = 90
            else: self.yaw= 180

            self.x_velocity, self.y_velocity, self.z_velocity = minescript.player().velocity
            
            time.sleep(0.01)
            
    
    def update_tool_in_main_hand(self):
        shovel_blocks = {'minecraft:dirt', 
                         'minecraft:gravel', 
                         'minecraft:clay',
                         'minecraft:grass_block[snowy=false]', 
                         'minecraft:sand', 
                         'minecraft:soul_sand',}
        
        blocks = {'minecraft:cobblestone',
                  'minecraft:stone', 
                  'minecraft:cobbled_deepslate', 
                  'minecraft:deepslate'
                  'minecraft:diorite', 
                  'minecraft:granite', 
                  'minecraft:sandstone'}
        
        food = {'minecraft:cooked_beef', 
                'minecraft:cooked_chicken', 
                'minecraft:cooked_porkchop', 
                'minecraft:cooked_salmon', 
                'minecraft:golden_carrot', 
                'minecraft:golden_apple', 
                'minecraft:pumpkin_pie'}
        
        while not self.stop_tracking:
            main_hand_item = minescript.player_hand_items().main_hand
            if main_hand_item: current_item = main_hand_item.get('item')
            else: 
                time.sleep(0.1)
                continue
            
            if current_item:
                try:
                    if current_item.endswith('water_bucket') or current_item.endswith('bucket') or current_item in blocks or current_item in food:
                        time.sleep(0.5)
                        continue
        
                    if minescript.player_get_targeted_block(5):
                        if minescript.player_get_targeted_block(5)[3] in shovel_blocks: minescript.player_inventory_select_slot(3)
                        else: minescript.player_inventory_select_slot(2)
                    time.sleep(0.1)
                except Exception as e:
                    minescript.echo('Error:', e)
                    time.sleep(0.1)
                    pass
                

    def stop(self):
        self.stop_tracking = True
        self.update_thread.join()
        print('Script STOPPED by user')
        exit()



# Initiating threads:     
player = PlayerTracker()
getblock_y_minus = lambda y: minescript.getblock(player.x, player.y-y, player.z)

# Repetitive functions:
def stuck_y():
    if not minescript.player_get_targeted_block(3):
        time.sleep(0.01)
        if minescript.player_get_targeted_block(150)[0] != [player.x, player.y-1, player.z] and player.y_velocity >= -0.0784000015258789:
            minescript.player_press_backward(True) 
            minescript.player_press_left(True)
            time.sleep(0.2)
            minescript.player_press_backward(False)
            minescript.player_press_left(False)
            return goToCenter()

def stuck_x(yaw):
    if player.z_velocity == 0.0 and not minescript.player_get_targeted_block(2):
        minescript.player_press_forward(False)
        goToCenter(yaw, 30)

# Go Down Functions
def inWater():
    minescript.echo('Player is in WATER!!!')
    while minescript.player_get_targeted_block(2) == None:
        minescript.player_press_sneak(True) 
    minescript.player_press_sprint(True)
    minescript.player_press_sneak(False)
    time.sleep(0.5)
    minescript.player_press_attack(False)
    minescript.player_inventory_select_slot(8)
    minescript.player_press_use(True)
    time.sleep(0.5)
    minescript.player_inventory_select_slot(8)
    
    block_positions = [(player.x+1.5, player.y-1, player.z+.5), (player.x+1.5, player.y+.7, player.z+.5), 
                       (player.x+.5, player.y-1, player.z+1.5), (player.x+.5, player.y+.7, player.z+1.5), 
                       (player.x-1.5, player.y-1, player.z+.5), (player.x-1.5, player.y+.5, player.z+.5), 
                       (player.x+.5, player.y-1, player.z-1.5), (player.x+.5, player.y+.5, player.z-1.5)]
    
    for position in block_positions:
        x, y, z = position
        minescript.player_look_at(x,y,z)
        time.sleep(0.35)
        
    minescript.player_press_jump(True)
    time.sleep(0.7)
    minescript.player_press_jump(False)
    minescript.player_press_sneak(True)
    time.sleep(0.6)
    minescript.player_press_sneak(False)
    minescript.player_set_orientation(-179,-60)
    time.sleep(0.65)
    minescript.player_inventory_select_slot(4)
    time.sleep(0.3)
    minescript.player_set_orientation(-90,90)
    time.sleep(0.4)
    minescript.player_press_use(False)
    
    while not minescript.player_hand_items().main_hand['item'].startswith('minecraft:water'):
        minescript.player_press_use(True)
        time.sleep(0.05)
        minescript.player_press_use(False)
    
    time.sleep(0.2)
    if getblock_y_minus(0).startswith('minecraft:water'):
        goToCenter()
        return inWater()
        
    minescript.echo('Player is not more in WATER :D')
    minescript.player_inventory_select_slot(2)
    return minescript.player_press_attack(True)


def closeToLava():
    minescript.echo('Player CLOSE to LAVA!!!')
    minescript.player_press_sneak(True) 
    minescript.player_set_orientation(player.yaw, 20) 
    minescript.player_press_forward(True)
    time.sleep(5)
    minescript.player_press_forward(False)
    
    if getblock_y_minus(7).startswith('minecraft:lava') or getblock_y_minus(17).startswith('minecraft:lava') or \
       minescript.getblock(player.x, -55, player.z).startswith('minecraft:lava'):
        return closeToLava()
    
    minescript.echo('Player is NOT more close to LAVA (:D')
    return goToCenter()


def waterDrop():
    minescript.echo('Falling!!!')
    minescript.player_press_attack(False)
    minescript.player_inventory_select_slot(4)
    
    while player.y_velocity < -.7 :
        minescript.player_press_use(True)
        time.sleep(0.05)
    minescript.player_press_use(False) 
    time.sleep(0.05)
    
    while not minescript.player_hand_items().main_hand['item'].startswith('minecraft:water'):
        minescript.player_press_use(True)
        time.sleep(0.05)
        
    minescript.player_press_use(False)
    minescript.player_inventory_select_slot(2)
    minescript.echo('Alto Clutch!!!')
    time.sleep(0.3)
    
    return goToCenter()


def goToCenter(yaw = None, pitch = 90):
    if yaw is None:
        yaw = player.yaw
        
    x_center = math.floor(minescript.player().position[0])+0.5
    z_center = math.floor(minescript.player().position[2])+0.5
    
    minescript.player_press_sneak(True) 
    minescript.player_set_orientation(yaw, pitch)
    
    if minescript.player().position[0] > x_center:
        while round(minescript.player().position[0],3)-0.017 > x_center:
            if yaw == -90: minescript.player_press_backward(True)
            elif yaw == 0: minescript.player_press_right(True)
            elif yaw == 90: minescript.player_press_forward(True)
            else: minescript.player_press_left(True)
    else:
        while round(minescript.player().position[0],3)-0.017 < x_center: 
            if yaw == -90: minescript.player_press_forward(True)
            elif yaw == 0: minescript.player_press_left(True)
            elif yaw == 90: minescript.player_press_backward(True)
            else: minescript.player_press_right(True)
            
    minescript.player_press_forward(False)
    minescript.player_press_left(False)
    minescript.player_press_backward(False)
    minescript.player_press_right(False)
    minescript.player_press_sneak(False)

    stuck_y()
    
    minescript.player_press_sneak(True) and minescript.player_set_orientation(yaw, pitch)
    
    if minescript.player().position[2] > z_center:
        while round(minescript.player().position[2],3)-0.017 > z_center:
            if yaw == -90: minescript.player_press_left(True)
            elif yaw == 0: minescript.player_press_backward(True)
            elif yaw == 90: minescript.player_press_right(True)
            else: minescript.player_press_forward(True)
    else:
        while round(minescript.player().position[2],3)-0.017 < z_center:
            if yaw == -90: minescript.player_press_right(True)
            elif yaw == 0: minescript.player_press_forward(True)
            elif yaw == 90: minescript.player_press_left(True)
            else: minescript.player_press_backward(True)
            
    stuck_y()
            
    minescript.player_press_right(False)
    minescript.player_press_forward(False)
    minescript.player_press_left(False)
    minescript.player_press_backward(False)
    minescript.player_press_sneak(False)     
        
    return


def mineToNegative58():
    minescript.echo('Mining to y level -58')
    goToCenter()
    minescript.player_inventory_select_slot(2)
    
    while True:
        time.sleep(0.02)
        minescript.player_press_attack(True)
        
        if player.y_velocity < -.7 and not getblock_y_minus(4).startswith('minecraft:water') and \
           not getblock_y_minus(2).startswith('minecraft:water'):
            waterDrop()
            continue
            
        if getblock_y_minus(7).startswith('minecraft:lava') or getblock_y_minus(17).startswith('minecraft:lava') or\
           minescript.getblock(player.x, -55, player.z).startswith('minecraft:lava'):
            closeToLava()
            continue
            
        if getblock_y_minus(0).startswith('minecraft:water'):
            inWater()
            continue
        
        
        if not minescript.player_get_targeted_block(3):
            time.sleep(0.001)
            if minescript.player_get_targeted_block(150)[0] != getblock_y_minus(-1) and player.y_velocity == -0.0784000015258789:
                minescript.player_press_backward(True) 
                minescript.player_press_left(True)
                time.sleep(0.2)
                minescript.player_press_backward(False) 
                minescript.player_press_left(False)
                goToCenter()
            continue

        
        if player.y <= -58:
            while player.y < -58:
                minescript.player_set_orientation(player.yaw, -90)
                minescript.player_inventory_select_slot(2)
                while minescript.player_get_targeted_block(1) != None:
                    minescript.player_press_attack(True)
                minescript.player_inventory_select_slot(8) 
                minescript.player_set_orientation(player.yaw, 90)
                minescript.player_press_attack(False)
                minescript.player_press_use(True)
                time.sleep(0.02) 
                minescript.player_press_jump(True)
                time.sleep(0.3)
                minescript.player_press_jump(False)
                minescript.player_press_use(False)
            break
        
    minescript.player_set_orientation(player.yaw, -60) 
    minescript.player_press_attack(False) 
    minescript.player_inventory_select_slot(8)
    minescript.player_press_use(True)
    time.sleep(0.3)
    minescript.player_press_use(False)
    minescript.player_set_orientation(player.yaw, 30)
    return minescript.echo(f'At y level {player.y}')  # Arrive at y -58


def searchForOres(off_xz = 7, off_y = 6, cache=None, ore = 'diamond') -> set: 
    # Facing east: xyz normal coordinate plane
    time.sleep(0.01) # Dont crash threads
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
        return searchForOres(off_xz+3, off_y+2, cache)
    
    # print(coords_with_ores, len(coords_with_ores))
    return coords_with_ores


def clusters(ores_coords:set) -> list:
    clusters = []
    seen = set()
    
    def neighbors(coords_main:tuple, ores_coords:set):
        x_main, y_main, z_main = coords_main
        seen.add(coords_main)
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == dy == dz == 0: continue
                    coords_neighbor = (x_main+dx, y_main+dy, z_main+dz)
                    if coords_neighbor in ores_coords and coords_neighbor not in seen:
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


def priorityGroup(clusters, ore = 'diamond'):
    if len(clusters) == 1: 
        minescript.echo(f'Going to group of {ore}s at {clusters[0]['center']} (closest)')
        return clusters[0]
    close_to_player = 5
    
    for cluster in clusters:
        x, y, z = cluster['center']
        dist = math.sqrt((player.x - x)**2 + (player.y - y)**2 + (player.z - z)**2)
        cluster['distance'] = dist
    
    clusters_close = [cluster for cluster in clusters if cluster['distance'] <= close_to_player]
    
    if clusters_close: #Mine closer clusters first
        if len(clusters_close) == 1: return clusters_close[0]
        best_cluster, best_score = clusters_close[0], float('inf')
        
        for cluster in clusters_close:
            score = (1.5 * cluster['distance']) - (cluster['size'] * 2)
            
            if score <= best_score:
                best_score = score
                best_cluster = cluster
        
        minescript.echo(f'Going to group of {ore}s at {best_cluster['center']} (closest)')
        return best_cluster
    
    #No diamonds close to the player, try to find the largest with with travel less distance
    best_cluster = min(clusters, key=lambda cluster: (-(cluster['size']), cluster['distance']))
    minescript.echo(f'Going to group of {ore}s at {best_cluster['center']} (largest and closest)')
    return best_cluster


def goToTarget(best_cluster_center:dict, imprecision=0.02):
    target_x, target_y, target_z = best_cluster_center
    
    goToCenter(pitch=30)
    time.sleep(0.02)
    minescript.player_press_attack(True) 
    minescript.player_inventory_select_slot(2)
    
    if player.x > target_x:
        yaw = 90
        while round(player.x,3) - imprecision > target_x:
            minescript.player_set_orientation(90, 30)
            time.sleep(0.02)
            minescript.player_press_forward(True)
            stuck_x(yaw)
    else:
        yaw = -90
        while round(player.x,3) + imprecision < target_x: 
            minescript.player_set_orientation(-90, 30) 
            time.sleep(0.02)
            minescript.player_press_forward(True)
            stuck_x(yaw)
                
    minescript.player_press_forward(False) 
    minescript.player_press_attack(False)
    goToCenter(yaw, 30)
    time.sleep(0.02)
    minescript.player_press_attack(True)
        
    if player.z > target_z:
        yaw = 180
        while round(player.z,3) - imprecision > target_z:
            minescript.player_set_orientation(180, 30)
            time.sleep(0.2)
            minescript.player_press_forward(True)
            stuck_x(yaw)
    else:
        yaw = 0
        while round(player.z,3) + imprecision < target_z:
            minescript.player_set_orientation(0, 30) 
            time.sleep(0.2)
            minescript.player_press_forward(True)
            stuck_x(yaw)

    minescript.player_press_forward(False)
    minescript.player_press_attack(False)
    goToCenter(yaw, 20)
    time.sleep(0.02)
    minescript.player_press_attack(True)
    
    if player.y > target_y:
        while player.y > target_y:
            minescript.player_set_orientation(player.yaw, 90)
    else: 
        while player.y < target_y:
            minescript.player_set_orientation(player.yaw, -90)
            minescript.player_inventory_select_slot(2)
            while minescript.player_get_targeted_block(1) != None:
                minescript.player_press_attack(True)
            minescript.player_inventory_select_slot(8) 
            minescript.player_set_orientation(player.yaw, 90)
            minescript.player_press_attack(False) 
            minescript.player_press_use(True)
            time.sleep(0.02) 
            minescript.player_press_jump(True)
            time.sleep(0.3)
            minescript.player_press_jump(False) 
            minescript.player_press_use(False)
            
    return minescript.player_press_attack(False)


def mineOresAndGoBack(best_cluster_coords:list[tuple[int]], ore = 'diamond'):
    best_cluster_coords.sort(key=lambda coords: coords[1], reverse=True)
    minescript.player_inventory_select_slot(2)
    for coords in best_cluster_coords:
        x, y, z = coords
        minescript.player_press_attack(True)
        minescript.player_look_at(x+.5,y+.5,z+.5)
        while minescript.getblock(x,y,z).endswith(f'{ore}_ore'):
            time.sleep(0.02)
    
    minescript.player_press_forward(True) 
    minescript.player_press_jump(True)
    time.sleep(0.3)
    minescript.player_press_forward(False) 
    minescript.player_press_jump(False)
    time.sleep(0.02)
    goToCenter(player.yaw)
    
    if player.y > -58:
        while player.y > -58:
            minescript.player_set_orientation(player.yaw, 90)
            time.sleep(0.02)
    else: 
        while player.y < -58:
            minescript.player_set_orientation(player.yaw, -90)
            minescript.player_inventory_select_slot(2)
            while minescript.player_get_targeted_block(1) != None:
                minescript.player_press_attack(True)
            minescript.player_inventory_select_slot(8) 
            minescript.player_set_orientation(player.yaw, 90)
            minescript.player_press_attack(False) 
            minescript.player_press_use(True)
            time.sleep(0.02) 
            minescript.player_press_jump(True)
            time.sleep(0.3)
            minescript.player_press_jump(False) 
            minescript.player_press_use(False)
    
    minescript.player_set_orientation(player.yaw, pitch=30)
    minescript.echo(f'{ore.capitalize()}s SUCCESSFULLY collected')
    return minescript.player_press_attack(False) 
        


def main():
    time.sleep(0.5)
    mineToNegative58()
    while True:
        nearby_diamonds_coords = searchForOres()
        clusters_of_ores = clusters(nearby_diamonds_coords)
        best_cluster = priorityGroup(clusters_of_ores)
        goToTarget(best_cluster['center'])
        mineOresAndGoBack(best_cluster['coords'])


if __name__ == '__main__':
    main()