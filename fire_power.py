import pygame
import random
import sys
import importlib

# Initialize pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Vighnesh's Fire Power Game")

# Player settings
player_size = 50
player_x = 50
player_y = window_height // 2 - player_size // 2

# Load player image
player_image = pygame.image.load('player_image.png')
player_image = pygame.transform.scale(player_image, (50, 50))


# Load robot image
robot_image = pygame.image.load('robot.png')
robot_image = pygame.transform.scale(robot_image, (50, 50))

# Load heart image
heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# Bullet settings
bullet_size = 10
bullet_speed = 10
bullet_color = RED
bullets = []

# Enemy settings
enemy_size = 50
enemy_speed = 2
enemies = []

# Score
score = 0
font_medium = pygame.font.Font(None, 36)

# Game controls
font_small = pygame.font.Font(None, 24)
controls_text = font_small.render("Controls: UP/DOWN arrow or W/S keyto move, SPACE to shoot, ESC to pause", True, RED)
controls_rect = controls_text.get_rect(topleft=(10, 10))

# Game over controls
game_over_font = pygame.font.Font(None, 48)
game_over_text = game_over_font.render("Game Over", True, RED)
game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2))

# Pause controls
paused = False
pause_text = font_small.render("PAUSED", True, RED)
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

# Function to spawn enemies
def spawn_enemy():
    enemy_y = random.randint(0, window_height - enemy_size)
    enemies.append({'x': window_width, 'y': enemy_y})

# Function to fire bullets
def fire_bullet():
    bullet_y = player_y + player_size // 2 - bullet_size // 2
    bullets.append({'x': player_x + player_size, 'y': bullet_y})

# Initialize pygame mixer for sound effects


# Define font sizes
font_small = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 72)

# Function to toggle fullscreen
def toggle_fullscreen():
    global window
    screen = pygame.display.get_surface()
    if screen.get_flags() & pygame.FULLSCREEN:
        pygame.display.set_mode((window_width, window_height))
    else:
        pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)

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
                if event.key == pygame.K_SPACE:
                    fire_bullet()
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key == pygame.K_f:
                    toggle_fullscreen()

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
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
                player_y -= 5
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_y < window_height - player_size:
                player_y += 5

            window.fill(WHITE)
            window.blit(player_image, (player_x, player_y))

            # Update and draw bullets
            for bullet in bullets[:]:
                bullet['x'] += bullet_speed
                pygame.draw.rect(window, bullet_color, (bullet['x'], bullet['y'], bullet_size, bullet_size))

                # Remove bullets when they go off-screen
                if bullet['x'] > window_width:
                    bullets.remove(bullet)

            # Spawn enemies
            if pygame.time.get_ticks() - spawn_timer >= spawn_interval:
                spawn_enemy()
                spawn_timer = pygame.time.get_ticks()

            # Update and draw enemies
            for enemy in enemies[:]:
                enemy['x'] -= enemy_speed
                window.blit(robot_image, (enemy['x'], enemy['y']))

                # Check collision with bullets
                for bullet in bullets[:]:
                    if bullet['x'] < enemy['x'] + enemy_size and bullet['x'] + bullet_size > enemy['x'] and \
                    bullet['y'] < enemy['y'] + enemy_size and bullet['y'] + bullet_size > enemy['y']:
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1
                        break

                # Check collision with player
                if player_x < enemy['x'] + enemy_size and player_x + player_size > enemy['x'] and \
                player_y < enemy['y'] + enemy_size and player_y + player_size > enemy['y']:
                    # Collision with player
                    lives -= 1
                    enemies.remove(enemy)
                    if lives <= 0:
                        game_over = True
                elif enemy['x'] + enemy_size < 0:
                    # Enemy passed the player
                    lives -= 1
                    enemies.remove(enemy)
                    if lives <= 0:
                        game_over = True

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
                    game_over = False

        else:
            # Game paused
            window.blit(pause_text, pause_rect)
            pygame.display.update()

        clock.tick(60)

    # Save highest score if the current score is higher
    if score > highest_score:
        highest_score = score
        save_highest_score(highest_score)

    # Game over
    window.fill(WHITE)
    game_over_text = font_large.render("Game Over", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
    window.blit(game_over_text, game_over_rect)

    highest_score_text = font_small.render("Highest Score: " + str(highest_score), True, BLACK)
    highest_score_rect = highest_score_text.get_rect(center=(window_width // 2, window_height // 2 + 20))
    window.blit(highest_score_text, highest_score_rect)

    current_score_text = font_small.render("Current Score: " + str(score), True, BLACK)
    current_score_rect = current_score_text.get_rect(center=(window_width // 2, window_height // 2 + 60))
    window.blit(current_score_text, current_score_rect)

    if score > highest_score:
        congrats_text = font_large.render("Congratulations! New High Score!", True, BLACK)
        congrats_rect = congrats_text.get_rect(center=(window_width // 2, window_height // 2 + 120))
        window.blit(congrats_text, congrats_rect)

    menu_text = font_small.render("Press 2 to go to main menu", True, BLACK)
    menu_rect = menu_text.get_rect(center=(window_width // 2, window_height // 2 + 160))
    window.blit(menu_text, menu_rect)

    exit_text = font_small.render("Press Q to exit", True, BLACK)
    exit_rect = exit_text.get_rect(center=(window_width // 2, window_height // 2 + 200))
    window.blit(exit_text, exit_rect)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    main_menu = importlib.import_module('main_menu')
                    main_menu.select_power()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Run the game
if __name__ == '__main__':
    play_game()
