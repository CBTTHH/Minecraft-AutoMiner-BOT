import time, minescript, math, threading
import bot.core.constants as C

class PlayerTracker:
    def __init__(self):
        self.health = 20
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = C.YAW_FACING_EAST
        self.pitch = C.PITCH_LOOK_AHEAD
        self.x_velocity, self.y_velocity, self.z_velocity = 0, 0, 0
        self.targeted_block = None
        self.targeted_entity = None
        self.lava_around = []
        self.main_hand_item = None
        
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
            
            self.health = minescript.player().health
            
            px, py, pz = minescript.player().position
            self.x = math.floor(px)
            self.y = math.floor(py)
            self.z = math.floor(pz)
            
            yaw = ((minescript.player().yaw + 180) % 360) - 180
            pitch = ((minescript.player().pitch + 90) % 180) - 90

            if yaw >= -135 and yaw < -45: self.yaw = C.YAW_FACING_EAST
            elif yaw >= -45 and yaw <= 45: self.yaw = C.YAW_FACING_SOUTH
            elif yaw > 45 and yaw < 135: self.yaw = C.YAW_FACING_WEST
            else: self.yaw = C.YAW_FACING_NORTH
            self.pitch = pitch

            self.x_velocity, self.y_velocity, self.z_velocity = minescript.player().velocity
            
            time.sleep(C.ONE_TICK_TIME)
            
    
    def tool_in_main_hand(self):
        shovel_blocks = {'minecraft:dirt', 
                         'minecraft:gravel', 
                         'minecraft:clay',
                         'minecraft:grass_block[snowy=false]', 
                         'minecraft:sand', 
                         'minecraft:soul_sand',}
        
        blocks = {'minecraft:cobblestone',
                  'minecraft:stone', 
                  'minecraft:cobbled_deepslate', 
                  'minecraft:deepslate',
                  'minecraft:diorite', 
                  'minecraft:granite', 
                  'minecraft:sandstone'}
        
        food = {'minecraft:cooked_beef', 
                'minecraft:cooked_chicken', 
                'minecraft:cooked_porkchop', 
                'minecraft:cooked_salmon', 
                'minecraft:golden_carrot', 
                'minecraft:golden_apple', 
                'minecraft:pumpkin_pie'}
        
        while not self.stop_tracking:
            
            self.targeted_block = minescript.player_get_targeted_block(5)
            main_hand_item = minescript.player_hand_items().main_hand
            
            if main_hand_item: 
                self.main_hand_item = main_hand_item.get('item')
            
            if self.main_hand_item:
                try:
                    if (self.main_hand_item.endswith('water_bucket')) or (self.main_hand_item in food) or \
                       (self.main_hand_item.endswith('bucket')) or(self.main_hand_item in blocks):
                        time.sleep(C.ONE_TICK_TIME*2)
                        continue
        
                    if minescript.player_get_targeted_block(5):
                        if minescript.player_get_targeted_block(5)[3] in shovel_blocks: 
                            minescript.player_inventory_select_slot(C.SHOVEL_SLOT)
                        else: 
                            minescript.player_inventory_select_slot(C.PICKAXE_SLOT)
                    time.sleep(C.ONE_TICK_TIME*2)
                    
                except Exception as e:
                    minescript.echo('Error:', e)
                    time.sleep(C.ONE_TICK_TIME*2)
                    self.stop_tracking = True
                    
                
    def hazard_detection(self):
        while not self.stop_tracking:
            
            self.targeted_entity = minescript.player_get_targeted_entity(5)
            
            lava_around = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1, 2]:
                    for dz in [-1, 0, 1]:
                        lava_around.append(minescript.getblock(self.x + dx, self.y + dy, self.z + dz).startswith("minecraft:lava"))
            self.lava_around = lava_around

            time.sleep(C.ONE_TICK_TIME*5)



    def auto_stop(self):
        def stop():
            minescript.echo('Stopping script')
            self.stop_tracking = True
            self.player_info_update_thread.join(timeout=1)
            self.tool_update_thread.join(timeout=1)
            self.hazard_detection_update_thread.join(timeout=1)
        
        while not self.stop_tracking:
            
            time.sleep(C.ONE_TICK_TIME*5)
            
            if self.targeted_entity:
                minescript.echo("ENTITY DETECTED")
                stop()
                
            elif any(self.lava_around):
                minescript.echo("VERY CLOSE TO LAVA")
                stop()
            
            elif (self.main_hand_item and (self.main_hand_item.endswith("sword") or self.main_hand_item.endswith("_axe"))):
                minescript.echo("PLAYER PULLET OUT HIS COMBAT WEAPON")
                stop()
                
            elif self.health <= C.MIN_HEALTH:
                minescript.echo("PLAYER HAS LOW HEALTH... RECOVER AND TRY AGAIN")
                stop()
                
player = PlayerTracker()
time.sleep(0.5)