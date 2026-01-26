import time

import minescript as m
import bot.core.minescript_extra as m_extra
import bot.core.searching as searching
import bot.core.decision as decision
import bot.core.constants as C
from bot.core import player


def run():
    player.auto_tracking = False
    
    while (not player.stop_tracking):
        
        if player.y > C.MAX_SCAN_Y_LEVEL:
            m.echo(f"{m_extra.txt_clr('y')}Player needs to be under y-level {C.MAX_SCAN_Y_LEVEL} - preventing high resources consumption...")
            player.stop_tracking = True
            break
        
        ore_coords, _, _ = searching.searchOresLava(caption=False)
        cluster = searching.clusters(ore_coords)
        best_cluster = decision.priorityGroup(cluster, caption=False)
        
        cx, cy, cz = best_cluster.get("center", None)
        n_diamonds = len(best_cluster['coords'])
        distance = best_cluster.get('distance', float("inf"))
        direction = decision.direction((cx, cy, cz))
        
        follow = f"{direction[0]} - {direction[1]} - {direction[2]}"
        diamond_pos = f"{m_extra.txt_clr('a')}{cx}, {cy}, {cz}"
        diamond_info = f"{m_extra.txt_clr('p')}Quantity: {n_diamonds}, Distance: {distance}"
        pos = f"{m_extra.txt_clr('p')}{player.x}, {player.y}, {player.z}"
        vel = f"{m_extra.txt_clr('p')}{player.x_vel:.5f}, {player.y_vel:.5f}, {player.z_vel:.5f}"
        y_p = f"{m_extra.txt_clr('p')}{player.yaw:.2f}, {player.pitch:.2f}"
        
        m.echo("\n"*5)
        m.echo("-"*45)
        m.echo(f"FOLLOW:         {follow}")
        m.echo(f"DIAMOND POS:  {diamond_pos:<10}")
        m.echo(f"DIAMOND INFO: {diamond_info:<10}")
        m.echo(f"POSITION:       {pos:<10}")
        m.echo(f"VELOCITY:       {vel:<10}")
        m.echo(f"YAW & PITCH:   {y_p:<10}")
        m.echo("-"*45)
        m.echo("\n"*5)
        
        time.sleep(C.ONE_TICK_TIME * 7)
        


if __name__ == "__main__":
    run()