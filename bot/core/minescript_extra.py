import time
from typing import Iterable

import minescript as m
import bot.core.constants as C

def select_slot(slot:int ,items:Iterable[str]) -> None:
    """
    Makes 100% sure that slot item is selected in the game
    
    :param slot: player slot from 0 to 8
    :type slot: int
    :param item_name: items selected (complete item name)
    :type item_name: Iterable[str]
    """
    
    while ((not m.player_hand_items().main_hand) or \
           (m.player_hand_items().main_hand.get("item") not in items)):
        m.player_inventory_select_slot(slot)
        time.sleep(C.ONE_TICK_TIME)
        
        
def tap_key(action_key) -> None:
    action_key(True)
    time.sleep(C.ONE_TICK_TIME)
    action_key(False)