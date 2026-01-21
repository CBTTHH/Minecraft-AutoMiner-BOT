from time import sleep

import minescript as m
import bot.core.movement as move
import bot.core.safety_descend as safety_descend
import bot.core.constants as C
from bot.core.player import player

def run():
    descend()

def descend():
    m.echo('Mining to y level -58')
    move.disableSprint()
    move.goToCenter()
    m.player_inventory_select_slot(C.PICKAXE_SLOT)
    
    while (not player.stop_tracking):
        if player.y <= C.STOP_Y_LEVEL:
            move.finalizeDescent(first_time=True)
            break
        
        m.player_press_attack(True)
        
        move.stuck_y()
        lava, water = safety_descend.scanEnvironment()
        
        if (player.y_velocity < C.FALLING_Y_VEL[0]) and (not water):
            safety_descend.waterDrop()
            
        if lava:
            safety_descend.closeToLava()
        
        if water:
            safety_descend.inWater()
        
        sleep(C.ONE_TICK_TIME / 2)
        
