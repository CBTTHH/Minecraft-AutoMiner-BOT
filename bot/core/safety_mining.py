import time
import math

import minescript as m
import bot.core.minescript_extra as m_extra
import bot.core.movement as move
import bot.core.constants as C

def lavaSave(): 
    m.echo("PLAYER IN LAVA - AUTO PLACING WATER")
    move.StopMovement(mining=False, using=True)
    
    x, y, z = map(math.floor, m.player().position)
    ABOVE_Y = y + 2
    
    m_extra.select_slot(C.BLOCKS_SLOT, C.BLOCKS_ITEM)
    # TODO: make lava safe to check for blocks around not only one part
    m.player_look_at(x + C.COORDS_OFFSET, ABOVE_Y, z + C.COORDS_OFFSET)
    while m.getblock(x, ABOVE_Y, z).endswith("air"):
        time.sleep(C.ONE_TICK_TIME)
    
    move.StopMovement()
    m_extra.select_slot(C.WATER_BUCKET_SLOT, C.BUCKETS_ITEM)
    m_extra.tap_key(m.player_press_use)
    
    time.sleep(C.ONE_TICK_TIME * 12)
    
    while m.player_hand_items().main_hand.get("item").startswith("minecraft:bucket"):
        m_extra.tap_key(m.player_press_use)
        
    m_extra.select_slot(C.FOOD_SLOT, C.FOOD_ITEMS)
    m.player_press_use(True)
    time.sleep(C.ONE_TICK_TIME * 32)
    move.StopMovement()