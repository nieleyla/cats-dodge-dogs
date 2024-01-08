# Constants

## Game window
GAME_TITLE = "Cats Dodge Dogs"

## Game state
SAVE_FILE_NAME = f"{GAME_TITLE.replace(' ', '_')}.json"
DEBUG = False

## Game mechanics
SPECIAL_SCORE = 10
DEFAULT_HEALTH = 2
HEAL_AMOUNT = 1
IMMUNITY_TIME = 200
CAT_HITBOX_SCALE_X = 1
CAT_HITBOX_SCALE_Y = 0.9
DOG_HITBOX_SCALE_X = 0.8
DOG_HITBOX_SCALE_Y = 0.6

### Dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1080

### Spawning
MIN_GAP = 100  # Minimum gap between dogs
GAP_REDUCTION_FACTOR = 10  # How much the gap reduces per border reach
VIEWPORT_BUFFER = 600
MAX_SPAWN_TRIES = 100


## Movement

## Movement speed
CAT_SPEED_X = 8 # Horizontal movement speed
CAT_SPEED_Y = 16 # Vertical movement speed
DOG_SPEED_X = 8 # Horizontal movement speed
DOG_SPEED_CAP = DOG_SPEED_X * 4 # Maximum dog speed


## Animation
CAT_ANIMATION_SPEED = 60
DOG_ANIMATION_SPEED = 45
FPS = 60

## Sprites

### Cat
### Regular Cat
CAT_WALK_FRAMES = 4 # Number of frames in the cat walking animation
REF_CAT_WIDTH = 23
REF_CAT_HEIGHT = 21
CAT_SCALE_X = 5
CAT_SCALE_Y = 5
GREY_CAT_COORDINATES = {
    'N': [(394, 291, 11, 22), (426, 292, 11, 22), (458, 291, 11, 22), (490, 292, 11, 22)], 
    'NE': [(389, 358, 23, 19), (422, 357, 22, 20), (453, 358, 23, 18), (486, 357, 22, 20)],
    'E': [(391, 422, 21, 18), (423, 421, 21, 19), (455, 422, 21, 18), (487, 421, 21, 19)],
    'SE': [(389, 486, 23, 20), (422, 485, 22, 21), (453, 486, 23, 20), (486, 485, 22, 21)],
    'S': [(394, 33, 11, 25), (426, 34, 11, 25), (458, 33, 11, 25), (490, 34, 11, 25)],
    'SW': [(388, 102, 23, 20), (420, 101, 22, 21), (452, 102, 23, 20), (484, 101, 22, 21)],
    'W': [(388, 166, 21, 18), (420, 165, 21, 19), (452, 166, 21, 18), (484, 165, 21, 19)],
    'NW': [(388, 230, 23, 19), (420, 229, 22, 20), (452, 230, 23, 18), (484, 229, 22, 20)],
    'ID': [(266, 292, 11, 24), (227, 422, 25, 18), (362, 42, 11, 18), (228, 166, 25, 18)]
}

### Dogs
DOG_BASE_WEIGHTS = {'dog_white': 3, 'dog_bw': 3, 'dog_black': 2, 'dog_brown': 4, 'dog_exotic': 2, 'boss_walking': 0.25, 'boss_boxing': 0.125}
DOG_BASE_WEIGHTS = {k: v / sum(DOG_BASE_WEIGHTS.values()) for k, v in DOG_BASE_WEIGHTS.items()}

#### Regular Dog
DOG_WALK_FRAMES = 7
REF_DOG_WIDTH = 23
REF_DOG_HEIGHT = 21
DOG_SCALE_X = 5
DOG_SCALE_Y = 5
WHITE_DOG_COORDINATES = {'E': [(17, 17, 25, 22), (81, 17, 24, 22), (145, 17, 24, 22), (209, 17, 24, 22), (273, 17, 25, 22), (337, 17, 24, 22), (401, 17, 24, 22)]}
BW_DOG_COORDINATES= {'E': [(17, 21, 25, 22), (81, 21, 24, 22), (145, 21, 24, 22), (209, 21, 24, 22), (273, 21, 25, 22), (337, 21, 24, 22), (401, 21, 24, 22)]}
BLACK_DOG_COORDINATES = {'E': [(17, 22, 25, 22), (81, 22, 24, 22), (145, 22, 24, 22), (209, 22, 24, 22), (273, 22, 25, 22), (337, 22, 24, 22), (401, 22, 24, 22)]}
BROWN_DOG_COORDINATES = {'E': [(17, 22, 24, 22), (81, 22, 23, 22), (145, 22, 23, 22), (209, 22, 23, 22), (273, 22, 24, 22), (337, 22, 23, 22), (401, 22, 23, 22)]}
EXOTIC_DOG_COORDINATES = {'E': [(17, 21, 25, 22), (81, 21, 24, 22), (145, 21, 24, 22), (209, 21, 24, 22), (273, 21, 25, 22), (337, 21, 24, 22), (401, 21, 24, 22)]}

#### Boss Dog
BOSS_SCALE_X = 1.5
BOSS_SCALE_Y = 1.5
REF_BOSS_WIDTH = 25
REF_BOSS_HEIGHT = 50
BOSS_WALKING_COORDINATES = {'E': [(16, 4, 84, 124), (148, 4, 80, 116), (276, 0, 92, 108), (400, 0, 84, 120), (528, 4, 84, 124), (648, 0, 96, 120), (648, 0, 96, 120)]}
BOSS_BOXING_COORDINATES = {'E': [(16, 4, 84, 124), (148, 4, 92, 124), (276, 4, 96, 124), (404, 4, 108, 124), (532, 4, 108, 124), (660, 4, 100, 124), (660, 4, 100, 124)]}

### Environment
GRASS_COORDINATES = [(x, 0, 32, 32) for x in range(0, 161, 32)]
PLANT_COORDINATES = [(x, 32, 32, 32) for x in range(0, 161, 32)]

### UI
START_BUTTON_COORDINATES = (240, 951, 318, 98)

### Wrapping
SPRITE_COORDINATES = {
    'cat_grey': GREY_CAT_COORDINATES,
    'dog_white': WHITE_DOG_COORDINATES,
    'dog_bw': BW_DOG_COORDINATES,
    'dog_black': BLACK_DOG_COORDINATES,
    'dog_brown': BROWN_DOG_COORDINATES,
    'dog_exotic': EXOTIC_DOG_COORDINATES,
    'boss_walking': BOSS_WALKING_COORDINATES,
    'boss_boxing': BOSS_BOXING_COORDINATES,
}
SPRITE_SCALES = [
    {
        'cat_grey': CAT_SCALE_X, 
        'dog_white': DOG_SCALE_X, 
        'dog_bw': DOG_SCALE_X, 
        'dog_black': DOG_SCALE_X, 
        'dog_brown': DOG_SCALE_X, 
        'dog_exotic': DOG_SCALE_X, 
        'boss_walking': BOSS_SCALE_X, 
        'boss_boxing': BOSS_SCALE_X
     }, 
     {
        'cat_grey': CAT_SCALE_Y, 
        'dog_white': DOG_SCALE_Y, 
        'dog_bw': DOG_SCALE_Y, 
        'dog_black': DOG_SCALE_Y, 
        'dog_brown': DOG_SCALE_Y, 
        'dog_exotic': DOG_SCALE_Y, 
        'boss_walking': BOSS_SCALE_Y, 
        'boss_boxing': BOSS_SCALE_Y
        }
    ]
SPRITE_LIST = ['cat_grey', 'dog_white', 'dog_bw', 'dog_black', 'dog_brown', 'dog_exotic', 'boss_walking', 'boss_boxing',]
DOUBLE_DAMAGE_DOGS = ['boss_walking', 'boss_boxing',]
UI_LIST = ['screen_start_normal', 'screen_start_special', 'screen_death', 'overlay_horizon', 'heart', 'heart_bg', 'heart_border', 'screen_keybinds'] # 'overlay_arrow']
SOUNDS = {'you-died': 0.5, 'cat-hurt-light': 0.5, 'cat-hurt-hard': 0.5, 'level-complete': 0.25, 'cat-heal': 0.5}


## Game world

### Dimensions
TILE_SIZE = 128
TILE_SCALE = 4
WORLD_WIDTH = WINDOW_WIDTH
LEVEL_HEIGHT = 3
WORLD_HEIGHT = WINDOW_HEIGHT * LEVEL_HEIGHT
BORDER_HEIGHT = TILE_SIZE  # Height of the border area
BORDER_Y = 0  # Y position of the border (at the top of the world)

### Noise
NOISE_OCTAVES = 6
NOISE_CLUSTER_SIZE = 48
NOISE_SURFACE_SIZE = 128
NOISE_ALPHA = 12
