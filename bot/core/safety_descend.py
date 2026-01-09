import time

import minescript as m
import bot.core.movement as move
import bot.core.constants as C
from bot.core.player import player

#Going down safety
def scanEnvironment(max_depth:int=7) -> tuple[bool, bool]:
    px, py, pz = player.x, player.y, player.z

    pos1 = (px - 1, py - max_depth, pz - 1)
    pos2 = (px + 1, py, pz + 1)
    
    m.await_loaded_region(px - 2, pz - 2, px + 2, pz + 2)
    region = m.get_block_region(pos1, pos2)
    
    lava = False
    water = False
    
    if m.getblock(px, C.Y_LEVEL_LAVA_PUDDLE, pz).startswith("minecraft:lava"):
        lava = True

    for dy in range(1, -max_depth - 1, -1):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                
                block = region.get_block(px + dx, py + dy, pz + dz)
                
                if (not block): continue
                
                if block.startswith("minecraft:lava"):
                    lava = True
                
                if dy in (-1, 0, 1) and block.startswith("minecraft:water"):
                    water = True 
                    
    return lava, water


def inWater() -> None:
    
    def aroundCheck() -> bool:  #
        blocks_around = set()
        for dx, dz in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            bx, by, bz = player.x + dx, player.y, player.z + dz
            if (not m.getblock(bx, by, bz).startswith("minecraft:water")):
                blocks_around.add((bx, bz))
        return (len(blocks_around) < 2) 
    
    m.echo('Player IS in WATER!!!')
    while m.player_get_targeted_block(2) == None: # Player in floor level
        m.player_press_sneak(True)
        time.sleep(C.ONE_TICK_TIME)
        
    move.goToCenter()
    
    m.player_press_attack(True) 
    while (m.player_get_targeted_block(2) == None) or (aroundCheck()):
        time.sleep(C.ONE_TICK_TIME * 2)
    
    move.StopMovement(using=True)

    while (not player.main_hand_item in C.BLOCKS_ITEM):
        m.player_inventory_select_slot(C.BLOCKS_SLOT)
    
    time.sleep(C.ONE_TICK_TIME * 3)
    BLOCK_POSITIONS = [( 1,  0,  0), ( 1,  1,  0), 
                       ( 0,  0,  1), ( 0,  1,  1), 
                       (-1,  0,  0), (-1,  1,  0),
                       ( 0,  0, -1), ( 0,  1, -1)]
    
    for dx, dy, dz in BLOCK_POSITIONS:
        bx, by, bz = player.x + dx, player.y + dy, player.z + dz
 
        while m.getblock(bx, by, bz).startswith("minecraft:water"):
            m.player_look_at(bx + C.COORDS_OFFSET, by, bz + C.COORDS_OFFSET)
            time.sleep(C.ONE_TICK_TIME)
    
    bx, by, bz = player.x, player.y + 2, player.z
    
    m.player_press_jump(True)
    time.sleep(C.ONE_TICK_TIME*11)
    m.player_press_jump(False)
    
    m.player_press_sneak(True)
    m.player_set_orientation(player.yaw, C.PITCH_LOOK_INCLINED_UP)
    
    while m.get_block(bx, by, bz).startswith("minecraft:water"):
        time.sleep(C.ONE_TICK_TIME * 2)

    m.player_inventory_select_slot(C.WATER_BUCKET_SLOT)
    time.sleep(C.ONE_TICK_TIME * 6)
    m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
    
    while m.getblock(player.x, player.y, player.z).startswith('minecraft:water'):
        time.sleep(C.ONE_TICK_TIME)
    
    move.StopMovement()    
        
    m.echo('Player IS NOT more in WATER :D')
    m.player_inventory_select_slot(C.PICKAXE_SLOT)


def closeToLava() -> None: ######Improve
    m.echo('Player CLOSE to LAVA!!!')
    m.player_press_sneak(True) 
    m.player_set_orientation(player.yaw, 20) 
    m.player_press_forward(True)
    time.sleep(5)
    m.player_press_forward(False)
    m.echo('Player IS NOT more close to LAVA :D')
    move.goToCenter()


def waterDrop() -> None:
    m.echo('FALLING!!!')
    m.player_press_attack(False)
    
    try: 
        while (not player.main_hand_item.startswith("minecraft:water")):
            m.player_inventory_select_slot(C.WATER_BUCKET_SLOT)
    except: m.player_inventory_select_slot(C.WATER_BUCKET_SLOT)

    while (player.y_velocity < C.FALLING_Y_VEL[0]):
        m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
        m.player_press_use(True)
        time.sleep(C.ONE_TICK_TIME / 2)
    m.player_press_use(False) 
    
 
    while (not player.main_hand_item.startswith('minecraft:water')) and \
          (m.getblock(player.x, player.y, player.z)).startswith('minecraft:water'):
        m.player_press_use(True)
        time.sleep(C.ONE_TICK_TIME)
        
    m.player_press_use(False)
    m.player_inventory_select_slot(C.PICKAXE_SLOT)
    time.sleep(C.ONE_TICK_TIME*2)
    
    m.echo('Water Clutch!')
    move.goToCenter()


def finalizeDescent() -> None:
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
    
    m.player_set_orientation(player.yaw, C.PITCH_LOOK_INCLINED_UP) 
    m.player_press_attack(False) 
    m.player_inventory_select_slot(C.BLOCKS_SLOT)
    m.player_press_use(True)
    time.sleep(C.ONE_TICK_TIME*6)
    
    m.player_press_use(False)
    m.player_set_orientation(player.yaw, C.PITCH_LOOK_AHEAD)
    
    m.echo(f'At y level {player.y}')  # Arrive at y -58
            