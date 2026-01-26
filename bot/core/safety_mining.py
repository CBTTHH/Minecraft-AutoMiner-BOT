import time
import math

import minescript as m
import bot.core.minescript_extra as m_extra
import bot.core.constants as C

def lavaSave(): 
    m.echo(f"{m_extra.txt_clr('r')}PLAYER IN LAVA {m_extra.txt_clr('y')}- AUTO PLACING {m_extra.txt_clr('b')}WATER")
    m_extra.toggle_all(False)
    m.player_press_use(True)
    m_extra.select_slot(C.BLOCKS_SLOT, C.BLOCKS_ITEM)
    
    safe_block_coord:tuple = None
    ABOVE_DY = 2
    AROUND_BLOCKS = ((-1, ABOVE_DY,  0),
                     ( 1, ABOVE_DY,  0),
                     ( 0, ABOVE_DY,  0),
                     ( 0, ABOVE_DY, -1),
                     ( 0, ABOVE_DY,  1),)
    
    while True:
        x, y, z = map(math.floor, m.player().position)
        
        for dx, dy, dz in AROUND_BLOCKS:
            bx, by, bz = x + dx, y + dy, z + dz
            
            if m.getblock(bx, by, bz) in C.BLOCKS_ITEM:
                safe_block_coord = bx, by, bz
                continue
        break
    
    if safe_block_coord:
        m.player_look_at(safe_block_coord[0] + C.COORDS_OFFSET, 
                         safe_block_coord[1] + C.COORDS_OFFSET, 
                         safe_block_coord[2] + C.COORDS_OFFSET)
    else: m.player_set_orientation(yaw=m.player().yaw, pitch=C.PITCH_LOOK_INCLINED_UP)
        
    while m.getblock(x, y + ABOVE_DY, z).endswith("air"):
        time.sleep(C.ONE_TICK_TIME)
    
    m_extra.toggle_all(False)
    m.player_set_orientation(m.player().yaw, C.PITCH_LOOK_UP)
    m_extra.select_slot(C.WATER_BUCKET_SLOT, C.BUCKETS_ITEM)
    m_extra.tap_key(m.player_press_use)
    
    time.sleep(C.ONE_TICK_TIME * 24)
    
    while m.player_hand_items().main_hand.get("item").startswith("minecraft:bucket"):
        m_extra.tap_key(m.player_press_use)
    
    m_extra.eat_food()
    m_extra.toggle_all(False)