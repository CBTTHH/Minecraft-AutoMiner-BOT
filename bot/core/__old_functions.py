## MOVEMENT
import time

import minescript as m
import bot.core.movement as move
import bot.core.safety_descend as safety_descend
import bot.core.constants as C
from player import player

def stuck_x(yaw:float):
    if (player.z_velocity == C.STANDING_X_Z_VEL) and (player.x_velocity == C.STANDING_X_Z_VEL):
        if not m.player_get_targeted_block(3):
            m.player_press_forward(False)
            move.goToCenter(yaw, C.PITCH_LOOK_INCLINED_DOWN)

def goToTargetOld(best_cluster_center:tuple):
    target_x, target_y, target_z = best_cluster_center
    
    move.goToCenter(pitch=C.PITCH_LOOK_INCLINED_DOWN)
    time.sleep(C.ONE_TICK_TIME)
    m.player_press_attack(True) 
    m.player_inventory_select_slot(C.PICKAXE_SLOT)
    
    quadrant = 1 if target_x - player.x > 0 and target_z - player.z > 0 else \
               2 if target_x - player.x > 0 and target_z - player.z < 0 else \
               3 if target_x - player.x < 0 and target_z - player.z < 0 else \
               4
    
    m.echo(quadrant)
    if quadrant == 1:
        m.echo('Working')
        yaw_1 = C.YAW_FACING_EAST
        yaw_2 = C.YAW_FACING_SOUTH
        while (round(player.x, 3) + C.MAX_CENTER_OFFSET[1]) < target_x and (round(player.z, 3) + C.MAX_CENTER_OFFSET[1]) < target_z:
            m.player_set_orientation(yaw_1, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_forward(True)
            m.player_press_attack(True)

            while (not m.getblock(player.x + 1, player.y, player.z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
            m.player_set_orientation(yaw_2, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_attack(True)
            m.player_press_forward(True)
            
            while not m.getblock(player.x, player.y, player.z + 1).endswith("air"):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
    elif quadrant == 2:
        m.echo('Working')
        yaw_1 = C.YAW_FACING_EAST
        yaw_2 = C.YAW_FACING_NORTH
        while (round(player.x, 3) + C.MAX_CENTER_OFFSET[1]) < target_x and (round(player.z, 3) + C.MAX_CENTER_OFFSET[1]) > target_z:
            m.player_set_orientation(yaw_1, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_forward(True)
            m.player_press_attack(True)

            while (not m.getblock(player.x + 1, player.y, player.z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
            m.player_set_orientation(yaw_2, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_attack(True)
            m.player_press_forward(True)
            
            while not m.getblock(player.x, player.y, player.z - 1).endswith("air"):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
    
    elif quadrant == 3:
        m.echo('Working')
        yaw_1 = C.YAW_FACING_WEST
        yaw_2 = C.YAW_FACING_NORTH
        while (round(player.x, 3) + C.MAX_CENTER_OFFSET[1]) > target_x and (round(player.z, 3) + C.MAX_CENTER_OFFSET[1]) > target_z:
            m.player_set_orientation(yaw_1, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_forward(True)
            m.player_press_attack(True)

            while (not m.getblock(player.x - 1, player.y, player.z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
            m.player_set_orientation(yaw_2, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_attack(True)
            m.player_press_forward(True)
            
            while not m.getblock(player.x, player.y, player.z - 1).endswith("air"):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
    
    else:
        m.echo('Working')
        yaw_1 = C.YAW_FACING_WEST
        yaw_2 = C.YAW_FACING_SOUTH
        while (round(player.x, 3) + C.MAX_CENTER_OFFSET[1]) > target_x and (round(player.z, 3) + C.MAX_CENTER_OFFSET[1]) < target_z:
            m.player_set_orientation(yaw_1, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_forward(True)
            m.player_press_attack(True)

            while (not m.getblock(player.x - 1, player.y, player.z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
            m.player_set_orientation(yaw_2, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_attack(True)
            m.player_press_forward(True)
            
            while not m.getblock(player.x, player.y, player.z + 1).endswith("air"):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
    
    if player.x > target_x:
        yaw = C.YAW_FACING_WEST
        while (round(player.x,3) - C.MAX_CENTER_OFFSET[1]) > target_x:
            m.player_set_orientation(yaw, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_forward(True)
            time.sleep(C.ONE_TICK_TIME)
            stuck_x(yaw)
            
    else:
        yaw = C.YAW_FACING_EAST
        while (round(player.x,3) + C.MAX_CENTER_OFFSET[1]) < target_x: 
            m.player_set_orientation(yaw, C.PITCH_LOOK_INCLINED_DOWN) 
            time.sleep(C.ONE_TICK_TIME)
            m.player_press_forward(True)
            stuck_x(yaw)
                
    move.StopMovement(mining=True)
    move.goToCenter(pitch=C.PITCH_LOOK_INCLINED_DOWN)
    time.sleep(C.ONE_TICK_TIME)
    
    m.player_press_attack(True)
        
    if player.z > target_z:
        yaw = C.YAW_FACING_NORTH
        while (round(player.z,3) - C.MAX_CENTER_OFFSET[1]) > target_z:
            m.player_set_orientation(yaw, C.PITCH_LOOK_INCLINED_DOWN)
            time.sleep(C.ONE_TICK_TIME)
            m.player_press_forward(True)
            stuck_x(yaw)
            
    else:
        yaw = C.YAW_FACING_SOUTH
        while (round(player.z,3) + C.MAX_CENTER_OFFSET[1]) < target_z:
            m.player_set_orientation(yaw, C.PITCH_LOOK_INCLINED_DOWN) 
            time.sleep(C.ONE_TICK_TIME)
            m.player_press_forward(True)
            stuck_x(yaw)

    move.StopMovement(mining=True)
    move.goToCenter(yaw, C.PITCH_LOOK_INCLINED_DOWN)
    time.sleep(C.ONE_TICK_TIME)
    
    m.player_press_attack(True)
    
    if player.y > target_y:
        while player.y > target_y:
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
            
    else: 
        while player.y < target_y:
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_UP)
            m.player_inventory_select_slot(C.PICKAXE_SLOT)
            
            while m.player_get_targeted_block(1) != None:
                m.player_press_attack(True)
                
            m.player_inventory_select_slot(C.BLOCKS_SLOT) 
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
            
            m.player_press_attack(False) 
            m.player_press_use(True)
            time.sleep(C.ONE_TICK_TIME) 
            
            m.player_press_jump(True)
            time.sleep(C.ONE_TICK_TIME*6)
            
    move.StopMovement()
    move.goToCenter(pitch=C.PITCH_LOOK_INCLINED_DOWN)
    
    
## SEARCHING
def searchForOresOld(searching_coords:tuple[int,int,int] = None, r=5, ore='diamond') -> set: 
    
    def search_nearby(bx,by,bz): # Searches blocks around a diamond ore
        for dx in [-1, 0 , 1]:
            for dy in [-1, 0 , 1]:
                for dz in [-1, 0 , 1]:
                    
                    _y = by + dy
                    if _y <= C.INVALID_Y_LEVEL[0]:
                        continue
                    
                    _x, _z = bx + dx, bz + dz
                    if m.getblock(_x,_y,_z).endswith(f'{ore}_ore'): 
                        coord_neighbor = (_x, _y, _z)
                        if coord_neighbor not in coords_with_ores:
                            coords_with_ores.add(coord_neighbor) 
                            cache.add(coord_neighbor)
                            search_nearby(_x,_y,_z)
                        
    # Facing east: xyz normal coordinate plane
    if not searching_coords:
        sx, sy, sz = player.x, player.y, player.z
    else:
        sx, sy, sz = searching_coords
        
    coords_with_ores = set()
    cache = set()
    prev_r = 0
    min_y = C.INVALID_Y_LEVEL[0] + 1
    min_dy = max(min_y - sy, -r)
    
    while True:          
    
        for dx in range(-r, r + 1):
            for dy in range(min_dy, r + 1):
                for dz in range(-r, r + 1):
                    
                    if max(abs(dx), abs(dy), abs(dz)) <= prev_r: # Shell expansion
                        continue
                    
                    x, y, z = sx + dx, sy + dy, sz + dz
                    
                    if (x, y, z) in cache: 
                        continue
                    
                    cache.add((x, y, z))
                    
                    if (x + y + z) & 2 == 0: 
                        if m.getblock(x,y,z).endswith(f'{ore}_ore'):
                            search_nearby(x,y,z)
    
        if coords_with_ores:
            m.echo("Old:")
            m.echo(coords_with_ores, len(coords_with_ores))
            return coords_with_ores
        
        prev_r = r
        r += 2
        m.echo(f'No {ore}s nearby, increasing searching radius to a offset of {r}')
        
        

## DESCEND
def descend(first_instance=False):
    if first_instance: m.echo(f'Mining to y level {C.STOP_Y_LEVEL}')
    move.goToCenter()
    
    while player.stop_tracking:
        time.sleep(C.ONE_TICK_TIME)
        m.player_press_attack(True)
        
        if (player.y_velocity < C.FALLING_Y_VEL[0]) and (not m.getblock(player.x, player.y-4, player.z).startswith('minecraft:water')) and (not m.getblock(player.x, player.y-2, player.z).startswith('minecraft:water')):
            safety_descend.waterDrop()
            continue
            
        if m.getblock(player.x, player.y-7, player.z).startswith('minecraft:lava') or m.getblock(player.x, player.y-4, player.z).startswith('minecraft:lava') or m.getblock(player.x, C.Y_LEVEL_LAVA_PUDDLE, player.z).startswith('minecraft:lava'):
            safety_descend.closeToLava()
            continue
            
        if  m.getblock(player.x, player.y, player.z).startswith('minecraft:water'):
            safety_descend.inWater()
            continue
        
        if not m.player_get_targeted_block(3):
            time.sleep(C.ONE_TICK_TIME)
            move.stuck_y()
            continue

        if player.y <= C.STOP_Y_LEVEL:
            while player.y < C.STOP_Y_LEVEL:
                m.player_set_orientation(player.yaw, C.PITCH_LOOK_UP)
                m.player_inventory_select_slot(C.PICKAXE_SLOT)
                m.player_press_attack(True)
                
                while m.player_get_targeted_block(1) != None:
                    time.sleep(C.ONE_TICK_TIME) 
                
                move.StopMovement(mining=False, using=True)
                m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
                
                m.player_inventory_select_slot(C.BLOCKS_SLOT) 
                time.sleep(C.ONE_TICK_TIME) 
                
                m.player_press_jump(True)
                time.sleep(C.ONE_TICK_TIME*4)
                move.StopMovement()
            break
    
    if first_instance: 
        m.player_set_orientation(player.yaw, C.PITCH_LOOK_INCLINED_UP) 
        m.player_press_attack(False) 
        m.player_inventory_select_slot(C.BLOCKS_SLOT)
        m.player_press_use(True)
        time.sleep(C.ONE_TICK_TIME*6)
        
        m.player_press_use(False)
        m.player_set_orientation(player.yaw, C.PITCH_LOOK_AHEAD)
        
        m.echo(f'At y level {player.y}')  # Arrive at y -58
        