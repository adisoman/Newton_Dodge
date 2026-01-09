import pygame
import random
import sys
import os
import time

# === High Score Functions ===
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# Initialize Pygame
pygame.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


icon = pygame.image.load(resource_path("Newtoncon.png"))  # or "icon.ico" if using .ico format
pygame.display.set_icon(icon)

# Screen settings
screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Newton-Dodge")
clock = pygame.time.Clock()

# Load images with scaling
newton_img = pygame.transform.scale(pygame.image.load(resource_path("Player_Img.png")).convert_alpha(), (60, 60))
apple_img = pygame.transform.scale(pygame.image.load(resource_path("Apple_Img.png")).convert_alpha(), (40, 40))
gravity_anomaly_img = pygame.transform.scale(pygame.image.load(resource_path("Grav_Img.png")).convert_alpha(), (45, 45))
Megravity_img = pygame.transform.scale(pygame.image.load(resource_path("Megrav_Img.png")).convert_alpha(), (45, 45))
background_img = pygame.transform.scale(pygame.image.load(resource_path("Back_Img.png")).convert(), (600, 600))
slowdown_img = pygame.transform.scale(pygame.image.load(resource_path("Slowdown_Img.png")).convert_alpha(), (40, 40))
invincible_img = pygame.transform.scale(pygame.image.load(resource_path("Invinc_Img.png")).convert_alpha(), (40, 40))
life_img = pygame.transform.scale(pygame.image.load(resource_path("Life_Img.png")).convert_alpha(), (40, 40))
lightbulb_img = pygame.transform.scale(pygame.image.load(resource_path("Lightbulb_Img.png")).convert_alpha(), (40, 40))

# Game variables
newton_x, newton_y = screen_width // 2, screen_height - 100
newton_speed = 10
score = 0
high_score = load_high_score()
lives = 3
speed_increment = 0.05
object_speed = 5
slowdown_timer = 0
invincible_timer = 0
life_flash_timer = 0

# Object lists
apples = []
gravity_anomalies = []
megravities = []
slowdowns = []
invincibles = []
extra_lives = []
lightbulbs = []

physics_facts = [
    "Light behaves both as a particle and a wave.",
    "A black hole's gravity can bend light itself.",
    "The speed of light is 299,792,458 m/s.",
    "Energy and mass are equivalent: E=mc².",
    "Gravity affects time – it's called time dilation."
]

show_fact = False
fact_text = ""
countdown = 0
fact_screen_active = False


# Font settings
font = pygame.font.SysFont('Arial', 30)

# Functions

def draw_text(text, x, y, color=(255, 255, 255)):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def spawn_apple():
    x = random.randint(0, screen_width - 50)
    y = -50
    apples.append([x, y])

def spawn_anomaly():
    x = random.randint(0, screen_width - 50)
    y = -50
    gravity_anomalies.append([x, y])

def spawn_megravity():
    if random.randint(1,7) == 1:
        x = random.randint(0, screen_width - 50)
        y = -50
        megravities.append([x, y])

def spawn_slowdown():
    if random.randint(1, 500) == 1:
        x = random.randint(0, screen_width - 50)
        y = -50
        slowdowns.append([x, y])

def spawn_invincible():
    if random.randint(1, 1250) == 1:
        x = random.randint(0, screen_width - 50)
        y = -50
        invincibles.append([x, y])

def spawn_extra_life():
    if random.randint(1, 750) == 1:
        x = random.randint(0, screen_width - 50)
        y = -50
        extra_lives.append([x, y])

def spawn_lightbulb():
    if random.randint(1, 750) == 1:
        x = random.randint(0, screen_width - 50)
        y = -50
        lightbulbs.append([x, y])

# Display game over screen
def game_over_screen():
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart", True, (255, 255, 0))
    screen.blit(game_over_text, (screen_width // 2 - 75, screen_height // 2 - 80))
    screen.blit(high_score_text, (screen_width // 2 - 100, screen_height // 2 - 40))
    screen.blit(restart_text, (screen_width // 2 - 115, screen_height // 2 + 20))
    pygame.display.flip()

# Restart the game
def restart_game():
    global score, lives, object_speed, slowdown_timer, invincible_timer, apples, gravity_anomalies, megravities, slowdowns, invincibles
    score = 0
    lives = 3
    object_speed = 5
    slowdown_timer = 0
    invincible_timer = 0
    apples.clear()
    gravity_anomalies.clear()
    megravities.clear()
    slowdowns.clear()
    invincibles.clear()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()

    # Move Newton
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and newton_x > 0:
        newton_x -= newton_speed
    if keys[pygame.K_RIGHT] and newton_x < screen_width - 50:
        newton_x += newton_speed

    # Decrease timers
    if slowdown_timer > 0:
        slowdown_timer -= 1
    else:
        object_speed += speed_increment * 0.01

    if invincible_timer > 0:
        invincible_timer -= 1

    # Spawn objects
    if random.randint(1, 20) == 1:
        spawn_apple()
    if random.randint(1, 50) == 1:
        spawn_anomaly()
    if random.randint(1, 50) == 1:
        spawn_megravity()
    spawn_slowdown()
    spawn_invincible()
    spawn_extra_life()
    spawn_lightbulb()

    # Determine actual speed
    current_speed = object_speed * (0.5 if slowdown_timer > 0 else 1)

    # Update object positions
    for apple in apples[:]:
        apple[1] += int(current_speed)
        if apple[1] > screen_height:
            apples.remove(apple)
        if abs(apple[0] - newton_x) < 50 and abs(apple[1] - newton_y) < 50:
            score += 1
            apples.remove(apple)

    for anomaly in gravity_anomalies[:]:
        anomaly[1] += int(current_speed * 1.3)
        if anomaly[1] > screen_height:
            gravity_anomalies.remove(anomaly)
        if abs(anomaly[0] - newton_x) < 50 and abs(anomaly[1] - newton_y) < 50:
            if invincible_timer == 0:
                lives -= 1
            gravity_anomalies.remove(anomaly)

    for megravity in megravities[:]:
        megravity[1] += int(current_speed * 1.5)
        if megravity[1] > screen_height:
            megravities.remove(megravity)
        if abs(megravity[0] - newton_x) < 50 and abs(megravity[1] - newton_y) < 50:
            if invincible_timer == 0:
                lives -= 2
            megravities.remove(megravity)


    for slowdown in slowdowns[:]:
        slowdown[1] += int(current_speed)
        if slowdown[1] > screen_height:
            slowdowns.remove(slowdown)
        if abs(slowdown[0] - newton_x) < 50 and abs(slowdown[1] - newton_y) < 50:
            slowdown_timer = 300
            slowdowns.remove(slowdown)

    for invincible in invincibles[:]:
        invincible[1] += int(current_speed)
        if invincible[1] > screen_height:
            invincibles.remove(invincible)
        if abs(invincible[0] - newton_x) < 50 and abs(invincible[1] - newton_y) < 50:
            invincible_timer = 450
            invincibles.remove(invincible)


    for life in extra_lives[:]:
        life[1] += int(current_speed)
        if life[1] > screen_height:
            extra_lives.remove(life)
        if abs(life[0] - newton_x) < 50 and abs(life[1] - newton_y) < 50:
            if lives < 5:
                lives += 1
                life_flash_timer = 30  # lasts for ~0.5 seconds at 60 FPS
            extra_lives.remove(life)

    for bulb in lightbulbs[:]:
        bulb[1] += int(current_speed)
        if bulb[1] > screen_height:
            lightbulbs.remove(bulb)
        if abs(bulb[0] - newton_x) < 50 and abs(bulb[1] - newton_y) < 50:
            show_fact = True
            fact_text = random.choice(physics_facts)
            lightbulbs.remove(bulb)
            score += 25
            fact_screen_active = True
            countdown = 0


    # Draw everything
    screen.blit(background_img, (0, 0))
    screen.blit(newton_img, (newton_x, newton_y))
    for apple in apples:
        screen.blit(apple_img, (apple[0], apple[1]))
    for anomaly in gravity_anomalies:
        screen.blit(gravity_anomaly_img, (anomaly[0], anomaly[1]))
    for megravity in megravities:
        screen.blit(Megravity_img, (megravity[0], megravity[1]))
    for slowdown in slowdowns:
        screen.blit(slowdown_img, (slowdown[0], slowdown[1]))
    for invincible in invincibles:
        screen.blit(invincible_img, (invincible[0], invincible[1]))
    for life in extra_lives:
        screen.blit(life_img, (life[0], life[1]))

    for bulb in lightbulbs:
        screen.blit(lightbulb_img, (bulb[0], bulb[1]))

    if show_fact:
        screen.fill((0, 0, 20))

        # Draw centered title
        fact_title = font.render("Fun Physics Fact!", True, (255, 255, 0))
        title_rect = fact_title.get_rect(center=(screen_width // 2, 100))
        screen.blit(fact_title, title_rect)

        # Draw centered fact
        wrapped_fact = font.render(fact_text, True, (200, 200, 255))
        fact_rect = wrapped_fact.get_rect(center=(screen_width // 2, 200))
        screen.blit(wrapped_fact, fact_rect)

        # Draw "Return" button
        return_text = font.render("Return", True, (0, 0, 0))
        return_button = pygame.Rect(screen_width // 2 - 60, 300, 120, 50)
        pygame.draw.rect(screen, (0, 255, 0), return_button)
        screen.blit(return_text, (return_button.x + 20, return_button.y + 10))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if return_button.collidepoint(event.pos):
                        waiting = False
                        show_fact = False
                        countdown = 3


    if countdown > 0:
        screen.fill((0, 0, 0))
        draw_text(f"{countdown}", screen_width//2, screen_height//2, color=(255, 255, 0))
        pygame.display.flip()
        pygame.time.delay(1000)
        countdown -= 1
        if countdown == 0:
            fact_screen_active = False


    draw_text(f'Score: {score}', 10, 10)
    draw_text(f'High Score: {high_score}', 10, 40)
    draw_text(f'Lives: {lives}', 10, 70)
    if life_flash_timer > 0:
        draw_text("+1", 130, 70, color=(0, 255, 0))
        life_flash_timer -= 1

    if slowdown_timer > 0:
        draw_text(f'Slow: {slowdown_timer // 60}s', 10, 100)
    if invincible_timer > 0:
        draw_text(f'Invincible: {invincible_timer // 60}s', 10, 130)

    if lives <= 0:
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        game_over_screen()
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    restart_game()
                    game_over = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and fact_screen_active:
                    show_fact = False
                    countdown = 3


    pygame.display.flip()
    clock.tick(60)
