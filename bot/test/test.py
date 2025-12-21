import minescript, time, math
import bot.core.movement as move
import bot.core.searching as searching
import bot.core.decision as decision
import bot.core.mining as mining
import bot.core.safety as safety
import bot.core.constants as C
from bot.core.player import player

def run_player_info(tick=C.ONE_TICK_TIME): #✅
    while not player.stop_tracking:
        health = player.health
        pos_x, pos_y, pos_z = player.x, player.y, player.z 
        vel_x, vel_y, vel_z = player.x_velocity, player.y_velocity, player.z_velocity
        yaw, pitch = player.yaw, player.pitch
        targeted_block = player.targeted_block
        targeted_entity = player.targeted_entity
        main_hand_item = player.main_hand_item
        
        minescript.echo("-"*45)
        minescript.echo(f"HEALTH: {health}")
        minescript.echo(f"POSITION: {pos_x}, {pos_y}, {pos_z}")
        minescript.echo(f"VELOCITY: {vel_x:.5f}, {vel_y:.5f}, {vel_z:.5f}")
        minescript.echo(f"YAW & PITCH: ({yaw}, {pitch})")
        minescript.echo(f"TARGETED BLOCK: {targeted_block}")
        minescript.echo(f"TARGETED ENTITY: {targeted_entity}")
        minescript.echo(f"MAIN HAND ITEM: {main_hand_item}")
        minescript.echo("-"*45)
        time.sleep(tick)
    
def run_safety_check(safety_type:str): # ❕
    """
    :param safety_type: Enter first letter: "i" for inWater, "c" for closeToLava, or "w" for "waterDrop"
    :type safety_type: str
    """
    
    if safety_type[0].lower() == 'i':
        safety.inWater()
    elif safety_type[0].lower() == "c":
        safety.closeToLava()
    elif safety_type[0].lower() == "w":
        safety.waterDrop()
    else:
        minescript.echo("Unknown safety check")
    
def run_movement_check(): # ✅
    # move.disableSprint()
    move.goToCenter()
    move.goToTarget((3010, -59, -3225))
    
def run_searching_check():
    # searching.searchForOres()
    searching.searchForOres()
    
    
if __name__ == "__main__":
    # run_player_info() 
    # run_movement_check()
    # run_safety_check()
    start_time = time.perf_counter()
    run_searching_check()   
    end_time = time.perf_counter()
    
    minescript.echo(f"It took {end_time-start_time:.5f} seconds")