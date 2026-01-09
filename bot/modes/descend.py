import bot.core.safety_descend as safety_descend
import bot.core.constants as C
from bot.core.player import player

def run():
    descend()

def descend():
    while not player.stop_tracking:
        lava, water = safety_descend.scanEnvironment()
        
        if (player.y_velocity < C.FALLING_Y_VEL[0]) and (not water):
            safety_descend.waterDrop()
            
        if lava:
            safety_descend.closeToLava()
        
        if water:
            safety_descend.inWater()
        
        if player.y <= C.STOP_Y_LEVEL:
            safety_descend.finalizeDescent()
            break
