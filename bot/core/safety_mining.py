import time
import math

import minescript as m
import bot.core.movement as move
import bot.core.constants as C

def lavaSave():
    m.echo("PLAYER IN LAVA - AUTO PLACING WATER")
    move.StopMovement(mining=False, using=True)
    
    x, y, z = map(math.floor, m.player().position)
    ABOVE_Y = y + 2
    
    m.player_look_at(x + C.COORDS_OFFSET, ABOVE_Y, z + C.COORDS_OFFSET)

    while m.getblock(x, ABOVE_Y, z).endswith("air"):
        m.player_inventory_select_slot(C.BLOCKS_SLOT)
        time.sleep(C.ONE_TICK_TIME)
    
    m.player_inventory_select_slot(C.WATER_BUCKET_SLOT)
    time.sleep(C.ONE_TICK_TIME*3)
    while m.player_hand_items().main_hand.get("item").endswith("water_bucket"):
        time.sleep(C.ONE_TICK_TIME)
    
    while m.player_hand_items().main_hand.get("item").startswith("minecraft:bucket"):
        time.sleep(C.ONE_TICK_TIME)
        
    m.player_inventory_select_slot(C.FOOD_SLOT)
    time.sleep(C.ONE_TICK_TIME * 32)
    move.StopMovement()