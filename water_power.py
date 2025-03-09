import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Vighnesh's Water Power Game")

# Player settings
player_size = 50
player_x = 50
player_y = window_height // 2 - player_size // 2

# Load fish image
player_image = pygame.image.load('fish.png')
player_image = pygame.transform.scale(player_image, (50, 50))

# Load shark image
shark_image = pygame.image.load('shark.png')
shark_image = pygame.transform.scale(shark_image, (50, 50))

# Load heart image
heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Load water background image
underwater_bg = pygame.image.load('underwater_bg.png')
underwater_bg = pygame.transform.scale(underwater_bg, (window_width, window_height))


# Colors
WHITE = (255, 255, 255)
AQUA_BLUE = (102, 204, 255)
LIGHT_BLUE = (153, 204, 255)
DARK_BLUE = (0, 51, 102)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Enemy settings
enemy_size = 50
enemy_speed = 2
enemies = []

# Score
score = 0
font_medium = pygame.font.Font(None, 36)

# Game controls
font_small = pygame.font.Font(None, 24)
controls_text = font_small.render("Controls: UP/DOWN arrow or W/S key to move, ESC to pause", True, AQUA_BLUE)
controls_rect = controls_text.get_rect(topleft=(10, 10))

# Game over controls
game_over_font = pygame.font.Font(None, 48)
game_over_text = game_over_font.render("Game Over", True, AQUA_BLUE)
game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2))

# Pause controls
paused = False
pause_text = font_small.render("PAUSED", True, AQUA_BLUE)
pause_rect = pause_text.get_rect(center=(window_width // 2, window_height // 2))

# Difficulty settings
difficulty_levels = [
    {'name': 'Easy', 'spawn_interval': 1500, 'countdown_time': 30},
    {'name': 'Medium', 'spawn_interval': 1000, 'countdown_time': 60},
    {'name': 'Hard', 'spawn_interval': 800, 'countdown_time': 90},
    {'name': 'Expert', 'spawn_interval': 600, 'countdown_time': 120},
    {'name': 'Insane', 'spawn_interval': 400, 'countdown_time': 150}
]
current_level = 0
current_difficulty = difficulty_levels[current_level]
countdown_time = current_difficulty['countdown_time'] * 1000  # Convert to milliseconds

# Countdown timer
countdown_timer = pygame.time.get_ticks() + countdown_time
timer_font = pygame.font.Font(None, 48)

# Lives
lives = 3
heart_spacing = 40

# Highest score
highest_score = 0

# Load highest score from file
def load_highest_score():
    try:
        with open("high_score.txt", "r") as file:
            highest_score = int(file.read())
    except FileNotFoundError:
        highest_score = 0

    return highest_score

# Save highest score to file
def save_highest_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Function to display the game description
def display_description():
    description_font = pygame.font.Font(None, 36)
    description_text = description_font.render("Welcome to Vighnesh's Water Power Game!", True, BLACK)
    instructions_text = description_font.render("Press any key to start the game", True, BLACK)
    description_rect = description_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
    instructions_rect = instructions_text.get_rect(center=(window_width // 2, window_height // 2 + 50))

    window.fill(WHITE)
    window.blit(description_text, description_rect)
    window.blit(instructions_text, instructions_rect)
    pygame.display.update()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting_for_start = False

# Function to spawn sharks
def spawn_shark():
    shark_y = random.randint(0, window_height)
    enemies.append({'x': window_width, 'y': shark_y})

# Function to check collision with player
def check_collision(player_x, player_y, enemy_x, enemy_y):
    distance = ((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2) ** 0.5
    return distance < (player_size + enemy_size) / 2

# Start the game
def play_game():
    global player_y, score, paused, current_level, current_difficulty, countdown_time, countdown_timer, lives, highest_score

    clock = pygame.time.Clock()
    game_over = False
    spawn_timer = 0
    spawn_interval = current_difficulty['spawn_interval']
    highest_score = load_highest_score()
    countdown_remaining = max(0, (countdown_timer - pygame.time.get_ticks()) // 1000)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        if paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

            window.blit(pause_text, pause_rect)
            pygame.display.update()
            continue

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w] and player_y > 0:
                player_y -= 5
            if keys[pygame.K_DOWN] or keys[pygame.K_s] and player_y < window_height - player_size:
                player_y += 5

            window.fill(WHITE)
            window.blit(underwater_bg, (0, 0))
            window.blit(player_image, (player_x, player_y))

            # Spawn sharks
            if pygame.time.get_ticks() - spawn_timer >= spawn_interval:
                spawn_shark()
                spawn_timer = pygame.time.get_ticks()

            # Update and draw sharks
            for shark in enemies:
                shark['x'] -= enemy_speed
                window.blit(shark_image, (shark['x'], shark['y']))

                # Check collision with player
                if check_collision(player_x, player_y, shark['x'], shark['y']):
                    # Collision with player
                    lives -= 1
                    enemies.remove(shark)
                    if lives <= 0:
                        game_over = True
                elif shark['x'] + enemy_size < player_x:
                    # Player escaped from the shark
                    score += 1
                    enemies.remove(shark)

            # Draw lives
            for i in range(lives):
                heart_x = window_width - 10 - (i + 1) * heart_spacing
                window.blit(heart_image, (heart_x, 10))

            # Draw controls
            window.blit(controls_text, controls_rect)

            # Update and draw countdown and difficulty
            countdown_remaining = max(0, (countdown_timer - pygame.time.get_ticks()) // 1000)
            countdown_text = font_small.render("Next level in " + str(countdown_remaining), True, BLACK)
            countdown_rect = countdown_text.get_rect(topleft=(15, 100))
            difficulty_text = font_small.render("Difficulty: " + current_difficulty['name'], True, BLACK)
            difficulty_rect = difficulty_text.get_rect(topleft=(17, 50))
            window.blit(countdown_text, countdown_rect)
            window.blit(difficulty_text, difficulty_rect)

            pygame.display.update()

            # Increase difficulty level when countdown reaches 0
            if countdown_remaining <= 0:
                current_level += 1
                if current_level < len(difficulty_levels):
                    current_difficulty = difficulty_levels[current_level]
                    countdown_time = current_difficulty['countdown_time'] * 1000
                    countdown_timer = pygame.time.get_ticks() + countdown_time
                    spawn_interval = current_difficulty['spawn_interval']
                else:
                    game_over = True

        clock.tick(60)

    # Save highest score if the current score is higher
    if score > highest_score:
        highest_score = score
        save_highest_score(highest_score)

    # Game over
    window.fill(WHITE)
    game_over_text = game_over_font.render("Game Over", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
    window.blit(game_over_text, game_over_rect)

    highest_score_text = font_small.render("Highest Score: " + str(highest_score), True, BLACK)
    highest_score_rect = highest_score_text.get_rect(center=(window_width // 2, window_height // 2 + 20))
    window.blit(highest_score_text, highest_score_rect)

    current_score_text = font_small.render("Current Score: " + str(score), True, BLACK)
    current_score_rect = current_score_text.get_rect(center=(window_width // 2, window_height // 2 + 60))
    window.blit(current_score_text, current_score_rect)

    pygame.display.update()
    pygame.time.delay(2000)

    # Restart the game
    play_game()

# Main function
def main():
    display_description()
    play_game()

# Run the game
if __name__ == '__main__':
    main()
