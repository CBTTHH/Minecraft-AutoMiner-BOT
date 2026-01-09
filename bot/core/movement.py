import time
import math

import minescript as m
import bot.core.constants as C
from bot.core.player import player

def StopMovement(mining:bool=False, using:bool=False) -> None:
    m.player_press_right(False)
    m.player_press_forward(False)
    m.player_press_left(False)
    m.player_press_backward(False)
    
    m.player_press_sneak(False)
    m.player_press_jump(False)
    
    m.player_press_attack(mining)
    m.player_press_use(using)
    

def disableSprint() -> None:
    m.player_press_forward(True)
    
    time.sleep(C.ONE_TICK_TIME*5)
    m.echo(round(math.hypot(player.x_velocity, player.z_velocity),6))
    if round(math.hypot(player.x_velocity, player.z_velocity),6) > C.MAX_WALKING_VEL:
        m.echo("work")
        m.player_press_sprint(True)
        time.sleep(C.ONE_TICK_TIME)
        
    m.player_press_forward(False)
    m.player_press_backward(True)
    time.sleep(C.ONE_TICK_TIME*4)
    m.player_press_backward(False)   
    

def stuck_y() -> None:
    if not m.player_get_targeted_block(3):
        time.sleep(C.ONE_TICK_TIME)

        if m.player_get_targeted_block(5)[0] != [player.x, player.y, player.z] and \
           (C.GROUND_Y_VEL[0] <= player.y_velocity <= C.GROUND_Y_VEL[1]):
            
            m.player_press_backward(True) 
            m.player_press_left(True)
            time.sleep(C.ONE_TICK_TIME*4)
            
            StopMovement()
            goToCenter()
      
        
def goToCenter(yaw:float=None, pitch:float=C.PITCH_LOOK_DOWN) -> None:
    if yaw is None:
        yaw = player.yaw
        
    x_center = math.floor(m.player().position[0]) + C.COORDS_OFFSET
    z_center = math.floor(m.player().position[2]) + C.COORDS_OFFSET
    
    m.player_press_sneak(True) 
    m.player_set_orientation(yaw, pitch)
    
    if m.player().position[0] > x_center:
        while (round(m.player().position[0], 3) - C.MAX_CENTER_OFFSET[1]) > x_center:
            if yaw == C.YAW_FACING_EAST: m.player_press_backward(True)
            elif yaw == C.YAW_FACING_SOUTH: m.player_press_right(True)
            elif yaw == C.YAW_FACING_WEST: m.player_press_forward(True)
            else: m.player_press_left(True)
            
    else:
        while (round(m.player().position[0], 3) + C.MAX_CENTER_OFFSET[1]) < x_center:
            if yaw == C.YAW_FACING_EAST: m.player_press_forward(True)
            elif yaw == C.YAW_FACING_SOUTH: m.player_press_left(True)
            elif yaw == C.YAW_FACING_WEST: m.player_press_backward(True)
            else: m.player_press_right(True)
    
    if pitch == C.PITCH_LOOK_INCLINED_DOWN: 
        stuck_y()
    StopMovement()
    
    
    m.player_press_sneak(True) and m.player_set_orientation(yaw, pitch)
    
    if m.player().position[2] > z_center:
        while (round(m.player().position[2], 3) - C.MAX_CENTER_OFFSET[1]) > z_center:
            if yaw == C.YAW_FACING_EAST: m.player_press_left(True)
            elif yaw == C.YAW_FACING_SOUTH: m.player_press_backward(True)
            elif yaw == C.YAW_FACING_WEST: m.player_press_right(True)
            else: m.player_press_forward(True)
            
    else:
        while (round(m.player().position[2], 3) + C.MAX_CENTER_OFFSET[1]) < z_center:
            if yaw == C.YAW_FACING_EAST: m.player_press_right(True)
            elif yaw == C.YAW_FACING_SOUTH: m.player_press_forward(True)
            elif yaw == C.YAW_FACING_WEST: m.player_press_left(True)
            else: m.player_press_backward(True)
            
    if pitch == C.PITCH_LOOK_INCLINED_DOWN: 
        stuck_y() 
    StopMovement()
    
    
def goToTarget(best_cluster:dict, path:list[tuple]) -> None:
    
    def checkFloor() -> None:
        if m.getblock(path_x, FLOOR_Y_LEVEL, path_z).endswith("air"):
            StopMovement(using=True)
            
            while m.player_hand_items().main_hand.get("item").endswith("axe"):
                m.player_inventory_select_slot(C.BLOCKS_SLOT)
            
            bx, by, bz = (axis + C.COORDS_OFFSET for axis in (path_x, FLOOR_Y_LEVEL, path_z))
            m.player_look_at(bx, by, bz)
            
            while m.getblock(path_x, FLOOR_Y_LEVEL, path_z).endswith("air"):
                time.sleep(C.ONE_TICK_TIME)
                
            StopMovement()
            m.player_inventory_select_slot(C.PICKAXE_SLOT)
    
    def miningPath(yaw:float):
        m.player_set_orientation(yaw, C.PITCH_LOOK_INCLINED_DOWN)
        m.player_press_forward(True)
        time.sleep(C.ONE_TICK_TIME)

    MINING_Y_LEVEL = (-57, -58)
    FLOOR_Y_LEVEL = -59
    target_y = best_cluster["center"][1]
    
    while path:
        path_x, path_z = path.pop()
        
        for path_y in MINING_Y_LEVEL:
            if m.getblock(path_x, path_y, path_z).endswith("air"):
                continue
            
            m.player_look_at(path_x + C.COORDS_OFFSET, path_y + C.COORDS_OFFSET, path_z + C.COORDS_OFFSET)
            
            m.player_press_attack(True)
            while (not m.getblock(path_x, path_y, path_z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME)
        
        checkFloor()
        StopMovement(mining=True)
        
        if player.x > path_x:
            yaw = C.YAW_FACING_WEST
            while (round(player.x,3) - C.MAX_CENTER_OFFSET[1]) > path_x:
                miningPath(yaw)
                
        else:
            yaw = C.YAW_FACING_EAST
            while (round(player.x,3) + C.MAX_CENTER_OFFSET[1]) < path_x: 
                miningPath(yaw)
            
        if player.z > path_z:
            yaw = C.YAW_FACING_NORTH
            while (round(player.z,3) - C.MAX_CENTER_OFFSET[1]) > path_z:
                miningPath(yaw)
                
        else:
            yaw = C.YAW_FACING_SOUTH
            while (round(player.z,3) + C.MAX_CENTER_OFFSET[1]) < path_z:
                miningPath(yaw)

        StopMovement()
    
    goToCenter(pitch=C.PITCH_LOOK_INCLINED_DOWN)
        
    if player.y > target_y:
        m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
        while player.y > target_y:
            time.sleep(C.ONE_TICK_TIME)
            
    else: 
        while player.y < target_y:
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_UP)
            m.player_inventory_select_slot(C.PICKAXE_SLOT)
            m.player_press_attack(True)
            
            while m.player_get_targeted_block(1) != None:
                time.sleep(C.ONE_TICK_TIME) 
            
            StopMovement(mining=False, using=True)
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
             
            m.player_inventory_select_slot(C.BLOCKS_SLOT) 
            time.sleep(C.ONE_TICK_TIME) 
            
            m.player_press_jump(True)
            time.sleep(C.ONE_TICK_TIME*4)
            StopMovement()

    goToCenter(pitch=C.PITCH_LOOK_INCLINED_DOWN)
    
    
    


 
    
    
        
