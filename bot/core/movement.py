import time
import math

import minescript as m
import bot.core.minescript_extra as m_extra
import bot.core.constants as C
from bot.core import player

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
    if (round(math.hypot(player.x_vel, player.z_vel)) > C.MAX_WALKING_VEL):
        m.player_press_sprint(True)
        time.sleep(C.ONE_TICK_TIME)
        
    m.player_press_forward(False)
    m.player_press_backward(True)
    time.sleep(C.ONE_TICK_TIME * 4)
    m.player_press_backward(False)   
    

def stuck_y() -> None:
    if (m.player_get_targeted_block(3)):
        return
    if ((m.player_get_targeted_block(5)) and \
        (m.player_get_targeted_block()[0] != m.getblock(player.x, player.y - 1, player.z)) and \
        (C.GROUND_Y_VEL[0] <= player.y_vel <= C.GROUND_Y_VEL[1])):
        
        m_extra.tap_key(m.player_press_sneak)
        m.player_press_backward(True) 
        m.player_press_left(True)
        time.sleep(C.ONE_TICK_TIME * 4)
        
        StopMovement()
        goToCenter()
    
    m.player_press_attack(True)
      
      
def update_stuck_timer(floor_y_level=C.FLOOR_Y_LEVEL):
    current_pos = (player.x, player.y, player.z)

    if (current_pos != player._last_pos):
        player._last_pos = current_pos
        player._last_time_movement = time.time()
        return False

    target_block = m.player_get_targeted_block(2.25)
    if (target_block) and (target_block.position[1] != floor_y_level):
        return False

    return (time.time() - player._last_time_movement > C.STUCK_TIMEOUT)


def recover_from_stuck(yaw, floor_y_level):
    m.player_press_forward(False)
    goToCenter(yaw, C.PITCH_LOOK_INCLINED_DOWN)

    target_block = m.player_get_targeted_block()
    if target_block and target_block.position[1] != floor_y_level:
        m.player_press_attack(True)
    else:
        m.player_press_attack(False)
    player._last_pos = (0, 0, 0)


def finalizeDescent(target_y:int = C.STOP_Y_LEVEL, first_time:bool = False) -> None:
    if player.y == target_y:
        m.player_press_attack(False)
        pass
    elif player.y > target_y:
        StopMovement(mining=True)
        m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
        while player.y > target_y:
            stuck_y()
            time.sleep(C.ONE_TICK_TIME)
    else: 
        while player.y < max(target_y - 1, C.STOP_Y_LEVEL):
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_UP)
            m_extra.select_slot(C.PICKAXE_SLOT, C.PICKAXES)
            m.player_press_attack(True)
            
            while m.player_get_targeted_block(1) != None:
                time.sleep(C.ONE_TICK_TIME) 
            m.player_press_attack(False)
            
            m_extra.select_slot(C.BLOCKS_SLOT, C.BLOCKS_ITEM)
            m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
            
            bx, by, bz = player.x, player.y, player.z
            if m.getblock(bx, by, bz).endswith("gravel"):
                m_extra.tap_key(m.player_press_jump)
                
            while m.getblock(bx, by, bz).endswith("air"):
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
        
        m.echo(f"At y-level {m_extra.txt_clr('p')}{player.y}")  # Arrive at y -58
    
      
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
    
    def checkFloor(floor_y_level=C.FLOOR_Y_LEVEL) -> None:
        if m.getblock(path_x, floor_y_level, path_z).endswith("air"):
            bx, by, bz = (axis + C.COORDS_OFFSET for axis in (path_x, C.FLOOR_Y_LEVEL, path_z))
            m.player_look_at(bx, by, bz)
            
            StopMovement(using=True)
            m_extra.select_slot(C.BLOCKS_SLOT, C.BLOCKS_ITEM)
            
            while m.getblock(path_x, C.FLOOR_Y_LEVEL, path_z).endswith("air"):
                time.sleep(C.ONE_TICK_TIME)
                
            StopMovement()
            m_extra.select_slot(C.PICKAXE_SLOT, C.PICKAXES)
    
    def miningPath(yaw=player.yaw, pitch=C.PITCH_LOOK_DOWN, path:list[tuple]=[], floor_y_level=C.FLOOR_Y_LEVEL):
        bx, by, bz = m.player_get_targeted_block().position
        m.player_press_attack(True) if (by != floor_y_level) and ((bx, bz) in path) else m.player_press_attack(False)
        
        m.player_set_orientation(yaw, pitch)
        m.player_press_forward(True)
        
        if update_stuck_timer(floor_y_level):
            recover_from_stuck(yaw, floor_y_level)

    target_y = target_coord[1] if target_coord else player.y
    floor_y_level = player.y - 1
    mining_y_level = (player.y + 1, player.y)
    static_path = frozenset(path)
    
    while path:
        path_x, path_z = path.pop()
        
        m_extra.select_slot(C.PICKAXE_SLOT, C.PICKAXES)
        
        for path_y in mining_y_level:
            if m.getblock(path_x, path_y, path_z).endswith("air"):
                m.player_press_attack(False)
                continue
            
            m.player_look_at(path_x + C.COORDS_OFFSET, path_y + C.COORDS_OFFSET, path_z + C.COORDS_OFFSET)
            
            m.player_press_attack(True)
            while (not m.getblock(path_x, path_y, path_z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME)
        
        checkFloor(floor_y_level)
        StopMovement()
        
        if player.x > path_x:
            yaw = C.YAW_FACING_WEST
            while (round(player.x, 3) - C.MAX_CENTER_OFFSET[1]) > path_x:
                miningPath(yaw, C.PITCH_LOOK_AHEAD, static_path, floor_y_level)
                
        else:
            yaw = C.YAW_FACING_EAST
            while (round(player.x, 3) + C.MAX_CENTER_OFFSET[1]) < path_x: 
                miningPath(yaw, C.PITCH_LOOK_AHEAD, static_path, floor_y_level)
                
        if player.z > path_z:
            yaw = C.YAW_FACING_NORTH
            while (round(player.z, 3) - C.MAX_CENTER_OFFSET[1]) > path_z:
                miningPath(yaw, C.PITCH_LOOK_AHEAD, static_path, floor_y_level)
                
        else:
            yaw = C.YAW_FACING_SOUTH
            while (round(player.z, 3) + C.MAX_CENTER_OFFSET[1]) < path_z:
                miningPath(yaw, C.PITCH_LOOK_AHEAD, static_path, floor_y_level)
           
        StopMovement()
    
    goToCenter()
    finalizeDescent(target_y)
    
    
    


 
    
    
        
