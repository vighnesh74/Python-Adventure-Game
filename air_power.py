import pygame
import random
import os
import sys

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
TORNADO_SPEED = 3
INITIAL_DIFFICULTY = 30  # Seconds before difficulty level increases
DIFFICULTY_INCREASE = 30  # Seconds to add for each difficulty increase
SCORE_FONT = pygame.font.SysFont("comicsans", 30)

# Load images
PLAYER_IMAGE = pygame.image.load("player.png")  # Replace with the path to the player image
TORNADO_IMAGE = pygame.image.load("tornado.png")  # Replace with the path to the tornado image

# Load high score from the external file or set it to 0 if the file doesn't exist
HIGH_SCORE_FILE = "high_score.txt"
if os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tornado Escape Game")

class Player:
    def __init__(self):
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.hearts = 3

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Add boundaries to keep the player within the screen
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self):
        window.blit(self.image, self.rect)

class Tornado:
    def __init__(self):
        self.image = TORNADO_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def move(self, speed):
        # Implement tornado movement logic here
        self.rect.y += speed

    def draw(self):
        window.blit(self.image, self.rect)

def display_controls():
    # Display controls on the top-left corner
    controls_text = SCORE_FONT.render("Controls: Arrow Keys or W/S/A/D to Move", True, (255, 255, 255))
    window.blit(controls_text, (10, 10))

def display_score(current_score):
    # Display current score and high score on the screen
    score_text = SCORE_FONT.render(f"Score: {current_score}  High Score: {high_score}", True, (255, 255, 255))
    window.blit(score_text, (10, 40))

def display_difficulty(difficulty_time):
    # Display difficulty countdown on the top-right corner
    difficulty_text = SCORE_FONT.render(f"Difficulty: {difficulty_time}", True, (255, 255, 255))
    window.blit(difficulty_text, (WIDTH - difficulty_text.get_width() - 10, 10))

def display_game_over(current_score):
    game_over_text = SCORE_FONT.render("Game Over", True, (255, 0, 0))
    score_text = SCORE_FONT.render(f"Your Score: {current_score}", True, (255, 255, 255))
    high_score_text = SCORE_FONT.render(f"Highest Score: {high_score}", True, (255, 255, 255))
    menu_text = SCORE_FONT.render("Press 2 to go to Main Menu", True, (255, 255, 255))
    exit_text = SCORE_FONT.render("Press Q to Exit", True, (255, 255, 255))

    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))
    window.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 20))
    window.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 80))
    window.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 120))

def toggle_fullscreen():
    pygame.display.toggle_fullscreen()

# Create player and tornado objects
player = Player()
tornados = [Tornado() for _ in range(5)]

# Game loop
running = False  # Game will start after any key is pressed
clock = pygame.time.Clock()
current_score = 0
difficulty_time = INITIAL_DIFFICULTY
difficulty_timer = pygame.time.get_ticks()  # To track difficulty countdown

game_description = SCORE_FONT.render("Tornado Escape Game! Press any key to start.", True, (255, 255, 255))
fullscreen_text = SCORE_FONT.render("Press F to toggle fullscreen", True, (255, 255, 255))

while not running:
    window.fill((0, 0, 0))
    window.blit(game_description, (WIDTH // 2 - game_description.get_width() // 2, HEIGHT // 2))
    window.blit(fullscreen_text, (WIDTH // 2 - fullscreen_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                toggle_fullscreen()
            else:
                running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = not running  # Pause/unpause the game
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_f:
                toggle_fullscreen()

    if not running:
        continue

    # Handle player movement
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx = -PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx = PLAYER_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy = -PLAYER_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy = PLAYER_SPEED

    player.move(dx, dy)

    # Update game state and collision detection with tornados
    for tornado in tornados:
        tornado.move(TORNADO_SPEED + current_score // 10)  # Increase tornado speed with difficulty
        if player.rect.colliderect(tornado.rect):
            # If player collides with a tornado, decrease hearts
            player.hearts -= 1
            if player.hearts <= 0:
                running = False
            # Reset tornado position
            tornado.rect.x = random.randint(0, WIDTH - tornado.rect.width)
            tornado.rect.y = random.randint(-HEIGHT, -tornado.rect.height)
        # Check if the tornado is out of the screen and reset its position
        if tornado.rect.y > HEIGHT:
            tornado.rect.x = random.randint(0, WIDTH - tornado.rect.width)
            tornado.rect.y = random.randint(-HEIGHT, -tornado.rect.height)
            current_score += 1

    # Calculate difficulty countdown
    current_time = pygame.time.get_ticks()
    time_passed = (current_time - difficulty_timer) // 1000
    difficulty_time = INITIAL_DIFFICULTY + (current_score // 10) * DIFFICULTY_INCREASE - time_passed

    # Draw everything on the screen
    window.fill((0, 0, 0))
    player.draw()
    for tornado in tornados:
        tornado.draw()

    display_controls()
    display_score(current_score)
    display_difficulty(max(difficulty_time, 0))

    # Display hearts
    hearts_text = SCORE_FONT.render(f"Hearts: {'❤' * player.hearts}", True, (255, 0, 0))
    window.blit(hearts_text, (10, 70))

    pygame.display.update()
    clock.tick(60)

# Show game over screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2:
                # Run main_menu.py
                import main_menu
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_f:
                toggle_fullscreen()
            
    window.fill((0, 0, 0))
    display_game_over(current_score)
    pygame.display.update()
