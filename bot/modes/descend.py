from time import sleep

import minescript as m
import bot.core.minescript_extra as m_extra
import bot.core.movement as move
import bot.core.safety_descend as safety_descend
import bot.core.constants as C
from bot.core import player


def run():
    player.auto_tracking = True
    
    m.echo(f"Mining to y level {m_extra.txt_clr('p')}-58")
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
        
        if (player.y_vel < C.FALLING_Y_VEL[0]) and (not water):
            safety_descend.waterDrop()
            
        if lava:
            safety_descend.closeToLava()
        
        if water:
            safety_descend.inWater()
        
        sleep(C.ONE_TICK_TIME / 2)
        


if __name__ == "__main__":
    run()
