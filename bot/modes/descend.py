import minescript, time
import bot.core.movement as move
import bot.core.safety as safety
import bot.core.constants as C
from bot.core.player import player

def run():
    descend()

def descend(first_instance=False):
    if first_instance: minescript.echo(f'Mining to y level {C.STOP_Y_LEVEL}')
    move.goToCenter()
    
    while True:
        time.sleep(C.ONE_TICK_TIME)
        minescript.player_press_attack(True)
        
        if (player.y_velocity < C.FALLING_Y_VEL[0]) and (not minescript.getblock(player.x, player.y-4, player.z).startswith('minecraft:water')) and (not minescript.getblock(player.x, player.y-2, player.z).startswith('minecraft:water')):
            safety.waterDrop()
            continue
            
        if minescript.getblock(player.x, player.y-7, player.z).startswith('minecraft:lava') or minescript.getblock(player.x, player.y-4, player.z).startswith('minecraft:lava') or minescript.getblock(player.x, C.Y_LEVEL_LAVA_PUDDLE, player.z).startswith('minecraft:lava'):
            safety.closeToLava()
            continue
            
        if  minescript.getblock(player.x, player.y, player.z).startswith('minecraft:water'):
            safety.inWater()
            continue
        
        if not minescript.player_get_targeted_block(3):
            time.sleep(C.ONE_TICK_TIME)
            move.stuck_y()
            continue

        if player.y <= C.STOP_Y_LEVEL:
            while player.y < C.STOP_Y_LEVEL:
                minescript.player_set_orientation(player.yaw, C.PITCH_LOOK_UP)
                minescript.player_inventory_select_slot(C.PICKAXE_SLOT)
                
                while minescript.player_get_targeted_block(1) != None:
                    minescript.player_press_attack(True)
                    
                minescript.player_inventory_select_slot() 
                minescript.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
                
                minescript.player_press_attack(False)
                minescript.player_press_use(True)
                time.sleep(C.ONE_TICK_TIME) 
                
                minescript.player_press_jump(True)
                time.sleep(C.ONE_TICK_TIME*6)
                move.StopMovement()
            break
    
    if first_instance: 
        minescript.player_set_orientation(player.yaw, C.PITCH_LOOK_INCLINED_UP) 
        minescript.player_press_attack(False) 
        minescript.player_inventory_select_slot(C.BLOCKS_SLOT)
        minescript.player_press_use(True)
        time.sleep(C.ONE_TICK_TIME*6)
        
        minescript.player_press_use(False)
        minescript.player_set_orientation(player.yaw, C.PITCH_LOOK_AHEAD)
        
        minescript.echo(f'At y level {player.y}')  # Arrive at y -58
        