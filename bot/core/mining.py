import time

import minescript as m
import bot.core.minescript_extra as m_extra
import bot.core.movement as move
import bot.core.constants as C

def mineCluster(best_cluster_coords:list[tuple[int]], ore=C.MINING_ORE) -> None:
    best_cluster_coords.sort(key=lambda coords: coords[1], reverse=True)
    m_extra.select_slot(C.PICKAXE_SLOT, C.PICKAXES)
    
    for coords in best_cluster_coords:
        x, y, z = coords
        
        m.player_press_attack(True)
        m.player_look_at(x + .5,y + .5,z + .5)
        
        while m.getblock(x,y,z).endswith(f'{ore}_ore'):
            time.sleep(C.ONE_TICK_TIME)
    
    m.player_press_attack(False)
    m.player_press_forward(True)
    m.player_press_jump(True)
    time.sleep(C.ONE_TICK_TIME*8)
    
    move.StopMovement()
    move.goToCenter()
    
    
