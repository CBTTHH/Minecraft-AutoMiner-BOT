##CHANGE DEPENDING ON YOUR NEEDS

#SLOTS (REMEMBER TO SUBTRACT 1 TO THE REAL SLOT NUMBER)
PICKAXE_SLOT = 1
SHOVEL_SLOT = 3
WATER_BUCKET_SLOT = 4
FOOD_SLOT = 5
BLOCKS_SLOT = 8

#MINING
MINING_ORE = 'diamond'

#PLAYER HEALTH
MIN_HEALTH = 10

#MOVEMENT
STOP_Y_LEVEL = -58



##NOT CHANGE THESE CONST
#THRESHOLDS ARE INCLUSIVE

#BREAKABLE TYPE AND HAND ITEMS
SHOVEL_BREAKABLE = {'minecraft:dirt', 
                'minecraft:gravel', 
                'minecraft:clay',
                'minecraft:grass_block[snowy=false]', 
                'minecraft:sand', 
                'minecraft:soul_sand',}
        
BLOCKS_ITEM = {'minecraft:cobblestone',
               'minecraft:stone', 
               'minecraft:cobbled_deepslate', 
               'minecraft:deepslate',
               'minecraft:diorite', 
               'minecraft:granite', 
               'minecraft:sandstone'}

FOOD_ITEMS = {'minecraft:cooked_beef', 
              'minecraft:cooked_chicken', 
              'minecraft:cooked_porkchop', 
              'minecraft:cooked_salmon', 
              'minecraft:golden_carrot', 
              'minecraft:golden_apple', 
              'minecraft:pumpkin_pie'}

OTHER_ITEMS = {'minecraft:water_bucket',
               'minecraft:bucket'}

HAND_ITEMS = FOOD_ITEMS.union(BLOCKS_ITEM).union(BLOCKS_ITEM).union(OTHER_ITEMS)

#TIMINGS
ONE_TICK_TIME = 0.05

#PLAYER PHYSICS
GROUND_Y_VEL = (-0.078, 0.0)
FALLING_Y_VEL = (-0.6, -3.92)
STANDING_X_Z_VEL = 0.0
MAX_WALKING_VEL = 0.117859


#PLAYER YAW AND PITCH
YAW_FACING_NORTH = 180
YAW_FACING_SOUTH = 0
YAW_FACING_EAST = -90
YAW_FACING_WEST = 90
PITCH_LOOK_UP = -90
PITCH_LOOK_DOWN = 90
PITCH_LOOK_AHEAD = 0
PITCH_LOOK_INCLINED_DOWN = 30
PITCH_LOOK_INCLINED_UP = -60

#PLAYER EXTRA
BLOCKS_AROUND_PLAYER = [( 0, -1,  0),
                        ( 0,  0,  0),
                        ( 0,  1,  0),
                        ( 0,  2,  0),
                        ( 0,  0,  1),
                        ( 0,  1,  1),
                        ( 0,  0, -1),
                        ( 0,  1, -1),
                        ( 1,  0,  0),
                        ( 1,  1,  0),
                        (-1,  0,  0),
                        (-1,  1,  0)]

#MOVEMENT
MAX_CENTER_OFFSET = (0.01, 0.02)
COORDS_OFFSET = 0.5


#PRIORITY RATING
CLUSTER_DISTANCE_SCORE = 1.5
CLUSTER_SIZE_SCORE = 2

#SAFETY
Y_LEVEL_LAVA_CHECK = (-59, -56)

#MINING
INVALID_Y_LEVEL = (-60, -64)
Y_LEVEL_LAVA_PUDDLE = -55




