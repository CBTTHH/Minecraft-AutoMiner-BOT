import minescript, time, math
import bot.core.constants as C
from bot.core.player import player

def stuck_y():
    if not minescript.player_get_targeted_block(3):
        time.sleep(C.ONE_TICK_TIME)

        if minescript.player_get_targeted_block(5)[0] != [player.x, player.y, player.z] and \
           (C.GROUND_Y_VEL[0] <= player.y_velocity <= C.GROUND_Y_VEL[1]):
            
            minescript.player_press_backward(True) 
            minescript.player_press_left(True)
            time.sleep(C.ONE_TICK_TIME*4)
            
            StopMovement()
            goToCenter()


def stuck_x(yaw):
    if (player.z_velocity == C.STANDING_X_Z_VEL) and (player.x_velocity == C.STANDING_X_Z_VEL):
        if not minescript.player_get_targeted_block(3):
            minescript.player_press_forward(False)
            goToCenter(yaw, C.PITCH_LOOK_INCLINED_DOWN)
      
        
def goToCenter(yaw=None, pitch=C.PITCH_LOOK_DOWN):
    if yaw is None:
        yaw = player.yaw
        
    x_center = math.floor(minescript.player().position[0]) + C.COORDS_OFFSET
    z_center = math.floor(minescript.player().position[2]) + C.COORDS_OFFSET
    
    minescript.player_press_sneak(True) 
    minescript.player_set_orientation(yaw, pitch)
    
    if minescript.player().position[0] > x_center:
        while (round(minescript.player().position[0],3) - C.MAX_CENTER_OFFSET[1]) > x_center:
            if yaw == C.YAW_FACING_EAST: minescript.player_press_backward(True)
            elif yaw == C.YAW_FACING_SOUTH: minescript.player_press_right(True)
            elif yaw == C.YAW_FACING_WEST: minescript.player_press_forward(True)
            else: minescript.player_press_left(True)
            
    else:
        while (round(minescript.player().position[0],3) + C.MAX_CENTER_OFFSET[1]) < x_center:
            if yaw == C.YAW_FACING_EAST: minescript.player_press_forward(True)
            elif yaw == C.YAW_FACING_SOUTH: minescript.player_press_left(True)
            elif yaw == C.YAW_FACING_WEST: minescript.player_press_backward(True)
            else: minescript.player_press_right(True)
    
    if pitch == C.PITCH_LOOK_INCLINED_DOWN: stuck_y()
    StopMovement()
    
    
    minescript.player_press_sneak(True) and minescript.player_set_orientation(yaw, pitch)
    
    if minescript.player().position[2] > z_center:
        while (round(minescript.player().position[2],3) - C.MAX_CENTER_OFFSET[1]) > z_center:
            if yaw == C.YAW_FACING_EAST: minescript.player_press_left(True)
            elif yaw == C.YAW_FACING_SOUTH: minescript.player_press_backward(True)
            elif yaw == C.YAW_FACING_WEST: minescript.player_press_right(True)
            else: minescript.player_press_forward(True)
            
    else:
        while (round(minescript.player().position[2],3) + C.MAX_CENTER_OFFSET[1]) < z_center:
            if yaw == C.YAW_FACING_EAST: minescript.player_press_right(True)
            elif yaw == C.YAW_FACING_SOUTH: minescript.player_press_forward(True)
            elif yaw == C.YAW_FACING_WEST: minescript.player_press_left(True)
            else: minescript.player_press_backward(True)
            
    if pitch == C.PITCH_LOOK_INCLINED_DOWN: stuck_y() 
    StopMovement()
    
    
def goToTarget(best_cluster_center:tuple):
    target_x, target_y, target_z = best_cluster_center
    
    goToCenter(pitch=C.PITCH_LOOK_INCLINED_DOWN)
    time.sleep(C.ONE_TICK_TIME)
    minescript.player_press_attack(True) 
    minescript.player_inventory_select_slot(C.PICKAXE_SLOT)
    
    quadrant = 1 if target_x - player.x > 0 and target_z - player.z > 0 else \
               2 if target_x - player.x > 0 and target_z - player.z < 0 else \
               3 if target_x - player.x < 0 and target_z - player.z < 0 else \
               4
    
    minescript.echo(quadrant)
    if quadrant == 1:
        minescript.echo('Working')
        yaw_1 = C.YAW_FACING_EAST
        yaw_2 = C.YAW_FACING_SOUTH
        while (round(player.x, 3) + C.MAX_CENTER_OFFSET[1]) < target_x and (round(player.z, 3) + C.MAX_CENTER_OFFSET[1]) < target_z:
            minescript.player_set_orientation(yaw_1, C.PITCH_LOOK_INCLINED_DOWN)
            minescript.player_press_forward(True)
            minescript.player_press_attack(True)

            while (not minescript.getblock(player.x + 1, player.y, player.z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
            minescript.player_set_orientation(yaw_2, C.PITCH_LOOK_INCLINED_DOWN)
            minescript.player_press_attack(True)
            minescript.player_press_forward(True)
            
            while not minescript.getblock(player.x, player.y, player.z + 1).endswith("air"):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
    elif quadrant == 2:
        minescript.echo('Working')
        yaw_1 = C.YAW_FACING_EAST
        yaw_2 = C.YAW_FACING_NORTH
        while (round(player.x, 3) + C.MAX_CENTER_OFFSET[1]) < target_x and (round(player.z, 3) + C.MAX_CENTER_OFFSET[1]) > target_z:
            minescript.player_set_orientation(yaw_1, C.PITCH_LOOK_INCLINED_DOWN)
            minescript.player_press_forward(True)
            minescript.player_press_attack(True)

            while (not minescript.getblock(player.x + 1, player.y, player.z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
            minescript.player_set_orientation(yaw_2, C.PITCH_LOOK_INCLINED_DOWN)
            minescript.player_press_attack(True)
            minescript.player_press_forward(True)
            
            while not minescript.getblock(player.x, player.y, player.z - 1).endswith("air"):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
    
    elif quadrant == 3:
        minescript.echo('Working')
        yaw_1 = C.YAW_FACING_WEST
        yaw_2 = C.YAW_FACING_NORTH
        while (round(player.x, 3) + C.MAX_CENTER_OFFSET[1]) > target_x and (round(player.z, 3) + C.MAX_CENTER_OFFSET[1]) > target_z:
            minescript.player_set_orientation(yaw_1, C.PITCH_LOOK_INCLINED_DOWN)
            minescript.player_press_forward(True)
            minescript.player_press_attack(True)

            while (not minescript.getblock(player.x - 1, player.y, player.z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
            minescript.player_set_orientation(yaw_2, C.PITCH_LOOK_INCLINED_DOWN)
            minescript.player_press_attack(True)
            minescript.player_press_forward(True)
            
            while not minescript.getblock(player.x, player.y, player.z - 1).endswith("air"):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
    
    else:
        minescript.echo('Working')
        yaw_1 = C.YAW_FACING_WEST
        yaw_2 = C.YAW_FACING_SOUTH
        while (round(player.x, 3) + C.MAX_CENTER_OFFSET[1]) > target_x and (round(player.z, 3) + C.MAX_CENTER_OFFSET[1]) < target_z:
            minescript.player_set_orientation(yaw_1, C.PITCH_LOOK_INCLINED_DOWN)
            minescript.player_press_forward(True)
            minescript.player_press_attack(True)

            while (not minescript.getblock(player.x - 1, player.y, player.z).endswith("air")):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
            
            minescript.player_set_orientation(yaw_2, C.PITCH_LOOK_INCLINED_DOWN)
            minescript.player_press_attack(True)
            minescript.player_press_forward(True)
            
            while not minescript.getblock(player.x, player.y, player.z + 1).endswith("air"):
                time.sleep(C.ONE_TICK_TIME * 2)
            time.sleep(C.ONE_TICK_TIME * 2)
    
    if player.x > target_x:
        yaw = C.YAW_FACING_WEST
        while (round(player.x,3) - C.MAX_CENTER_OFFSET[1]) > target_x:
            minescript.player_set_orientation(yaw, C.PITCH_LOOK_INCLINED_DOWN)
            minescript.player_press_forward(True)
            time.sleep(C.ONE_TICK_TIME)
            stuck_x(yaw)
            
    else:
        yaw = C.YAW_FACING_EAST
        while (round(player.x,3) + C.MAX_CENTER_OFFSET[1]) < target_x: 
            minescript.player_set_orientation(yaw, C.PITCH_LOOK_INCLINED_DOWN) 
            time.sleep(C.ONE_TICK_TIME)
            minescript.player_press_forward(True)
            stuck_x(yaw)
                
    StopMovement(mining=True)
    goToCenter(pitch=C.PITCH_LOOK_INCLINED_DOWN)
    time.sleep(C.ONE_TICK_TIME)
    
    minescript.player_press_attack(True)
        
    if player.z > target_z:
        yaw = C.YAW_FACING_NORTH
        while (round(player.z,3) - C.MAX_CENTER_OFFSET[1]) > target_z:
            minescript.player_set_orientation(yaw, C.PITCH_LOOK_INCLINED_DOWN)
            time.sleep(C.ONE_TICK_TIME)
            minescript.player_press_forward(True)
            stuck_x(yaw)
            
    else:
        yaw = C.YAW_FACING_SOUTH
        while (round(player.z,3) + C.MAX_CENTER_OFFSET[1]) < target_z:
            minescript.player_set_orientation(yaw, C.PITCH_LOOK_INCLINED_DOWN) 
            time.sleep(C.ONE_TICK_TIME)
            minescript.player_press_forward(True)
            stuck_x(yaw)

    StopMovement(mining=True)
    goToCenter(yaw, C.PITCH_LOOK_INCLINED_DOWN)
    time.sleep(C.ONE_TICK_TIME)
    
    minescript.player_press_attack(True)
    
    if player.y > target_y:
        while player.y > target_y:
            minescript.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
            
    else: 
        while player.y < target_y:
            minescript.player_set_orientation(player.yaw, C.PITCH_LOOK_UP)
            minescript.player_inventory_select_slot(C.PICKAXE_SLOT)
            
            while minescript.player_get_targeted_block(1) != None:
                minescript.player_press_attack(True)
                
            minescript.player_inventory_select_slot(C.BLOCKS_SLOT) 
            minescript.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
            
            minescript.player_press_attack(False) 
            minescript.player_press_use(True)
            time.sleep(C.ONE_TICK_TIME) 
            
            minescript.player_press_jump(True)
            time.sleep(C.ONE_TICK_TIME*6)
            
    StopMovement()
    goToCenter(pitch=C.PITCH_LOOK_INCLINED_DOWN)

def StopMovement(mining=False, using=False):
    minescript.player_press_right(False)
    minescript.player_press_forward(False)
    minescript.player_press_left(False)
    minescript.player_press_backward(False)
    
    minescript.player_press_sneak(False)
    minescript.player_press_jump(False)
    
    minescript.player_press_attack(mining)
    minescript.player_press_use(using)
    

def disableSprint():
    minescript.player_press_forward(True)
    
    time.sleep(C.ONE_TICK_TIME*5)
    minescript.echo(round(math.hypot(player.x_velocity, player.z_velocity),6))
    if round(math.hypot(player.x_velocity, player.z_velocity),6) > C.MAX_WALKING_VEL:
        minescript.echo("work")
        minescript.player_press_sprint(True)
        time.sleep(C.ONE_TICK_TIME)
        
    minescript.player_press_forward(False)
    minescript.player_press_backward(True)
    time.sleep(C.ONE_TICK_TIME*4)
    minescript.player_press_backward(False)    
    
    
        
