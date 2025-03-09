import pygame
import sys
import importlib


# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Power Selection Game")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Set up fonts
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 36)



# Function for power selection
def select_power():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill(BLACK)

        title_text = font_large.render("Choose Your Power", True, WHITE)
        title_rect = title_text.get_rect(center=(window_width // 2, window_height // 4))
        window.blit(title_text, title_rect)

        fire_text = font_medium.render("1. Fire", True, RED)
        fire_rect = fire_text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(fire_text, fire_rect)

        water_text = font_medium.render("2. Water", True, BLUE)
        water_rect = water_text.get_rect(center=(window_width // 2, window_height // 2 + 60))
        window.blit(water_text, water_rect)

        air_text = font_medium.render("3. Air", True, YELLOW)
        air_rect = air_text.get_rect(center=(window_width // 2, window_height // 2 + 120))
        window.blit(air_text, air_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    fire_power = importlib.import_module("fire_power")
                    fire_power.play_game()
                elif event.key == pygame.K_2:
                    water_power = importlib.import_module("water_power")
                    water_power.play_game()
                elif event.key == pygame.K_3:
                    air_power = importlib.import_module("air_power")
                    air_power.play_game()

# Call the power selection function
select_power()
