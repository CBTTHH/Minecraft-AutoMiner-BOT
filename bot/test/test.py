import time
import pyperclip

import minescript as m
import bot.core.movement as move
import bot.core.searching as searching
import bot.core.decision as decision
import bot.core.mining as mining
import bot.core.safety_descend as safety_descend
import bot.core.constants as C
from bot.core.player import player


def run_player_info(tick=C.ONE_TICK_TIME) -> None: #✅
    while not player.stop_tracking:
        health = player.health
        pos_x, pos_y, pos_z = player.x, player.y, player.z 
        vel_x, vel_y, vel_z = player.x_velocity, player.y_velocity, player.z_velocity
        yaw, pitch = player.yaw, player.pitch
        targeted_block = player.targeted_block
        targeted_entity = player.targeted_entity
        main_hand_item = player.main_hand_item
        off_hand_item = player.off_hand_item
        
        m.echo("-"*45)
        m.echo(f"HEALTH: {health}")
        m.echo(f"POSITION: {pos_x}, {pos_y}, {pos_z}")
        m.echo(f"VELOCITY: {vel_x:.5f}, {vel_y:.5f}, {vel_z:.5f}")
        m.echo(f"YAW & PITCH: ({yaw}, {pitch})")
        m.echo(f"TARGETED BLOCK: {targeted_block}")
        m.echo(f"TARGETED ENTITY: {targeted_entity}")
        m.echo(f"MAIN HAND ITEM: {main_hand_item}")
        m.echo(f"OFF HAND ITEM: {off_hand_item}")
        m.echo("-"*45)
        time.sleep(tick)
    
    
def run_safety(safety_type:str) -> None: # ❕
    """
    :param safety_type: Enter first letter: "i" for inWater, "c" for closeToLava, or "w" for "waterDrop"
    :type safety_type: str
    """
    
    if safety_type[0].lower() == 'i':
        safety_descend.inWater()
    elif safety_type[0].lower() == "c":
        safety_descend.closeToLava()
    elif safety_type[0].lower() == "w":
        safety_descend.waterDrop()
    else:
        m.echo("Unknown safety check")
    
    
def run_movement() -> None: # ✅
    move.disableSprint()
    move.goToCenter()
    move.goToTarget((3010, -59, -3225))
    
    
def run_searching_and_decision() -> tuple[dict, list]: # ✅
    start_time = time.perf_counter()
    diamond_coords, walkable_2d_coords = searching.searchOresLava()
    end_time = time.perf_counter()
    time1 = end_time - start_time
    
    start_time_cluster = time.perf_counter()
    cluster = searching.clusters(diamond_coords)
    end_time_cluster = time.perf_counter()
    time2 = end_time_cluster - start_time_cluster
    
    start_time_decision = time.perf_counter()
    best_cluster = decision.priorityGroup(cluster)
    end_time_decision = time.perf_counter()
    time3 = end_time_decision - start_time_decision
    
    start_time_path_finding = time.perf_counter()
    (x, _, z) = best_cluster["center"]
    goal = (x, z)
    path = decision.AStarPathFinder(walkable_2d_coords, goal)
    pyperclip.copy(path)
    end_time_path_finding = time.perf_counter()
    time4 = end_time_path_finding - start_time_path_finding
    
    # m.echo(f"Old took: {end_time_old-start_time_old}")    
    m.echo(f"Current took: {time1}")
    m.echo(f"Clustering took: {time2}")
    m.echo(f"Decision took: {time3}")
    m.echo(f"Path finding took: {time4}")
    m.echo(f"Total time: {time1+time2+time3+time4}")
    
    return best_cluster, path
    
    
def run_searching_movement() -> None:
    best_cluster, path = run_searching_and_decision()
    move.goToTarget(best_cluster, path)
    
    
if __name__ == "__main__":
    # run_player_info()
    run_safety("w")
    # run_movement()
    # run_searching_and_decision()   
    
    
     
