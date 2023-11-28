import pygame

pygame.init()

#game window
window_width = 800
window_height = 1200

game_window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Crossing Game")

#load images
cat_image = pygame.image.load('C:/Users/niede/Pictures/cat_walk_1.png')
cat_walk_frames = [pygame.image.load(f'C:/Users/niede/Pictures/cat_walk_{i}.png') for i in range(1, 3+1)]
background_image = pygame.image.load('C:/Users/niede/Pictures/background.png')
stationary_cat_image = pygame.transform.scale(cat_walk_frames[0], (100, 100))

#resize the cat
smaller_cat_image = pygame.transform.scale(cat_image, (100, 100))

cat_rect = smaller_cat_image.get_rect()
cat_rect.x = window_width // 2 - cat_rect.width // 2  # Center horizontally
cat_rect.y = window_height - cat_rect.height - 150  # Align to the bottom

#game loop
running = True
clock = pygame.time.Clock()
animation_speed = 100
frame_count = 0
current_frame = 0
cat_speed = 5
bg_speed = 5
background_y = 0
is_moving = False

while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        #check key presses
        keys = pygame.key.get_pressed()
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
                background_y += bg_speed
                is_moving = True
        if keys[pygame.K_s]:
                background_y -= bg_speed
                is_moving = True

        #animation logic
        current_time = pygame.time.get_ticks()
        if is_moving and current_time - frame_count > animation_speed:
                frame_count = current_time
                current_frame = (current_frame + 1) % len(cat_walk_frames)
                cat_image = cat_walk_frames[current_frame]
                smaller_cat_image = pygame.transform.scale(cat_image, (100, 100))
        elif not is_moving:
                smaller_cat_image = stationary_cat_image
                
        game_window.fill((255, 255, 255))
        game_window.blit(background_image, (0, background_y))
        
        #draw cat
        game_window.blit(smaller_cat_image, cat_rect)
        
        #update display
        pygame.display.update()
        clock.tick(60)
        
pygame.quit()
        
