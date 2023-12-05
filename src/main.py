import pygame
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1200
CAT_SPEED = 5
SCROLL_SPEED = 5
ANIMATION_SPEED = 100
FPS = 60
TILE_SIZE = 128
WORLD_WIDTH = WINDOW_WIDTH
LEVEL_HEIGHT = 2
WORLD_HEIGHT = WINDOW_HEIGHT * LEVEL_HEIGHT
BORDER_HEIGHT = TILE_SIZE  # Height of the border area
BORDER_Y = 0  # Y position of the border (at the top of the world)

current_frame = 0
frame_count = 0
viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT
border_reaches = 0

# Initialize Pygame
pygame.init()
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Crossing Game")
font = pygame.font.Font("./assets/pico-8.otf", 24)

# Asset loading and sprite extraction
def load_sprite_sheet(filename):
    return pygame.image.load(filename)

def get_sprite(sheet, x, y, width, height, scale_x=None, scale_y=None):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    if scale_x and scale_y:
        sprite = pygame.transform.scale(sprite, (scale_x, scale_y))
    return sprite

cat_sprite_sheet = load_sprite_sheet('assets/grey_cat_sprite.png')
grass_sprite_sheet = load_sprite_sheet('assets/grass_sprite.png')

# Extract and scale sprites
grey_cat = get_sprite(cat_sprite_sheet, 394, 291, 11, 22, 66, 132)
cat_walk_frames_vertical = [get_sprite(cat_sprite_sheet, x, 291, 11, 22, 66, 132) for x in range(426, 491, 32)]
cat_walk_frames_diagonal = [get_sprite(cat_sprite_sheet, x, 250, 11, 22, 66, 132) for x in range(394, 426, 32)]
cat_walk_frames_backwards = [get_sprite(cat_sprite_sheet, x, 247, 11, 22, 66, 132) for x in range(491, 556, 32)]
cat_walk_frames_horizontal = [pygame.transform.rotate(frame, 90) for frame in cat_walk_frames_vertical]
cat_walk_frames = cat_walk_frames_vertical + cat_walk_frames_backwards + cat_walk_frames_diagonal

grass_textures = [(x, 0, 32, 32) for x in range(0, 161, 32)]
textures = [get_sprite(grass_sprite_sheet, *tex, TILE_SIZE, TILE_SIZE) for tex in grass_textures]

# Cat initialization
cat_start_y = WORLD_HEIGHT - 150 - grey_cat.get_height()  # Start position near the bottom of the world
cat_rect = grey_cat.get_rect(center=(WINDOW_WIDTH // 2, cat_start_y))

# Create a larger world surface
world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))

# Function to fill the world surface with tiles
def fill_world_with_tiles():
    for y in range(0, WORLD_HEIGHT, TILE_SIZE):
        for x in range(0, WORLD_WIDTH, TILE_SIZE):
            chosen_texture = random.choice(textures)
            world_surface.blit(chosen_texture, (x, y))

# Function to draw the counter
def draw_counter():
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

fill_world_with_tiles()
draw_level_border()

# Update animation function
def update_animation(horizontal_movement, vertical_movement, current_frame, frame_count):
    current_time = pygame.time.get_ticks()
    if current_time - frame_count > ANIMATION_SPEED:
        frame_count = current_time
        current_frame = (current_frame + 1) % len(cat_walk_frames)

    if vertical_movement > 0:  # Moving down
        cat_image = cat_walk_frames_vertical[current_frame]
    elif horizontal_movement:  # Moving sideways
        cat_image = cat_walk_frames_horizontal[current_frame]
    elif vertical_movement > 0 and horizontal_movement:  # Moving diagonally
        cat_image = cat_walk_frames_diagonal[current_frame]
    elif vertical_movement < 0:  # Moving up
        cat_image = cat_walk_frames_backwards[current_frame]
    else:  # Idle
        cat_image = grey_cat

    return cat_image, frame_count, current_frame


# Draw Frame function
def draw_frame(is_moving, current_frame, viewport_y):
    cat_image = cat_walk_frames[current_frame] if is_moving else grey_cat
    cat_screen_y = cat_rect.y - viewport_y  # Calculate cat's position relative to the viewport
    game_window.blit(cat_image, (cat_rect.x, cat_screen_y))
    pygame.display.update()

# Game Loop
def game_loop():
    global frame_count, current_frame, viewport_y, border_reaches
    running = True
    clock = pygame.time.Clock()
    viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT  # Start at the bottom of the world
    is_moving = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        is_moving = False

        horizontal_movement = 0
        vertical_movement = 0

        # Horizontal movement with boundary check
        if keys[pygame.K_a] and cat_rect.x > 0:
            cat_rect.x -= CAT_SPEED
            is_moving = True
        if keys[pygame.K_d] and cat_rect.x < WINDOW_WIDTH - cat_rect.width:
            cat_rect.x += CAT_SPEED
            is_moving = True

        # Vertical scrolling with boundary check
        if keys[pygame.K_w] and viewport_y > 0:
            viewport_y = max(0, viewport_y - SCROLL_SPEED)
            cat_rect.y -= SCROLL_SPEED  # Move cat up in the world
            is_moving = True
        elif keys[pygame.K_s] and cat_rect.y < WORLD_HEIGHT - cat_rect.height:
            viewport_y = min(WORLD_HEIGHT - WINDOW_HEIGHT, viewport_y + SCROLL_SPEED)
            cat_rect.y += SCROLL_SPEED  # Move cat down in the world
            is_moving = True
            
        # Check for border collision
        if cat_rect.top <= viewport_y + BORDER_HEIGHT:
            # Cat has reached the border, increment counter and reset position
            border_reaches += 1
            cat_rect.y = WORLD_HEIGHT - 150 - grey_cat.get_height()
            viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT

        # Draw the visible portion of the world
        visible_rect = pygame.Rect(0, viewport_y, WINDOW_WIDTH, WINDOW_HEIGHT)
        game_window.blit(world_surface, (0, 0), visible_rect)

        cat_image, frame_count, current_frame = update_animation(horizontal_movement, vertical_movement, current_frame, frame_count)
        
        # Draw the counter and progress bar
        draw_counter()
        draw_progress_bar(viewport_y)
        draw_frame(is_moving, current_frame, viewport_y)

        clock.tick(FPS)
        is_moving = False

    pygame.quit()

if __name__ == "__main__":
    game_loop()
