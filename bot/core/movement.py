import time
import math

import minescript as m
import bot.core.minescript_extra as m_extra
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
    if round(math.hypot(player.x_velocity, player.z_velocity),6) > C.MAX_WALKING_VEL:
        m.player_press_sprint(True)
        time.sleep(C.ONE_TICK_TIME)
        
    m.player_press_forward(False)
    m.player_press_backward(True)
    time.sleep(C.ONE_TICK_TIME * 4)
    m.player_press_backward(False)   
    

def stuck_y() -> None:
    if (not m.player_get_targeted_block(3)):

        if ((m.player_get_targeted_block(5)) and \
            (m.player_get_targeted_block()[0] != m.getblock(player.x, player.y - 1, player.z)) and \
            (C.GROUND_Y_VEL[0] <= player.y_velocity <= C.GROUND_Y_VEL[1])):
            
            m_extra.tap_key(m.player_press_sneak)
            m.player_press_backward(True) 
            m.player_press_left(True)
            time.sleep(C.ONE_TICK_TIME * 4)
            
            StopMovement()
            goToCenter()
        
        m.player_press_attack(True)
      
      
def stuck_x(yaw:float):
    if (round(player.x_velocity, 3) == C.STANDING_X_Z_VEL) and (round(player.z_velocity, 3) == C.STANDING_X_Z_VEL):
        if not m.player_get_targeted_block(3):
            m.player_press_forward(False)
            goToCenter(yaw, C.PITCH_LOOK_INCLINED_DOWN)
            m.player_press_attack(True)


def finalizeDescent(target_y:int = C.STOP_Y_LEVEL, first_time:bool = False) -> None:
    if player.y == target_y:
        pass
    elif player.y > target_y:
        StopMovement(mining=True)
        m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
        while player.y > target_y:
            stuck_y()
            time.sleep(C.ONE_TICK_TIME)
    else: 
        while player.y < target_y:
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_UP)
            m_extra.select_slot(C.PICKAXE_SLOT, C.PICKAXES)
            m.player_press_attack(True)
            
            while m.player_get_targeted_block(1) != None:
                time.sleep(C.ONE_TICK_TIME) 
            m.player_press_attack(False)
            
            m_extra.select_slot(C.BLOCKS_SLOT, C.BLOCKS_ITEM)
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
            
            bx, by, bz = player.x, player.y, player.z
            while m.getblock(bx, by, bz).endswith("air") or m.getblock(bx, by, bz).endswith("gravel"):
                m_extra.tap_key(m.player_press_jump)
                m.player_press_use(True)
            m.player_press_use(False)
        
    if first_time:
        StopMovement()
        m_extra.select_slot(C.BLOCKS_SLOT, C.BLOCKS_ITEM)
        
        while m.getblock(player.x, player.y + 2, player.z).endswith("air"):
            m_extra.tap_key(m.player_press_use)
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_INCLINED_UP) 
        m.player_press_use(False)
        
        m.echo(f'At Y-level {player.y}')  # Arrive at y -58
    
      
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
    
    StopMovement()
    
    m.player_press_sneak(True) 
    m.player_set_orientation(yaw, pitch)
    
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

    StopMovement()
    
    
def goToTarget(path:list[tuple], target_coord:tuple[int] = None) -> None:
    
    def checkFloor() -> None:
        if m.getblock(path_x, FLOOR_Y_LEVEL, path_z).endswith("air"):
            bx, by, bz = (axis + C.COORDS_OFFSET for axis in (path_x, FLOOR_Y_LEVEL, path_z))
            m.player_look_at(bx, by, bz)
            
            StopMovement(using=True)
            m_extra.select_slot(C.BLOCKS_SLOT, C.BLOCKS_ITEM)
            
            while m.getblock(path_x, FLOOR_Y_LEVEL, path_z).endswith("air"):
                time.sleep(C.ONE_TICK_TIME)
                
            StopMovement()
            m_extra.select_slot(C.PICKAXE_SLOT, C.PICKAXES)
    
    def miningPath(yaw:float):
        m.player_set_orientation(yaw, C.PITCH_LOOK_AHEAD)
        m.player_press_forward(True)
        stuck_x(yaw)
        time.sleep(C.ONE_TICK_TIME / 2)

    MINING_Y_LEVEL = (player.y + 1, player.y) # (-57, -58) when finding diamonds | any if lava
    FLOOR_Y_LEVEL = player.y - 1 # -59 when finding diamonds | any if lava
    target_y = target_coord[1] if target_coord else player.y
    
    while path:
        path_x, path_z = path.pop()
        
        m_extra.select_slot(C.PICKAXE_SLOT, C.PICKAXES)
        
        for path_y in MINING_Y_LEVEL:
            if m.getblock(path_x, path_y, path_z).endswith("air"):
                m.player_press_attack(False)
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
        
    finalizeDescent(target_y)
    
    
    


 
    
    
        
