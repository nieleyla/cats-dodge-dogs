import pygame
import random
import numpy as np
from perlin_noise import PerlinNoise


# Constants
## Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1200

## Cat movement speed
CAT_SPEED = 8 # Horizontal movement speed
SCROLL_SPEED = 8 # Vertical movement speed

## Animation
ANIMATION_SPEED = 60
FPS = 60
CAT_WALK_FRAMES = 4 # Number of frames in the cat walking animation
REF_CAT_WIDTH = 23
REF_CAT_HEIGHT = 21
CAT_SCALE_X = 5
CAT_SCALE_Y = 5
SPRITE_COORDINATES = {
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

## World dimensions
TILE_SIZE = 128
TILE_SCALE = 4
NOISE_OCTAVES = 6
NOISE_CLUSTER_SIZE = 48
NOISE_SURFACE_SIZE = 128
NOISE_ALPHA = 12
WORLD_WIDTH = WINDOW_WIDTH
LEVEL_HEIGHT = 2
WORLD_HEIGHT = WINDOW_HEIGHT * LEVEL_HEIGHT
BORDER_HEIGHT = TILE_SIZE  # Height of the border area
BORDER_Y = 0  # Y position of the border (at the top of the world)


# Asset loading and sprite extraction
def load_sprite_sheet(filename):
    return pygame.image.load(filename)

def get_sprite(sheet, x, y, width, height, scale_x, scale_y):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    if scale_x and scale_y:
        sprite = pygame.transform.scale(sprite, (width*scale_x, height*scale_y))
    return sprite

def generate_cat_sprites(sheet):
    cat_sprites = {}
    for direction, coordinates in SPRITE_COORDINATES.items():
        cat_sprites[direction] = [get_sprite(sheet, *coord, CAT_SCALE_X, CAT_SCALE_Y) for coord in coordinates]
    return cat_sprites

# Function to fill the world surface with tiles
# Takes arbitrary amount of sprite sheets as arguments and blends them together in order
def fill_world_with_tiles(texture_sets):
    for y in range(0, WORLD_HEIGHT, TILE_SIZE):
        for x in range(0, WORLD_WIDTH, TILE_SIZE):
            for texture_set in texture_sets:
                chosen_texture = random.choice(texture_set)
                world_surface.blit(chosen_texture, (x, y))

# Function to draw the counter
def draw_counter(border_reaches):
    text = font.render(f"completions: {border_reaches}", True, (255, 255, 255))
    game_window.blit(text, (WINDOW_WIDTH - text.get_width() - 20, 20))

# Function to draw the progress bar
def draw_progress_bar(viewport_y):
    progress = viewport_y / (WORLD_HEIGHT - WINDOW_HEIGHT)
    bar_length = 200  # Total length of the bar
    filled_length = bar_length * progress
    pygame.draw.rect(game_window, (255, 255, 255), (20, 20, bar_length, 20))  # Draw the border of the bar
    pygame.draw.rect(game_window, (0, 255, 0), (20, 20, filled_length, 20))  # Draw the filled part of the bar

# Function to draw the top level border with a pixel-dithered fade to black overlay
def draw_level_border():
    # Fill the border area with a gradient
    for y in range(BORDER_Y, BORDER_Y + BORDER_HEIGHT):
        for x in range(WORLD_WIDTH):
            # Calculate alpha based on distance from the top of the border
            alpha = 255 - (y - BORDER_Y) / BORDER_HEIGHT * 255
            fade_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, alpha))
            world_surface.blit(fade_surface, (x, y))

def draw_noise(octaves=NOISE_OCTAVES):
    noise = PerlinNoise(octaves=octaves)
    for y in range(0, WORLD_HEIGHT, NOISE_CLUSTER_SIZE):
        for x in range(0, WORLD_WIDTH, NOISE_CLUSTER_SIZE):
            noise_surface = pygame.Surface((NOISE_SURFACE_SIZE, NOISE_SURFACE_SIZE), pygame.SRCALPHA)
            noise_surface.fill((0, 0, 0, NOISE_ALPHA))
            noise_surface.set_alpha(noise([x / WORLD_WIDTH, y / WORLD_HEIGHT]) * 255)
            world_surface.blit(noise_surface, (x, y))

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


# Update animation function
## This function takes in the current frame and the direction of movement and returns the appropriate animation frame
def get_animation_frame(cat_sprites, horizontal_movement, vertical_movement, current_frame, frame_count, last_movement):
    current_time = pygame.time.get_ticks()
    if current_time - frame_count > ANIMATION_SPEED:
        frame_count = current_time
        current_frame = (current_frame + 1) % CAT_WALK_FRAMES

    if vertical_movement < 0:  # Moving down
        cat_image = cat_sprites['S'][current_frame]
        last_movement = 'S'
    if vertical_movement > 0:  # Moving up
        cat_image = cat_sprites['N'][current_frame]
        last_movement = 'N'
    if horizontal_movement > 0:  # Moving right
        cat_image = cat_sprites['E'][current_frame]
        last_movement = 'E'
    if horizontal_movement < 0:  # Moving left
        cat_image = cat_sprites['W'][current_frame]
        last_movement = 'W'
    if horizontal_movement > 0 and vertical_movement < 0:  # Moving down-right
        cat_image = cat_sprites['SE'][current_frame]
        last_movement = 'SE'
    if horizontal_movement > 0 and vertical_movement > 0:  # Moving up-right
        cat_image = cat_sprites['NE'][current_frame]
        last_movement = 'NE'
    if horizontal_movement < 0 and vertical_movement < 0:  # Moving down-left
        cat_image = cat_sprites['SW'][current_frame]
        last_movement = 'SW'
    if horizontal_movement < 0 and vertical_movement > 0:  # Moving up-left
        cat_image = cat_sprites['NW'][current_frame]
        last_movement = 'NW'
    if horizontal_movement == 0 and vertical_movement == 0:  # Idle
        idle_mapping = {'N': 0, 'NE': 1, 'E': 1, 'SE': 1, 'S': 2, 'SW': 2, 'W': 3, 'NW': 3}
        cat_image = cat_sprites['ID'][idle_mapping[last_movement]]

    return cat_image, current_frame, frame_count, last_movement

# Draw Frame function
def draw_cat(cat_image, viewport_y):
    cat_screen_y = cat_rect.y - viewport_y  # Calculate cat's position relative to the viewport
    game_window.blit(cat_image, (cat_rect.x, cat_screen_y))
    pygame.display.update()

def draw_dogs():
    # For now, just draw rectangles scrolling horizontally across the screen
    dog_rect = pygame.Rect(0, 0, 100, 100)
    dog_rect.center = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(game_window, (255, 0, 0), dog_rect)
    pygame.display.update()


# Game Loop
def game_loop(cat_sprites, current_frame=0, frame_count=0, viewport_y=WORLD_HEIGHT-WINDOW_HEIGHT, border_reaches=0):
    running = True
    clock = pygame.time.Clock()
    viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT  # Start at the bottom of the world
    last_movement = 'N'  # Start facing north

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Movement
        horizontal_movement = 0
        vertical_movement = 0
        ## Horizontal movement with boundary check
        if keys[pygame.K_a] and cat_rect.x > 0:
            horizontal_movement = -1
        if keys[pygame.K_d] and cat_rect.x < WINDOW_WIDTH - cat_rect.width:
            horizontal_movement = 1
        ## Vertical movement with boundary check
        if keys[pygame.K_w] and cat_rect.y > viewport_y - cat_rect.height:
            viewport_y = max(0, viewport_y - SCROLL_SPEED)
            vertical_movement = 1
        if keys[pygame.K_s] and cat_rect.y < WORLD_HEIGHT - cat_rect.height:
            viewport_y = min(WORLD_HEIGHT - WINDOW_HEIGHT, viewport_y + SCROLL_SPEED)
            vertical_movement = -1
        ## Apply movement
        cat_rect.x += horizontal_movement * CAT_SPEED
        cat_rect.y -= vertical_movement * SCROLL_SPEED
        ## Check for border collision
        if cat_rect.top <= viewport_y - cat_rect.height:
            ### Cat has reached the border, increment counter and reset position
            border_reaches += 1
            draw_end_screen(border_reaches)
            cat_rect.y = WORLD_HEIGHT - 150 - REF_CAT_HEIGHT
            viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT

        # Draw the visible portion of the world
        visible_rect = pygame.Rect(0, viewport_y, WINDOW_WIDTH, WINDOW_HEIGHT)
        game_window.blit(world_surface, (0, 0), visible_rect)
        cat_image, current_frame, frame_count, last_movement = get_animation_frame(cat_sprites, horizontal_movement, vertical_movement, current_frame, frame_count, last_movement)
        
        # Draw the counter and progress bar
        draw_counter(border_reaches)
        draw_progress_bar(viewport_y)
        draw_cat(cat_image, viewport_y)
        draw_dogs()

        # Tick the clock
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":

    # Initialize Pygame
    pygame.init()
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Crossing Game")
    font = pygame.font.Font("./assets/pico-8.otf", 24)

    # Load assets
    grass_texture_coordinates = [(x, 0, 32, 32) for x in range(0, 161, 32)]

    cat_sprite_sheet = load_sprite_sheet('assets/grey_cat_sprites.png')
    grass_sprite_sheet = load_sprite_sheet('assets/grass_sprites.png')
    plant_sprite_sheet = load_sprite_sheet('assets/plant_sprites.png')
    
    grass_textures = [get_sprite(grass_sprite_sheet, *tex, TILE_SCALE, TILE_SCALE) for tex in grass_texture_coordinates]
    plant_textures = [get_sprite(plant_sprite_sheet, *tex, TILE_SCALE, TILE_SCALE) for tex in grass_texture_coordinates]
    
    cat_sprites = generate_cat_sprites(cat_sprite_sheet)

    # Initialize game world
    world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
    fill_world_with_tiles([grass_textures, plant_textures])
    draw_level_border()
    draw_noise()

    # Initialize cat
    cat_start_y = WORLD_HEIGHT - 150 - REF_CAT_HEIGHT  # Start position near the bottom of the world
    idle_cat = cat_sprites['ID'][0]
    cat_rect = idle_cat.get_rect(center=(WINDOW_WIDTH // 2, cat_start_y))

    # Start the game loop
    game_loop(cat_sprites)
