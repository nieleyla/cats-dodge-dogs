import pygame

pygame.init()

window_width = 800
window_height = 1200

game_window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Crossing Game")

running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        pygame.display.update()
        
pygame.quit()
        
