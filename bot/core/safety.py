import minescript, time
import bot.core.movement as move
import bot.core.constants as C
from bot.core.player import player

#Going down safety
def inWater():
    minescript.echo('Player IS in WATER!!!')
    
    while minescript.player_get_targeted_block(2) == None:
        minescript.player_press_sneak(True) ### make player go down 3 blocks
        
    move.goToCenter()
    time.sleep(C.ONE_TICK_TIME*2)
 
    minescript.echo("change slot")
    minescript.player_inventory_select_slot(C.BLOCKS_SLOT)
    minescript.player_press_use(True)
    time.sleep(C.ONE_TICK_TIME*2)
    
    ###Change so the player go down until everything is cover up
    # block_positions = [(player.x+1.5, player.y-1, player.z+.5), (player.x+1.5, player.y+1, player.z+.5), 
    #                    (player.x+.5, player.y-1, player.z+1.5), (player.x+.5, player.y+1, player.z+1.5), 
    #                    (player.x-1.5, player.y-1, player.z+.5), (player.x-1.5, player.y+1, player.z+.5), 
    #                    (player.x+.5, player.y-1, player.z-1.5), (player.x+.5, player.y+1, player.z-1.5)]
    
    # for position in block_positions:
    #     x, y, z = position
    #     minescript.player_look_at(x,y,z)
    #     time.sleep(C.ONE_TICK_TIME*10) ### check if block was placed or not or solve above
        
    # minescript.player_press_jump(True)
    # time.sleep(C.ONE_TICK_TIME*4)
    # minescript.player_press_jump(False)
    # minescript.player_set_orientation(player.yaw, C.PITCH_LOOK_INCLINED_DOWN)
    # time.sleep(0.65)
    # minescript.player_inventory_select_slot(C.WATER_BUCKET_SLOT)
    # time.sleep(0.3)
    # minescript.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
    # time.sleep(0.4)
    # minescript.player_press_use(False)
    
    # while not player.main_hand_item.startswith('minecraft:water'):
    #     minescript.player_press_use(True)
    #     time.sleep(0.05)
    #     minescript.player_press_use(False)
        
    minescript.echo('Player IS NOT more in WATER :D')
    minescript.player_inventory_select_slot(C.PICKAXE_SLOT)


def closeToLava(): ######Improve
    minescript.echo('Player CLOSE to LAVA!!!')
    minescript.player_press_sneak(True) 
    minescript.player_set_orientation(player.yaw, 20) 
    minescript.player_press_forward(True)
    time.sleep(5)
    minescript.player_press_forward(False)###########
    
    if minescript.getblock(player.x, player.y-7, player.z).startswith('minecraft:lava') or \
       minescript.getblock(player.x, player.y-4, player.z).startswith('minecraft:lava') or \
       minescript.getblock(player.x, C.Y_LEVEL_LAVA_PUDDLE, player.z).startswith('minecraft:lava'):
        return closeToLava()
    
    minescript.echo('Player IS NOT more close to LAVA :D')
    move.goToCenter()#####


def waterDrop():
    minescript.echo('FALLING!!!')
    minescript.player_press_attack(False)
    minescript.player_inventory_select_slot(C.WATER_BUCKET_SLOT)
    
    while player.y_velocity < C.FALLING_Y_VEL[0] :
        minescript.player_press_use(True)
        time.sleep(C.ONE_TICK_TIME)
    minescript.player_press_use(False) 
    time.sleep(C.ONE_TICK_TIME)
    
    while not minescript.player_hand_items().main_hand['item'].startswith('minecraft:water'):
        minescript.player_press_use(True)
        time.sleep(C.ONE_TICK_TIME)
        
    minescript.player_press_use(False)
    minescript.player_inventory_select_slot(C.PICKAXE_SLOT)
    time.sleep(C.ONE_TICK_TIME*2)
    
    minescript.echo('Water Clutch!')
    move.goToCenter()
    

#Mining and searching diamonds safety