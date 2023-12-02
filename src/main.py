import pygame

pygame.init()

#game window
window_width = 800
window_height = 1200
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Crossing Game")

#load images
sprite_sheet = pygame.image.load('assets/grey_cat_sprite.png')
grass_tile = pygame.image.load('assets/grass_texture.jpg')
tile_width, tile_height = grass_tile.get_size()

#extract sprites
def get_sprite(sheet, x, y, width, height):
    """Extracts and returns a single sprite from the sprite sheet."""
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

grey_cat = get_sprite(sprite_sheet, 394, 291, 11, 22)
grey_cat_walk_1 = get_sprite(sprite_sheet, 426, 292, 11, 22)
grey_cat_walk_2 = get_sprite(sprite_sheet, 458, 291, 11, 22)
grey_cat_walk_3 = get_sprite(sprite_sheet, 490, 292, 11, 22)
cat_walk_frames = [grey_cat_walk_1, grey_cat_walk_2, grey_cat_walk_3]

#resize the cat
grey_cat = pygame.transform.scale(grey_cat, (33, 66))
cat_walk_frames = [pygame.transform.scale(frame, (33, 66)) for frame in cat_walk_frames]

#cat_rect = smaller_cat_image.get_rect()
cat_rect = grey_cat.get_rect()
cat_rect.x = window_width // 2 - cat_rect.width // 2  # Center horizontally
cat_rect.y = window_height - cat_rect.height - 150  # Align to the bottom

tile_positions = []
for y in range(0, window_height, tile_height):
        for x in range(0, window_width, tile_width):
                tile_positions.append((x, y))

#game loop
running = True
clock = pygame.time.Clock()
animation_speed = 100
frame_count = 0
current_frame = 0
cat_speed = 5
bg_speed = 5
background_movement_speed = 0
background_y = 0

while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        #check key presses
        keys = pygame.key.get_pressed()
        background_movement_speed = 0
        is_moving = False
       
        #move cat horizontally
        if keys[pygame.K_a]:
                cat_rect.x -= cat_speed
                is_moving = True
        if keys[pygame.K_d]:
                cat_rect.x += cat_speed
                is_moving = True
                
        # Move the background vertically
        if keys[pygame.K_w]:
                background_movement_speed = bg_speed
                is_moving = True
        if keys[pygame.K_s]:
                background_movement_speed = -bg_speed
                is_moving = True

        #animation logic
        current_time = pygame.time.get_ticks()
        if is_moving and current_time - frame_count > animation_speed:
                frame_count = current_time
                current_frame = (current_frame + 1) % len(cat_walk_frames)
                cat_image = cat_walk_frames[current_frame]
        elif not is_moving:
                cat_image = grey_cat

        for i, (x, y) in enumerate(tile_positions):
                y += background_movement_speed
                if y > window_height:
                        y -= window_height + tile_height
                elif y < -tile_height:
                        y += window_height + tile_height
                tile_positions[i] = (x, y)

        game_window.fill((255, 255, 255))
        for x, y in tile_positions:
                game_window.blit(grass_tile, (x, y))
        
        #draw cat
        game_window.blit(cat_image, cat_rect)
        
        #update display
        pygame.display.update()
        clock.tick(60)
        
pygame.quit()
        
