import time
import math
import threading

import minescript as m
import bot.core.safety_mining as safety
import bot.core.constants as C

class PlayerTracker:
    def __init__(self):
        self.health = 20
        
        self.x, self.y, self.z = map(math.floor, m.player().position)
        self.yaw, self.pitch = C.YAW_FACING_EAST, C.PITCH_LOOK_AHEAD
        self.x_velocity, self.y_velocity, self.z_velocity = 0, 0, 0
        
        self.targeted_block = None
        self.targeted_entity = None
        self.main_hand_item = None
        self.off_hand_item = None
        
        self.lava_around = set()
        
        #Threads
        self.stop_tracking = False
        self.player_info_update_thread = threading.Thread(target=self.player_info) 
        self.tool_update_thread = threading.Thread(target=self.tool_in_main_hand)
        self.hazard_detection_update_thread = threading.Thread(target=self.hazard_detection)
        self.auto_stop_update_thread = threading.Thread(target=self.auto_stop)
        self.player_info_update_thread.daemon = True
        self.tool_update_thread.daemon = True
        self.hazard_detection_update_thread.daemon = True
        self.auto_stop_update_thread.daemon = True
        self.player_info_update_thread.start()
        self.tool_update_thread.start()
        self.hazard_detection_update_thread.start()
        self.auto_stop_update_thread.start()
    
    
    def player_info(self):
        while not self.stop_tracking:
            
            self.health = m.player().health
            
            self.x, self.y, self.z = map(math.floor, m.player().position)
            
            yaw = ((m.player().yaw + 180) % 360) - 180
            pitch = ((m.player().pitch + 90) % 180) - 90

            if yaw >= -135 and yaw < -45: self.yaw = C.YAW_FACING_EAST
            elif yaw >= -45 and yaw <= 45: self.yaw = C.YAW_FACING_SOUTH
            elif yaw > 45 and yaw < 135: self.yaw = C.YAW_FACING_WEST
            else: self.yaw = C.YAW_FACING_NORTH
            self.pitch = pitch

            self.x_velocity, self.y_velocity, self.z_velocity = m.player().velocity
            
            time.sleep(C.ONE_TICK_TIME)
            
    
    def tool_in_main_hand(self):
        
        while not self.stop_tracking:
            
            self.targeted_block = m.player_get_targeted_block(5)
            
            main_hand_item = m.player_hand_items().main_hand
            off_hand_item = m.player_hand_items().off_hand
            
            self.main_hand_item = main_hand_item.get('item') if main_hand_item else None
            self.off_hand_item = off_hand_item.get("item") if off_hand_item else None
                
            
            if self.main_hand_item:
                try:
                    if self.main_hand_item in C.HAND_ITEMS:
                        time.sleep(C.ONE_TICK_TIME*2)
                        continue
        
                    if m.player_get_targeted_block(5):
                        if m.player_get_targeted_block(5)[3] in C.SHOVEL_BREAKABLE: 
                            m.player_inventory_select_slot(C.SHOVEL_SLOT)
                        else: 
                            m.player_inventory_select_slot(C.PICKAXE_SLOT)
                    time.sleep(C.ONE_TICK_TIME*2)
                    
                except Exception as e:
                    m.echo('Error:', e)
                    time.sleep(C.ONE_TICK_TIME*2)
                    self.stop_tracking = True
                    
                
    def hazard_detection(self):
        while not self.stop_tracking:
            self.targeted_entity = m.player_get_targeted_entity(5)
            
            px, py, pz = player.x, player.y, player.z
            pos1 = (px - 1, py - 1, pz -1)
            pos2 = (px + 1, py + 2, pz + 1)
            
            m.await_loaded_region(px - 2, pz - 2, px + 2, pz + 2)
            region = m.get_block_region(pos1, pos2)
            
            for dx, dy, dz in C.BLOCKS_AROUND_PLAYER:
     
                        x, y, z = px + dx, py + dy, pz + dz
                        
                        block = region.get_block(x, y, z)
                        if block and block.startswith("minecraft:lava"):
                            self.lava_around.add((x, y, z))

            time.sleep(C.ONE_TICK_TIME*5)


    def auto_stop(self):
        
        def stop() -> None:
            m.echo('Stopping script')
            
            m.player_press_right(False)
            m.player_press_forward(False)
            m.player_press_left(False)
            m.player_press_backward(False)
            m.player_press_sneak(False)
            m.player_press_jump(False)
            m.player_press_attack(False)
            m.player_press_use(False)
            
            self.stop_tracking = True
            self.player_info_update_thread.join(timeout=1)
            self.tool_update_thread.join(timeout=1)
            self.hazard_detection_update_thread.join(timeout=1)
            
            running_scripts = m.job_info()
            for job in running_scripts:
                m.execute(f"\killjob {job.job_id}")
        
        while not self.stop_tracking:
            
            time.sleep(C.ONE_TICK_TIME*5)
            
            if self.targeted_entity:
                m.echo("ENTITY DETECTED")
                stop()
                
            elif self.lava_around:
                m.echo("VERY CLOSE TO LAVA")
                safety.lavaSave()
                stop()
            
            elif (self.main_hand_item and (self.main_hand_item.endswith("sword") or self.main_hand_item.endswith("_axe"))):
                m.echo("PLAYER PULLET OUT HIS COMBAT WEAPON")
                stop()
                
            elif self.health <= C.MIN_HEALTH:
                m.echo("PLAYER HAS LOW HEALTH... RECOVER AND TRY AGAIN")
                stop()
                
                
player = PlayerTracker()
time.sleep(0.5) # Loading threads (prevent crashing)