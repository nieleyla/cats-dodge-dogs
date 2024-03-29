# Imports
import os
import platform
import json
import pygame
import random
import numpy as np
from perlin_noise import PerlinNoise

from constants import *


# Functions

## Saving and loading

### Get platform-specific path to save directory
def get_save_path(app_name=GAME_TITLE):
    try:
        home = os.path.expanduser('~')
        if platform.system() == 'Windows':
            return os.path.join(os.getenv('APPDATA', home), app_name)
        elif platform.system() == 'Darwin':  # macOS
            return os.path.join(home, 'Library', 'Application Support', app_name)
        else:  # Linux and other Unix-like OS
            return os.path.join(home, '.local', 'share', app_name)
    except Exception:
        return os.path.join(os.getcwd(), app_name)

### Save game data to file
def save_game_data(data, app_name=GAME_TITLE, file_name=SAVE_FILE_NAME):
    save_path = get_save_path(app_name)
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, file_name)
    with open(file_path, 'w') as file:
        json.dump(data, file)

### Load game data from file
def load_game_data(app_name=GAME_TITLE, file_name=SAVE_FILE_NAME):
    file_path = os.path.join(get_save_path(app_name), file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {"highscore": 0}

### Delete save data
def delete_save_data(app_name=GAME_TITLE, file_name=SAVE_FILE_NAME):
    file_path = os.path.join(get_save_path(app_name), file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

### Write high score to file
def write_high_score(score):
    data = load_game_data()
    if data is None:
        data = {'highscore': score}
    else:
        data['highscore'] = max(score, data['highscore'])
    save_game_data(data)


## Asset loading and sprite extraction

### Loading sprite sheet from file
def load_sprite_sheet(filename):
    return pygame.image.load(filename).convert_alpha()

def get_sprite(sheet, x, y, width, height, scale_x, scale_y):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    if scale_x and scale_y:
        sprite = pygame.transform.scale(sprite, (width*scale_x, height*scale_y))
    return sprite

def generate_sprites(sheet, coordinates, scale_x, scale_y):
    sprites = {}
    for direction, coordinates in coordinates.items():
        sprites[direction] = [get_sprite(sheet, *coord, scale_x, scale_y) for coord in coordinates]
    if 'E' in sprites and 'W' not in sprites:
        sprites['W'] = [pygame.transform.flip(sprite, True, False) for sprite in sprites['E']]
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
            noise_surface = pygame.Surface((NOISE_SURFACE_SIZE, NOISE_SURFACE_SIZE), pygame.SRCALPHA).convert_alpha()
            noise_surface.fill((0, 0, 0, NOISE_ALPHA))
            noise_surface.set_alpha(noise([x / WORLD_WIDTH, y / WORLD_HEIGHT]) * 255)
            world_surface.blit(noise_surface, (x, y))


## Drawing UI

### Fading to black
def fade_black(frames):
    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)).convert_alpha()
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        game_window.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(frames)

### Flashing the screen red
def flash_screen_red():
    flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)).convert_alpha()
    flash_surface.fill((255, 0, 0))
    for alpha in range(0, 32, 4):
        flash_surface.set_alpha(alpha)
        game_window.blit(flash_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)

### Drawing the completions counter
def draw_counter(border_reaches):
    text = font.render(f"score: {border_reaches}", True, (255, 255, 255))
    text_shadow = font.render(f"score: {border_reaches}", True, (0, 0, 64))
    game_window.blit(text_shadow, (WINDOW_WIDTH // 2 + 220 + 2, 45+2))
    game_window.blit(text, (WINDOW_WIDTH // 2 + 220, 45))

### Drawing the high score counter
def draw_high_score(high_score):
    text = font.render(f"high score: {high_score}", True, (255, 255, 255))
    text_shadow = font.render(f"high score: {high_score}", True, (0, 0, 64))
    game_window.blit(text_shadow, (WINDOW_WIDTH // 2 + 140 + 2, 85+2))
    game_window.blit(text, (WINDOW_WIDTH // 2 + 140, 85))

### Drawing the progress bar
def draw_progress_bar(viewport_y):
    progress = (WORLD_HEIGHT - WINDOW_HEIGHT - viewport_y) / (WORLD_HEIGHT - WINDOW_HEIGHT)
    bar_length = 225  # Total length of the bar
    filled_length = bar_length * progress
    pygame.draw.rect(game_window, (0, 0, 0), (20 + 2, 20 + 2, bar_length, 20))  # Draw the shadow of the bar
    pygame.draw.rect(game_window, (255, 255, 255), (20, 20, bar_length, 20))  # Draw the border of the bar
    pygame.draw.rect(game_window, (0, 255, 0), (20, 20, filled_length, 20))  # Draw the filled part of the bar

### Drawing the health hearts
def draw_hearts(health):
    for i in range(health + 1):
        game_window.blit(ui['heart_bg'], (WINDOW_WIDTH // 2 - 56 + i * 48 + 2, 16 + 2))
        game_window.blit(ui['heart'], (WINDOW_WIDTH // 2 - 56 + i * 48, 16))
        game_window.blit(ui['heart_border'], (WINDOW_WIDTH // 2 - 56 + i * 48, 16))

### Drawing the level border
def draw_level_border():
    # Fill the border area with a gradient
    for y in range(BORDER_Y, BORDER_Y + BORDER_HEIGHT):
        for x in range(WORLD_WIDTH):
            # Calculate alpha based on distance from the top of the border
            alpha = 255 - (y - BORDER_Y) / BORDER_HEIGHT * 255
            fade_surface = pygame.Surface((1, 1), pygame.SRCALPHA).convert_alpha()
            fade_surface.fill((0, 0, 0, alpha))
            world_surface.blit(fade_surface, (x, y))

### Drawing the horizon
def draw_horizon():
    game_window.blit(ui['overlay_horizon'], (0, 0))

### Drawing the 'UP' arrow
def draw_arrow(viewport_y, size=128, color=(255, 255, 0), alpha=128):
    position = (WINDOW_WIDTH // 2 - size // 2, WINDOW_HEIGHT // 3 - (viewport_y - 2400))  # Position of the arrow
    # Create a surface for the arrow
    arrow_surface = pygame.Surface((size, size), pygame.SRCALPHA).convert_alpha()
    arrow_surface.fill((0, 0, 0, 0))  # Make the surface fully transparent
    # Define points for the arrow
    arrow_points = [
        (size // 2, 0),             # Top point
        (size, size),               # Bottom right
        (size // 2, size * 2 // 3), # Middle
        (0, size)                   # Bottom left
    ]
    alpha = 180 + 60 * np.sin(pygame.time.get_ticks() / 256)
    pygame.draw.polygon(arrow_surface, color + (alpha,), arrow_points)
    game_window.blit(arrow_surface, position)


## Drawing the level end screen
def draw_end_screen(border_reaches, old_high_score=0):
    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade_surface.fill((0, 0, 0))
        
    text = font.render(f"score: {border_reaches}", True, (255, 255, 255))
    text_hs = font.render("NEW HIGH SCORE!", True, (255, 255, 0))
    text_ss = font.render("YOU UNLOCKED SPECIAL MUSIC AND START SCREEN!", True, (255, 190, 200))
    for alpha in np.linspace(0, 255, 60):
        fade_surface.set_alpha(alpha)
        text.set_alpha(alpha)
        text_ss.set_alpha(alpha)
        text_hs.set_alpha(alpha)
        game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
        delay = 10
        if border_reaches > old_high_score:
            game_window.blit(text_hs, (WINDOW_WIDTH // 2 - text_hs.get_width() // 2, WINDOW_HEIGHT // 2 + 50 - text_hs.get_height() // 2))
            delay = 20
        if border_reaches >= SPECIAL_SCORE:
            game_window.blit(text_ss, (WINDOW_WIDTH // 2 - text_ss.get_width() // 2, WINDOW_HEIGHT // 2 + 100 - text_ss.get_height() // 2))
            delay = 50
        game_window.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(delay)
    pygame.display.update()

## Drawing the game over screen: Fade in 'screen_death' from ui and then
def draw_game_over_screen(border_reaches):
    pygame.mixer.music.stop()
    sounds['you-died'].play()

    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        game_window.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(20)

    # Fading in "YOU DIED" text
    for size in np.linspace(10, 100, 100):  # Gradual increase in text size
        text = pygame.font.Font.render(font, "YOU DIED", True, (255, 0, 0))
        text = pygame.transform.scale(text, (int(text.get_width() * (size / 100)), int(text.get_height() * (size / 100))))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        game_window.blit(fade_surface, (0, 0))
        game_window.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(10)
    pygame.time.delay(500)

    # Display border reaches
    reach_text = pygame.font.Font.render(font, f"score: {border_reaches}", True, (255, 255, 255))
    reach_rect = reach_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
    game_window.blit(reach_text, reach_rect)
    pygame.display.update()

    # Display high score
    high_score = load_game_data()["highscore"]
    msg = f"high score: {high_score}"
    color = (255, 255, 255)
    high_score_text = pygame.font.Font.render(font, msg, True, color)
    high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 120))
    game_window.blit(high_score_text, high_score_rect)
    pygame.display.update()
    pygame.time.delay(1000)

    # Stop sound effect and resume music
    sounds['you-died'].stop()
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

### Displaying credits
def display_credits():
    with open(os.path.join(os.path.dirname(__file__), f'assets/ui/credits.txt'), 'r') as file:
        credits_text = file.readlines()

    fade_black(10)
    credits = True
    while credits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()

        for i, line in enumerate(credits_text):
            text = font.render(line.strip(), True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 100 + i * 30))
            game_window.blit(text, text_rect)

        if keys[pygame.K_c]:
            credits = False
            fade_black(10)
        pygame.display.update()

### Displaying keybinds
def display_keybinds():
    fade_black(10)
    keybinds = True
    while keybinds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        color = (85, 170, 170) if load_game_data()["highscore"] < SPECIAL_SCORE else (254, 140, 180)
        pygame.draw.rect(game_window, color, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        game_window.blit(ui['screen_keybinds'], (0, 0))

        # Assign text_color so it fades in and out
        text_color = (155 + 100 * np.sin(pygame.time.get_ticks() / 256),) * 3
        text = font.render("PRESS ANY KEY TO CONTINUE", True, text_color).convert_alpha()
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 500))
        game_window.blit(text, text_rect)

        if any(keys):
            keybinds = False
            fade_black(10)

        pygame.display.update()

### Displaying the menu
def display_menu(cursor, ui, border_reaches=0):
    fade_black(10)
    menu = True

    while menu:
        pygame.draw.rect(game_window, (0, 0, 0, 0), START_BUTTON_COORDINATES) # Start button rect
        game_window.blit(ui['screen_start'], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        game_window.blit(cursor, pygame.mouse.get_pos())

        # Check for input
        if keys[pygame.K_m]:
            if pygame.mixer.music.get_volume() == 0.0:
                pygame.mixer.music.set_volume(0.2)
                pygame.time.delay(250) # Lazy way to debounce
            else:
                pygame.mixer.music.set_volume(0.0)
                pygame.time.delay(250) # Lazy way to debounce
        
        if keys[pygame.K_q]:
            pygame.quit()
            quit()
        if keys[pygame.K_c]:
            display_credits()
        if keys[pygame.K_DELETE]:
            delete_save_data()
            pygame.quit()

        if pygame.mouse.get_pressed()[0] or keys[pygame.K_RETURN] or keys[pygame.K_ESCAPE]:
            if pygame.Rect(START_BUTTON_COORDINATES).collidepoint(pygame.mouse.get_pos()) or keys[pygame.K_RETURN]:
                menu = False
                fade_black(10)
        
        if DEBUG:
            # Cheat/debug keys
            if keys[pygame.K_1]:
                border_reaches += 1
                high_score = border_reaches
                write_high_score(high_score)
                pygame.time.delay(100)
            if keys[pygame.K_2]:
                border_reaches = 0
                high_score = border_reaches
                write_high_score(high_score)
                pygame.time.delay(100)

        high_score = load_game_data()["highscore"]
        draw_counter(border_reaches)
        draw_high_score(high_score)
        pygame.display.update()


## Animation

### Retrieval of current animation frame
def get_animation_frame(sprites, horizontal_movement, vertical_movement, current_frame, frame_count, last_movement, walk_frames, animation_speed, type=None):
    current_time = pygame.time.get_ticks()
    offset = (0, 0)

    if current_time - frame_count > animation_speed:
        frame_count = current_time
        current_frame = (current_frame + 1) % walk_frames

    try:
        if vertical_movement < 0:  # Moving down
            image = sprites['S'][current_frame]
            last_movement = 'S'
            offset = (0, -10)
        if vertical_movement > 0:  # Moving up
            image = sprites['N'][current_frame]
            last_movement = 'N'
        if horizontal_movement > 0:  # Moving right
            image = sprites['E'][current_frame]
            last_movement = 'E'
            offset = (-30, 0)
        if horizontal_movement < 0:  # Moving left
            image = sprites['W'][current_frame]
            last_movement = 'W'
            offset = (-10, 0)
        if horizontal_movement > 0 and vertical_movement < 0:  # Moving down-right
            image = sprites['SE'][current_frame]
            last_movement = 'SE'
            offset = (-40, 10)
        if horizontal_movement > 0 and vertical_movement > 0:  # Moving up-right
            image = sprites['NE'][current_frame]
            last_movement = 'NE'
            offset = (-40, 10)
        if horizontal_movement < 0 and vertical_movement < 0:  # Moving down-left
            image = sprites['SW'][current_frame]
            last_movement = 'SW'
        if horizontal_movement < 0 and vertical_movement > 0:  # Moving up-left
            image = sprites['NW'][current_frame]
            last_movement = 'NW'
            offset = (0, 10)
        if horizontal_movement == 0 and vertical_movement == 0:  # Idle
            idle_mapping = {'N': 0, 'NE': 1, 'E': 1, 'SE': 1, 'S': 2, 'SW': 2, 'W': 3, 'NW': 3}
            image = sprites['ID'][idle_mapping[last_movement]]
            offset = (-50, 0) if last_movement == 'E' else offset
    except KeyError:
        image = sprites['E'][0]
    
    offset = (0, 0) if type == "dog" else offset
    return image, current_frame, frame_count, last_movement, offset

### Drawing a character
def draw_character(image, rect, viewport_y, offset=(0, 0), type=None):
    draw_rect = rect.move(offset)
    screen_y = draw_rect.y - viewport_y
    game_window.blit(image, (draw_rect.x, screen_y))
    if DEBUG:
        bound_rect = (draw_rect.x, screen_y, draw_rect.width, draw_rect.height)
        pygame.draw.rect(game_window, (255, 0, 0), bound_rect, 1)
        if type == "cat":
            collision_rect = rect.scale_by(CAT_HITBOX_SCALE_X, CAT_HITBOX_SCALE_Y)
            collision_rect.y -= viewport_y
        if type == "dog":
            collision_rect = rect.scale_by(DOG_HITBOX_SCALE_X, DOG_HITBOX_SCALE_Y)
            collision_rect.y -= viewport_y
        pygame.draw.rect(game_window, (0, 255, 0), collision_rect, 1)

### Picking a dog
def pick_dog(dogs=[]):
    dog_weights = DOG_BASE_WEIGHTS.copy()
    # Increase the weight of exotic and boss dogs based on the number of dogs
    dog_weights['boss_walking'] += len(dogs)*0.1
    dog_weights['boss_boxing'] += len(dogs)*0.05
    # Normalize weights
    dog_weights = {k: v / sum(dog_weights.values()) for k, v in dog_weights.items()}
    # Pick a dog
    return np.random.choice(list(dog_weights.keys()), p=list(dog_weights.values()))

### Dog spawn position function
def get_dog_spawn(dog_rects, border_reaches):
    # Calculate dynamic gap for this turn (decreses with each border reach)
    dynamic_gap = max(MIN_GAP - border_reaches * GAP_REDUCTION_FACTOR, REF_DOG_WIDTH)
    # Calculate the maximum spawn height
    upper_limit = WORLD_HEIGHT-(WORLD_HEIGHT - VIEWPORT_BUFFER)
    # Calculate the minimum spawn height
    lower_limit = dog_start_y
    
    tries = 0
    while True:
        if tries >= MAX_SPAWN_TRIES:
            break
        # Randomize the spawn position within the allowed range
        spawn_pos = random.randint(*sorted([lower_limit, upper_limit]))
        tries += 1
        # Check if the spawn position is too close to another dog
        if all([abs(spawn_pos - dog_rect.y) > dynamic_gap for dog_rect in dog_rects]):
            break
    return (REF_DOG_WIDTH, spawn_pos)


# Game Loop
def game_loop(sprites, cursor, ui, cat_rect, dog_rects, sounds, viewport_y=WORLD_HEIGHT-WINDOW_HEIGHT, border_reaches=0, high_score=0):

    ## Initialization
    running = True
    clock = pygame.time.Clock()
    
    ### Animation initialization
    first_run = True
    last_cat_movement = 'N'
    last_dog_movements = ['E']
    current_cat_frame = 0
    current_dog_frames = [0]
    cat_frame_count = 0
    dog_frame_counts = [0]
    horizontal_cat_movement = 0
    vertical_cat_movement = 0
    horizontal_dog_movements = [1]
    vertical_dog_movements = [0]
    dog_speeds = [DOG_SPEED_X]
    dog_images = [None]
    dogs = ['dog_white']
    health = DEFAULT_HEALTH
    last_hit = 0

    display_keybinds()

    ## Main game loop
    while running:
        for event in pygame.event.get():

            ### Quitting the game
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        ### Check for ui input
        if keys[pygame.K_ESCAPE] or first_run:
            first_run = False
            display_menu(cursor, ui, border_reaches)

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
        for i in range(len(dogs)):
            if dog_rects[i].x <= 0:
                horizontal_dog_movements[i] = 1
                vertical_dog_movements[i] = 0
            if dog_rects[i].x >= WINDOW_WIDTH - dog_rects[i].width:
                horizontal_dog_movements[i] = -1
                vertical_dog_movements[i] = 0
            
            #### Dog speed increases with each border reach
            dog_speeds[i] = min((DOG_SPEED_X + 2*border_reaches*random.randint(1, 100)*0.01), DOG_SPEED_CAP)

            #### Apply dog movement
            dog_rects[i].x += horizontal_dog_movements[i] * dog_speeds[i]
            dog_rects[i].y -= vertical_dog_movements[i]
        
        #### Check for border collision
        if cat_rect.top <= viewport_y - cat_rect.height:
            border_reaches += 1
            picked_dog = pick_dog(dogs)
            dogs.append(picked_dog)
            old_high_score = load_game_data()["highscore"]
            high_score = border_reaches
            write_high_score(high_score)
            dog_spawn = get_dog_spawn(dog_rects, border_reaches)
            if picked_dog in ['boss_walking', 'boss_boxing']:
                dog_rects.append(idle_boss.get_rect(center=dog_spawn))
            else:
                dog_rects.append(idle_dog.get_rect(center=dog_spawn))
            horizontal_dog_movements.append(1)
            vertical_dog_movements.append(0)
            last_dog_movements.append(random.choice(['E','W']))
            dog_frame_counts.append(0)
            current_dog_frames.append(0)
            dog_images.append(None)
            dog_speeds.append(DOG_SPEED_X)
            sounds['level-complete'].play()
            draw_end_screen(border_reaches, old_high_score)
            cat_rect.y = WORLD_HEIGHT - 150 - REF_CAT_HEIGHT
            viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT

        ### Check for dog collision
        for i, dog in enumerate(dogs):
            if cat_rect.scale_by(CAT_HITBOX_SCALE_X, CAT_HITBOX_SCALE_Y).colliderect(dog_rects[i].scale_by(DOG_HITBOX_SCALE_X, DOG_HITBOX_SCALE_Y)):
                if pygame.time.get_ticks() - last_hit <= IMMUNITY_TIME:
                    pass
                elif health > 0 and pygame.time.get_ticks() - last_hit > IMMUNITY_TIME:
                    # cat_hurt = True
                    last_hit = pygame.time.get_ticks()
                    if dog in DOUBLE_DAMAGE_DOGS:
                        sounds['cat-hurt-hard'].play()
                        health -= 2
                    else:
                        sounds['cat-hurt-light'].play()
                        health -= 1
                    flash_screen_red()
                    horizontal_dog_movements[i] = -horizontal_dog_movements[i]*4
                    vertical_dog_movements[i] = vertical_cat_movement*2
                else:
                    draw_game_over_screen(border_reaches)
                    cat_rect.y = WORLD_HEIGHT - 150 - REF_CAT_HEIGHT
                    viewport_y = WORLD_HEIGHT - WINDOW_HEIGHT
                    dogs = [pick_dog()]
                    write_high_score(border_reaches)
                    border_reaches = 0
                    health = DEFAULT_HEALTH
                    display_menu(cursor, ui)

        ### Drawing the visible part of the world
        visible_rect = pygame.Rect(0, viewport_y, WINDOW_WIDTH, WINDOW_HEIGHT)
        game_window.blit(world_surface, (0, 0), visible_rect)

        ### Animation
        cat_image, current_cat_frame, cat_frame_count, last_cat_movement, offset = get_animation_frame(sprites['cat_grey'], horizontal_cat_movement, vertical_cat_movement, current_cat_frame, cat_frame_count, last_cat_movement, CAT_WALK_FRAMES, CAT_ANIMATION_SPEED, type="cat")
        draw_character(cat_image, cat_rect, viewport_y, offset, type="cat")
        
        for i in range(len(dogs)):
            dog_images[i], current_dog_frames[i], dog_frame_counts[i], last_dog_movements[i], offset = get_animation_frame(sprites[dogs[i]], horizontal_dog_movements[i], vertical_dog_movements[i], current_dog_frames[i], dog_frame_counts[i], last_dog_movements[i], DOG_WALK_FRAMES, DOG_ANIMATION_SPEED/(0.5*(border_reaches+1)), type="dog")
            draw_character(dog_images[i], dog_rects[i], viewport_y, type="dog")

        ### Drawing UI
        draw_arrow(viewport_y, 96, (200, 200, 150), 200)
        draw_horizon()
        draw_counter(border_reaches)
        draw_progress_bar(viewport_y)
        draw_hearts(health)

        ### Reset
        horizontal_cat_movement = 0
        vertical_cat_movement = 0

        ### Game clock
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit(0)



# Main function
if __name__ == "__main__":
    
    ## Windows-specific instructions
    if platform.system() == 'Windows':
        os.system('cls')
        print(f"\n\nWelcome to {GAME_TITLE}!\n\n\nYou can safely minimize (not close) this console window.\nThis window needs to be opened - otherwise Windows will be suspicious of the game and block it from running.") # This is because Microsoft decided to be extremely paranoid about PyInstaller-generated executables such as this one. Boo!!
        print(f"\n\nSince we need to open this window, we might as well use it to give you some cool cat facts.\nHere's your cat fact of the day:\n")
        with open(os.path.join(os.path.dirname(__file__), os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/ui/cat-facts.txt'))), 'r', encoding="utf-8") as file:
            cat_facts = file.readlines()
            print(random.choice(cat_facts))
        print("\n\nNow enjoy the game - and try to reach a score of 10 for a surprise!!\n\n")
        print("  ／l、\n（ﾟ､ ｡ ７\n  l  ~ヽ\n  じしf_,)ノ\n") # Cat ASCII art
    else:
        print("Uhh... I don't know why you're reading this, but you're not on Windows, so you can just ignore this message and minimize this window. Enjoy the game, I guess? :p")

    ## Initialize Pygame
    pygame.init()
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    pygame.display.set_icon(pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/ui/icon.png'))).convert_alpha())

    ## Load assets

    ### Load, pregenerate, and store sprites
    sprites = {sprite: generate_sprites(load_sprite_sheet(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/sprites/{sprite}.png'))).convert_alpha(), SPRITE_COORDINATES[sprite], SPRITE_SCALES[0][sprite], SPRITE_SCALES[1][sprite]) for sprite in SPRITE_LIST}
    sprites.update({'grass': [get_sprite(load_sprite_sheet(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/sprites/grass.png'))).convert(), *coord, TILE_SCALE, TILE_SCALE) for coord in GRASS_COORDINATES]})
    # sprites.update({'plant': [get_sprite(load_sprite_sheet(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/sprites/plants.png'))).convert(), *coord, TILE_SCALE, TILE_SCALE) for coord in PLANT_COORDINATES]})
    
    ### Load and store UI elements
    ui = {ui_element: pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/ui/{ui_element}.png'))).convert_alpha() for ui_element in UI_LIST}
    font = pygame.font.Font(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/ui/pico-8.otf')), 24)

    ### Resize UI elements
    ui['heart'] = pygame.transform.scale(ui['heart'], (int(ui['heart'].get_width() * 2), int(ui['heart'].get_height() * 2))).convert_alpha()
    ui['heart_bg'] = pygame.transform.scale(ui['heart_bg'], (int(ui['heart_bg'].get_width() * 2), int(ui['heart_bg'].get_height() * 2))).convert_alpha()
    ui['heart_border'] = pygame.transform.scale(ui['heart_border'], (int(ui['heart_border'].get_width() * 2), int(ui['heart_border'].get_height() * 2))).convert_alpha()
    
    ### Load and store sounds
    sounds = {sound: pygame.mixer.Sound(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/audio/sounds/{sound}.mp3'))) for sound in SOUNDS.keys()}
    for sound, volume in SOUNDS.items():
        sounds[sound].set_volume(volume)

    ## Load high score and special assets if applicable
    high_score = load_game_data()["highscore"]
    if high_score >= SPECIAL_SCORE:
        pygame.mixer.music.load(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/audio/music/blippy_trance.mp3')))
        ui['screen_start'] = ui['screen_start_special']
        cursor = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/ui/cursor_black.cur'))).convert_alpha()
    else:
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), f'assets/audio/music/doobly_doo.mp3'))
        ui['screen_start'] = ui['screen_start_normal']
        cursor = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), f'assets/ui/cursor_grey.cur'))).convert_alpha()

    ## Initialize game world
    world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT)).convert()
    fill_world_with_tiles([sprites['grass'],]) # plant_textures])
    draw_noise()

    ## Initialize characters
    ### Initialize cat   
    cat_start_y = WORLD_HEIGHT - int(0.25*WINDOW_HEIGHT) - REF_CAT_HEIGHT
    idle_cat = sprites['cat_grey']['ID'][0]
    cat_rect = idle_cat.get_rect(center=(WINDOW_WIDTH // 2, cat_start_y))
    ### Initialize dog
    dog_start_y = WORLD_HEIGHT - WINDOW_HEIGHT - REF_DOG_HEIGHT
    idle_dog = sprites['dog_white']['E'][0]
    idle_boss = sprites['boss_walking']['E'][0]
    dog_rects = [idle_dog.get_rect(center=(REF_DOG_WIDTH, dog_start_y))]

    ## Start the game
    pygame.mouse.set_visible(False)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    game_loop(sprites, cursor, ui, cat_rect, dog_rects, sounds, high_score=high_score)
