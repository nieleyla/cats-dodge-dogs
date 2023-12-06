# Imports
import pygame
import random
import numpy as np
from perlin_noise import PerlinNoise



# Constants

## Game window
GAME_TITLE = "Cats Dodge Dogs"

### Dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1200


## Movement

## Movement speed
CAT_SPEED_X = 8 # Horizontal movement speed
CAT_SPEED_Y = 16 # Vertical movement speed
DOG_SPEED_X = 8 # Horizontal movement speed
DOG_SPEED_Y = 8 # Vertical movement speed


## Animation
ANIMATION_SPEED = 60
FPS = 60


### Cat
CAT_WALK_FRAMES = 4 # Number of frames in the cat walking animation
REF_CAT_WIDTH = 23
REF_CAT_HEIGHT = 21
CAT_SCALE_X = 5
CAT_SCALE_Y = 5
CAT_SPRITE_COORDINATES = {
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

### Dog
DOG_WALK_FRAMES = 4 # Number of frames in the dog walking animation
REF_DOG_WIDTH = 23
REF_DOG_HEIGHT = 21
DOG_SCALE_X = 5
DOG_SCALE_Y = 5
DOG_SPRITE_COORDINATES = {
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



# Functions

## Asset loading and sprite extraction

### Loading sprite sheet from file
def load_sprite_sheet(filename):
    return pygame.image.load(filename)

def get_sprite(sheet, x, y, width, height, scale_x, scale_y):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    if scale_x and scale_y:
        sprite = pygame.transform.scale(sprite, (width*scale_x, height*scale_y))
    return sprite

def generate_sprites(sheet, coordinates):
    sprites = {}
    for direction, coordinates in coordinates.items():
        sprites[direction] = [get_sprite(sheet, *coord, CAT_SCALE_X, CAT_SCALE_Y) for coord in coordinates]
    return sprites


## Drawing world

## Drawing world tiles
def fill_world_with_tiles(texture_sets):
    for y in range(0, WORLD_HEIGHT, TILE_SIZE):
        for x in range(0, WORLD_WIDTH, TILE_SIZE):
            for texture_set in texture_sets:
                chosen_texture = random.choice(texture_set)
                world_surface.blit(chosen_texture, (x, y))

## Drawing noise
def draw_noise(octaves=NOISE_OCTAVES):
    noise = PerlinNoise(octaves=octaves)
    for y in range(0, WORLD_HEIGHT, NOISE_CLUSTER_SIZE):
        for x in range(0, WORLD_WIDTH, NOISE_CLUSTER_SIZE):
            noise_surface = pygame.Surface((NOISE_SURFACE_SIZE, NOISE_SURFACE_SIZE), pygame.SRCALPHA)
            noise_surface.fill((0, 0, 0, NOISE_ALPHA))
            noise_surface.set_alpha(noise([x / WORLD_WIDTH, y / WORLD_HEIGHT]) * 255)
            world_surface.blit(noise_surface, (x, y))


## Drawing UI

### Drawing the completions counter
def draw_counter(border_reaches):
    text = font.render(f"completions: {border_reaches}", True, (255, 255, 255))
    game_window.blit(text, (WINDOW_WIDTH - text.get_width() - 20, 20))

### Drawing the progress bar
def draw_progress_bar(viewport_y):
    progress = viewport_y / (WORLD_HEIGHT - WINDOW_HEIGHT)
    bar_length = 200  # Total length of the bar
    filled_length = bar_length * progress
    pygame.draw.rect(game_window, (255, 255, 255), (20, 20, bar_length, 20))  # Draw the border of the bar
    pygame.draw.rect(game_window, (0, 255, 0), (20, 20, filled_length, 20))  # Draw the filled part of the bar

### Drawing the level border
def draw_level_border():
    # Fill the border area with a gradient
    for y in range(BORDER_Y, BORDER_Y + BORDER_HEIGHT):
        for x in range(WORLD_WIDTH):
            # Calculate alpha based on distance from the top of the border
            alpha = 255 - (y - BORDER_Y) / BORDER_HEIGHT * 255
            fade_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, alpha))
            world_surface.blit(fade_surface, (x, y))

### Drawing the 'UP' arrow
def draw_arrow(viewport_y, size=128, color=(255, 255, 0), alpha=128):
    position = (WINDOW_WIDTH // 2 - size // 2, WINDOW_HEIGHT // 3 - (viewport_y - 2400))  # Position of the arrow
    # Create a surface for the arrow
    arrow_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    arrow_surface.fill((0, 0, 0, 0))  # Make the surface fully transparent
    # Define points for the arrow
    arrow_points = [
        (size // 2, 0),             # Top point
        (size, size),               # Bottom right
        (size // 2, size * 2 // 3), # Middle
        (0, size)                   # Bottom left
    ]
    # Draw the arrow
    alpha = 180 + 60 * np.sin(pygame.time.get_ticks() / 256)
    pygame.draw.polygon(arrow_surface, color + (alpha,), arrow_points)
    # Blit the arrow surface onto the main screen
    game_window.blit(arrow_surface, position)


## Drawing the level end screen
def draw_end_screen(border_reaches):
    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade_surface.fill((0, 0, 0))
    text = font.render(f"completions: {border_reaches}", True, (255, 255, 255))
    for alpha in np.linspace(0, 255, 60):
        fade_surface.set_alpha(alpha)
        text.set_alpha(alpha)
        game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
        game_window.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(32)
    pygame.display.update()

## Drawing the game over screen
def draw_game_over_screen(border_reaches):

    # Fading to black
    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 256, 5):  # Faster fade to black
        fade_surface.set_alpha(alpha)
        game_window.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(20)

    # Fading in "YOU DIED" text
    for size in np.linspace(10, 100, 100):  # Gradual increase in text size
        text = pygame.font.Font.render(font, "YOU DIED", True, (255, 0, 0))
        text = pygame.transform.scale(text, (int(text.get_width() * (size / 100)), int(text.get_height() * (size / 100))))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        game_window.blit(fade_surface, (0, 0))  # Redraw black background
        game_window.blit(text, text_rect)       # Draw main text
        pygame.display.update()
        pygame.time.delay(10)
    pygame.time.delay(500)

    # Display border reaches
    reach_text = pygame.font.Font.render(font, f"completions: {border_reaches}", True, (255, 255, 255))
    reach_rect = reach_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
    game_window.blit(reach_text, reach_rect)
    pygame.display.update()
    pygame.time.delay(1000)


## Animation

### Retrieval of current animation frame
def get_animation_frame(sprites, horizontal_movement, vertical_movement, current_frame, frame_count, last_movement, walk_frames=CAT_WALK_FRAMES):
    current_time = pygame.time.get_ticks()
    if current_time - frame_count > ANIMATION_SPEED:
        frame_count = current_time
        current_frame = (current_frame + 1) % walk_frames

    if vertical_movement < 0:  # Moving down
        image = sprites['S'][current_frame]
        last_movement = 'S'
    if vertical_movement > 0:  # Moving up
        image = sprites['N'][current_frame]
        last_movement = 'N'
    if horizontal_movement > 0:  # Moving right
        image = sprites['E'][current_frame]
        last_movement = 'E'
    if horizontal_movement < 0:  # Moving left
        image = sprites['W'][current_frame]
        last_movement = 'W'
    if horizontal_movement > 0 and vertical_movement < 0:  # Moving down-right
        image = sprites['SE'][current_frame]
        last_movement = 'SE'
    if horizontal_movement > 0 and vertical_movement > 0:  # Moving up-right
        image = sprites['NE'][current_frame]
        last_movement = 'NE'
    if horizontal_movement < 0 and vertical_movement < 0:  # Moving down-left
        image = sprites['SW'][current_frame]
        last_movement = 'SW'
    if horizontal_movement < 0 and vertical_movement > 0:  # Moving up-left
        image = sprites['NW'][current_frame]
        last_movement = 'NW'
    if horizontal_movement == 0 and vertical_movement == 0:  # Idle
        idle_mapping = {'N': 0, 'NE': 1, 'E': 1, 'SE': 1, 'S': 2, 'SW': 2, 'W': 3, 'NW': 3}
        image = sprites['ID'][idle_mapping[last_movement]]

    return image, current_frame, frame_count, last_movement

### Drawing a character
def draw_character(image, rect, viewport_y):
    screen_y = rect.y - viewport_y
    game_window.blit(image, (rect.x, screen_y))


# Game Loop
def game_loop(cat_sprites, dog_sprites, cat_rect, dog_rect, viewport_y=WORLD_HEIGHT-WINDOW_HEIGHT, border_reaches=0):

    ## Initialization
    running = True
    clock = pygame.time.Clock()
    viewport_x = 0
    viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT  # Start viewport at the bottom of the world
    dogs = 1
    
    ### Animation initialization
    last_cat_movement = 'N'  # Start with player facing north
    last_dog_movements = ['E'] # Start with dogs facing east
    current_cat_frame = 0
    current_dog_frames = [0]
    cat_frame_count = 0
    dog_frame_counts = [0]
    horizontal_cat_movement = 0
    vertical_cat_movement = 0
    horizontal_dog_movements = [1]
    vertical_dog_movements = [0]

    ## Main game loop
    while running:
        for event in pygame.event.get():

            ### Quitting the game
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        ### Movement

        #### Horizontal movement with boundary check
        if keys[pygame.K_a] and cat_rect.x > 0:
            horizontal_cat_movement = -1
        if keys[pygame.K_d] and cat_rect.x < WINDOW_WIDTH - cat_rect.width:
            horizontal_cat_movement = 1

        #### Vertical movement with boundary check
        if keys[pygame.K_w] and cat_rect.y > viewport_y - cat_rect.height:
            viewport_y = max(0, viewport_y - CAT_SPEED_Y)
            vertical_cat_movement = 1
        if keys[pygame.K_s] and cat_rect.y < WORLD_HEIGHT - cat_rect.height:
            viewport_y = min(WORLD_HEIGHT - WINDOW_HEIGHT, viewport_y + CAT_SPEED_Y)
            vertical_cat_movement = -1

        #### Apply cat movement
        cat_rect.x += horizontal_cat_movement * CAT_SPEED_X
        cat_rect.y -= vertical_cat_movement * CAT_SPEED_Y

        #### Dog movement (walking back and forth)
        for i in range(dogs):
            if dog_rects[i].x <= 0:
                horizontal_dog_movements[i] = 1
            if dog_rects[i].x >= WINDOW_WIDTH - 2*dog_rect[i].width:
                horizontal_dog_movements[i] = -1
            
            #### Apply dog movement
            dog_rect[i].x += horizontal_dog_movements[i] * (DOG_SPEED_X + 2*border_reaches*random.randint(1, 100)*0.01)
            dog_rect[i].y -= vertical_dog_movements[i] * DOG_SPEED_Y
        
        #### Check for border collision
        if cat_rect.top <= viewport_y - cat_rect.height:
            border_reaches += 1
            dogs += 1
            # Dog spacing depends on number of dogs, number of completions, and LEVEL_HEIGHT:
            dog_rects.append(idle_dog.get_rect(center=(REF_DOG_WIDTH, dog_start_y + min(dogs*LEVEL_HEIGHT*32*(random.randint(1, 100)*0.1)/border_reaches, int(WINDOW_HEIGHT/2)))))
            horizontal_dog_movements.append(1)
            vertical_dog_movements.append(0)
            last_dog_movements.append(random.choice(['E','W']))
            dog_frame_counts.append(0)
            current_dog_frames.append(0)
            draw_end_screen(border_reaches)
            cat_rect.y = WORLD_HEIGHT - 150 - REF_CAT_HEIGHT # Reset cat position
            viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT # Reset viewport position

        ### Check for dog collision
        for i in range(dogs):
            if cat_rect.colliderect(dog_rects[i].inflate(dog_rects[i].width//2, -dog_rects[i].height*0.5)):
                draw_game_over_screen(border_reaches)
                cat_rect.y = WORLD_HEIGHT - 150 - REF_CAT_HEIGHT
                viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT
                border_reaches = 0
                dogs = 1

        ### Drawing the visible part of the world
        visible_rect = pygame.Rect(0, viewport_y, WINDOW_WIDTH, WINDOW_HEIGHT)
        game_window.blit(world_surface, (0, 0), visible_rect)

        ### Drawing UI
        draw_counter(border_reaches)
        draw_progress_bar(viewport_y)
        draw_arrow(viewport_y, 96, (200, 200, 150), 200)

        ### Animation
        cat_image, current_cat_frame, cat_frame_count, last_cat_movement = get_animation_frame(cat_sprites, horizontal_cat_movement, vertical_cat_movement, current_cat_frame, cat_frame_count, last_cat_movement, CAT_WALK_FRAMES)
        draw_character(cat_image, cat_rect, viewport_y)
        
        for i in range(dogs):
            dog_image, current_dog_frames[i], dog_frame_counts[i], last_dog_movements[i] = get_animation_frame(dog_sprites, horizontal_dog_movements[i], vertical_dog_movements[i], current_dog_frames[i], dog_frame_counts[i], last_dog_movements[i], DOG_WALK_FRAMES)
            draw_character(dog_image, dog_rects[i], viewport_y + len(dog_rects)*DOG_SPEED_Y)
        
        ### Reset
        horizontal_cat_movement = 0
        vertical_cat_movement = 0

        ### Game clock
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()



# Main function
if __name__ == "__main__":

    ## Initialize Pygame
    pygame.init()
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    font = pygame.font.Font("./assets/pico-8.otf", 24)

    ## Load assets
    ### Load sprite sheets from file
    cat_sprite_sheet = load_sprite_sheet('assets/grey_cat_sprites.png')
    dog_sprite_sheet = load_sprite_sheet('assets/grey_cat_sprites.png')
    grass_sprite_sheet = load_sprite_sheet('assets/grass_sprites.png')
    plant_sprite_sheet = load_sprite_sheet('assets/plant_sprites.png')
    ### Extract sprites from sprite sheets
    grass_texture_coordinates = [(x, 0, 32, 32) for x in range(0, 161, 32)]
    grass_textures = [get_sprite(grass_sprite_sheet, *tex, TILE_SCALE, TILE_SCALE) for tex in grass_texture_coordinates]
    plant_textures = [get_sprite(plant_sprite_sheet, *tex, TILE_SCALE, TILE_SCALE) for tex in grass_texture_coordinates]
    ### Pregenerate sprites
    cat_sprites = generate_sprites(cat_sprite_sheet, CAT_SPRITE_COORDINATES)
    dog_sprites = generate_sprites(dog_sprite_sheet, DOG_SPRITE_COORDINATES)

    ## Initialize game world
    world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
    fill_world_with_tiles([grass_textures,]) #plant_textures])
    draw_level_border()
    draw_noise()

    ## Initialize cat   
    cat_start_y = WORLD_HEIGHT - int(0.25*WINDOW_HEIGHT) - REF_CAT_HEIGHT  # Start position near the bottom of the world
    idle_cat = cat_sprites['ID'][0]
    cat_rect = idle_cat.get_rect(center=(WINDOW_WIDTH // 2, cat_start_y))

    ## Initialize dog
    dog_start_y = WORLD_HEIGHT - int(1.5*WINDOW_HEIGHT) - REF_DOG_HEIGHT
    idle_dog = dog_sprites['ID'][0]
    dog_rects = [idle_dog.get_rect(center=(REF_DOG_WIDTH, dog_start_y))]

    ## Start the game loop
    game_loop(cat_sprites, dog_sprites, cat_rect, dog_rects)
