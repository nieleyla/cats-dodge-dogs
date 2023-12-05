import pygame
import random

pygame.init()

# game window
window_width = 800
window_height = 1200
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Crossing Game")

# load images
cat_sprite_sheet = pygame.image.load('assets/grey_cat_sprite.png')
grass_sprite_sheet = pygame.image.load('assets/grass_sprite.png')

# extract sprites
def get_sprite(sheet, x, y, width, height):
    """Extracts and returns a single sprite from the sprite sheet."""
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

grey_cat = get_sprite(cat_sprite_sheet, 394, 291, 11, 22)
grey_cat_walk_1 = get_sprite(cat_sprite_sheet, 426, 292, 11, 22)
grey_cat_walk_2 = get_sprite(cat_sprite_sheet, 458, 291, 11, 22)
grey_cat_walk_3 = get_sprite(cat_sprite_sheet, 490, 292, 11, 22)
cat_walk_frames = [grey_cat_walk_1, grey_cat_walk_2, grey_cat_walk_3]
grass_textures = [
        (0, 0, 32, 32),
        (32, 0, 32, 32),
        (64, 0, 32, 32),
        (96, 0, 32, 32),
        (128, 0, 32, 32),
        (160, 0, 32, 32),
]
textures = [get_sprite(grass_sprite_sheet, x, y, width, height) for (x, y, width, height) in grass_textures]

# resize the cat, resize grass
grey_cat = pygame.transform.scale(grey_cat, (66, 132))
cat_walk_frames = [pygame.transform.scale(frame, (66, 132)) for frame in cat_walk_frames]
original_tile_width, original_tile_height = textures[0].get_size()
new_tile_width = original_tile_width * 4
new_tile_height = original_tile_height * 4
scaled_textures = [pygame.transform.scale(tex, (new_tile_width, new_tile_height)) for tex in textures]

cat_rect = grey_cat.get_rect()
cat_rect.x = window_width // 2 - cat_rect.width // 2
cat_rect.y = window_height - cat_rect.height - 150

# surface for drawing the tiles
buffer_height = new_tile_height
tile_surface_height = window_height + 2 * buffer_height
tile_surface = pygame.Surface((window_width, tile_surface_height))

for y in range(-buffer_height, tile_surface_height - buffer_height, new_tile_height):
        for x in range(0, window_width, new_tile_width):
                chosen_texture = random.choice(scaled_textures)
                tile_surface.blit(chosen_texture, (x, y))

# game loop
running = True
clock = pygame.time.Clock()
animation_speed = 100
frame_count = 0
current_frame = 0
cat_speed = 5
background_y = 0
scroll_speed = 5
scroll = 0

while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # check key presses
        keys = pygame.key.get_pressed()
        is_moving = False
        scroll_movement = 0
       
        # move cat horizontally
        if keys[pygame.K_a]:
                cat_rect.x -= cat_speed
                is_moving = True
        if keys[pygame.K_d]:
                cat_rect.x += cat_speed
                is_moving = True
                
        # move the background vertically
        if keys[pygame.K_w] or keys[pygame.K_s]:
                if keys[pygame.K_w]:
                        scroll_movement = scroll_speed
                        is_moving = True
                if keys[pygame.K_s]:
                        scroll_movement = -scroll_speed
                        is_moving = True
                
                tile_surface.scroll(dy=scroll_movement)
                
                if scroll_movement > 0:
                        y_pos = -buffer_height
                elif scroll_movement < 0:
                        y_pos = window_height + buffer_height - new_tile_height
                
                for x in range(0, window_width, new_tile_width):
                        chosen_texture = random.choice(scaled_textures)
                        tile_surface.blit(chosen_texture, (x, y_pos))
                        
        game_window.blit(tile_surface, (0, 0), area=(0, buffer_height, window_width, window_height))
        
        # animation logic
        current_time = pygame.time.get_ticks()
        if is_moving and current_time - frame_count > animation_speed:
                frame_count = current_time
                current_frame = (current_frame + 1) % len(cat_walk_frames)
                cat_image = cat_walk_frames[current_frame]
        elif not is_moving:
                cat_image = grey_cat
        
        # draw cat, draw tiles
        game_window.blit(tile_surface, (0, 0), area=(0, buffer_height, window_width, window_height))
        game_window.blit(cat_image, cat_rect)
        
        # update display
        pygame.display.update()
        clock.tick(60)
        
pygame.quit()
        
