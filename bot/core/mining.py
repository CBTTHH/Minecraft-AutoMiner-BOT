import minescript, time
import bot.core.movement as move
import bot.core.constants as C

def mineCluster(best_cluster_coords:list[tuple[int]], ore=C.MINING_ORE):
    best_cluster_coords.sort(key=lambda coords: coords[1], reverse=True)
    minescript.player_inventory_select_slot(C.PICKAXE_SLOT)
    
    for coords in best_cluster_coords:
        x, y, z = coords
        
        minescript.player_press_attack(True)
        minescript.player_look_at(x+.5,y+.5,z+.5)
        
        while minescript.getblock(x,y,z).endswith(f'{ore}_ore'):
            time.sleep(C.ONE_TICK_TIME)
    
    minescript.player_press_forward(True) 
    minescript.player_press_jump(True)
    time.sleep(C.ONE_TICK_TIME*6)
    
    move.StopMovement()
    time.sleep(C.ONE_TICK_TIME)
    
    
