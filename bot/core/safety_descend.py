import time

import minescript as m
import bot.core.minescript_extra as m_extra
import bot.core.movement as move
import bot.core.constants as C
from bot.core import player


#Going down safety
def scanEnvironment(max_depth:int=14) -> tuple[bool, bool]:
    px, py, pz = player.x, player.y, player.z
    
    pos1 = (px + 1, py + 1, pz + 1)
    pos2 = (px - 1, max(py - max_depth, -64), pz - 1)
    
    m.await_loaded_region(px - 2, pz - 2, px + 2, pz + 2)
    region = m.get_block_region(pos1, pos2)
    
    lava = False
    water = False
    
    if m.getblock(px, C.Y_LEVEL_LAVA_PUDDLE, pz).startswith("minecraft:lava"):
        lava = True

    for dy in range(1, -max_depth - 1, -1):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                
                block = region.get_block(px + dx, max(py + dy, -64), pz + dz)
                
                if (not block): continue
                
                if block.startswith("minecraft:lava"):
                    lava = True
                
                if (dy in (-1, 0, 1)) and (dx == 0) and (dz == 0) and \
                   (block.startswith("minecraft:water")):
                    water = True 
                    
    return lava, water


def inWater() -> None:
    
    def aroundCheck() -> bool: # Make sure is in the floor
        blocks_around = set()
        for dx, dz in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            bx, by, bz = player.x + dx, player.y, player.z + dz
            if (not m.getblock(bx, by, bz).startswith("minecraft:water")):
                blocks_around.add((bx, bz))
        return (len(blocks_around) < 3) 
    
    m.echo(f"{m_extra.txt_clr('y')}Player IS in {m_extra.txt_clr('b')}WATER{m_extra.txt_clr('y')}!")
    while m.player_get_targeted_block(2) == None: # Player in floor level
        m.player_press_sneak(True)
        time.sleep(C.ONE_TICK_TIME)
        
    move.goToCenter()
    
    m.player_press_attack(True) 
    while (m.player_get_targeted_block(2) == None) or (aroundCheck()):
        time.sleep(C.ONE_TICK_TIME * 2)
    
    move.StopMovement(using=True)

    m_extra.select_slot(C.BLOCKS_SLOT, C.BLOCKS_ITEM)
    
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
    time.sleep(C.ONE_TICK_TIME * 11)
    m.player_press_jump(False)
    
    m.player_press_sneak(True)
    m.player_set_orientation(player.yaw, C.PITCH_LOOK_INCLINED_UP)
    
    while m.get_block(bx, by, bz).startswith("minecraft:water"):
        time.sleep(C.ONE_TICK_TIME * 2)

    m_extra.select_slot(C.WATER_BUCKET_SLOT, C.BUCKETS_ITEM)
    time.sleep(C.ONE_TICK_TIME * 6)
    m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
    
    while m.getblock(player.x, player.y, player.z).startswith("minecraft:water"):
        time.sleep(C.ONE_TICK_TIME)
    
    move.StopMovement()    
        
    m.echo(f"{m_extra.txt_clr('g')}Player IS NOT more in {m_extra.txt_clr('b')}WATER")
    m_extra.select_slot(C.PICKAXE_SLOT, C.PICKAXES)


def closeToLava() -> None:
    m.echo(f"{m_extra.txt_clr('y')}Player CLOSE to {m_extra.txt_clr('r')}LAVA{m_extra.txt_clr('y')}!")
    
    path = []
    
    m.player_set_orientation(player.yaw, C.PITCH_LOOK_INCLINED_DOWN)
    while m.player_get_targeted_block(1) == None:
        m.player_press_forward(True)
    move.StopMovement(mining=True)
    
    target_coords = m.player_get_targeted_block(2).position
    dx, _, dz = tuple(
        coord1 - coord2 for coord1, coord2 in zip(target_coords, (player.x, player.y, player.z))
        )
    
    for i in range(4, 1, -1):
        bx, bz = player.x + dx * i, player.z + dz * i
        path.append((bx, bz))
    
    move.goToTarget(path)
    


def waterDrop() -> None:
    m.echo(f"{m_extra.txt_clr('y')}FALLING!!!")
    
    move.StopMovement()
    m.player_press_sneak(True)
    
    m.player_inventory_select_slot(C.WATER_BUCKET_SLOT)
    m_extra.select_slot(C.WATER_BUCKET_SLOT, C.BUCKETS_ITEM)

    while (player.y_vel < C.FALLING_Y_VEL[0]):
        m.player_set_orientation(player.yaw, C.PITCH_LOOK_DOWN)
        m_extra.tap_key(m.player_press_use, C.ONE_TICK_TIME / 4)
    
    time.sleep(C.ONE_TICK_TIME * 3)
    if (not player.main_hand_item.startswith("minecraft:water")):
        m_extra.tap_key(m.player_press_use, C.ONE_TICK_TIME)
        

    move.StopMovement()
    m_extra.select_slot(C.PICKAXE_SLOT, C.PICKAXES)
    
    m.echo(f"{m_extra.txt_clr('g')}Water Clutch!")
    move.goToCenter()

            