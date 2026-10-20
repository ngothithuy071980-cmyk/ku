import pygame
import random
import math
import sys

pygame.init()

# ==============================
# CAU HINH GAME
# ==============================
WIDTH, HEIGHT = 900, 500
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash - Python Edition")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 25, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 18, bold=True)
TITLE_FONT = pygame.font.SysFont("arial", 48, bold=True)

# Mau sac
BG = (12, 15, 35)
GRID = (29, 37, 68)
WHITE = (245, 250, 255)
CYAN = (0, 240, 255)
PINK = (255, 55, 125)
PURPLE = (140, 75, 255)
YELLOW = (255, 225, 65)
GREEN = (70, 255, 160)

GROUND_Y = 420
PLAYER_X = 130
PLAYER_SIZE = 36

GRAVITY = 2200
JUMP_VELOCITY = -730

# Trang thai game
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

game_state = MENU

# Nhan vat
player_y = float(GROUND_Y - PLAYER_SIZE)
player_vy = 0.0
on_ground = True
player_angle = 0.0

# Chinh game
obstacles = []
particles = []
score = 0
best_score = 0
speed = 330.0
spawn_timer = 0.0
next_spawn = 1.15
game_time = 0.0

# Nen chuyen dong
background_offset = 0.0


# ==============================
# HAM VE CHU
# ==============================
def draw_text(text, font, color, x, y, center=True):
    image = font.render(str(text), True, color)
    rect = image.get_rect()

    if center:
        rect.center = (int(x), int(y))
    else:
        rect.topleft = (int(x), int(y))

    screen.blit(image, rect)


# ==============================
# VE NEN
# ==============================
def draw_background(dt):
    global background_offset

    screen.fill(BG)
    background_offset = (background_offset + speed * dt * 0.35) % 40

    # Luoi nen
    offset = int(background_offset)

    for x in range(-40, WIDTH + 40, 40):
        xx = x - offset
        pygame.draw.line(
            screen, GRID, (xx, 0), (xx, HEIGHT), 1
        )

    for y in range(0, HEIGHT, 40):
        pygame.draw.line(
            screen, GRID, (0, y), (WIDTH, y), 1
        )

    # Mat dat
    pygame.draw.rect(
        screen, (25, 29, 57),
        (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y)
    )

    pygame.draw.line(
        screen, PURPLE,
        (0, GROUND_Y), (WIDTH, GROUND_Y), 4
    )

    # Duong neon ben duoi
    pygame.draw.line(
        screen, (50, 55, 100),
        (0, GROUND_Y + 7), (WIDTH, GROUND_Y + 7), 2
    )


# ==============================
# NHAN VAT
# ==============================
def draw_player():
    center = (
        int(PLAYER_X + PLAYER_SIZE / 2),
        int(player_y + PLAYER_SIZE / 2)
    )

    # Tao hinh vuong de xoay
    cube = pygame.Surface(
        (PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA
    )

    pygame.draw.rect(
        cube, CYAN,
        (2, 2, PLAYER_SIZE - 4, PLAYER_SIZE - 4),
        border_radius=4
    )

    pygame.draw.rect(
        cube, WHITE,
        (2, 2, PLAYER_SIZE - 4, PLAYER_SIZE - 4),
        width=3, border_radius=4
    )

    # Mat nhan vat
    pygame.draw.rect(cube, BG, (21, 9, 7, 7))
    pygame.draw.rect(cube, BG, (9, 21, 7, 5))

    rotated = pygame.transform.rotate(cube, player_angle)
    rect = rotated.get_rect(center=center)

    # Lop sang nhe
    glow = pygame.Surface(
        (PLAYER_SIZE + 12, PLAYER_SIZE + 12),
        pygame.SRCALPHA
    )
    pygame.draw.rect(
        glow, (0, 220, 255, 35),
        (0, 0, PLAYER_SIZE + 12, PLAYER_SIZE + 12),
        border_radius=8
    )
    screen.blit(glow, glow.get_rect(center=center))

    screen.blit(rotated, rect)


# ==============================
# CHUONG NGAI VAT
# ==============================
def create_obstacle():
    size = random.choice([32, 38, 42])
    obstacles.append({
        "x": float(WIDTH + 20),
        "size": size
    })


def draw_obstacles():
    for obstacle in obstacles:
        x = int(obstacle["x"])
        size = obstacle["size"]

        points = [
            (x, GROUND_Y),
            (x + size // 2, GROUND_Y - size),
            (x + size, GROUND_Y)
        ]

        # Vien sang
        pygame.draw.polygon(
            screen, (100, 25, 75),
            [
                (x - 3, GROUND_Y),
                (x + size // 2, GROUND_Y - size - 3),
                (x + size + 3, GROUND_Y)
            ]
        )

        pygame.draw.polygon(screen, PINK, points)
        pygame.draw.polygon(screen, WHITE, points, 2)


def get_obstacle_rect(obstacle):
    # Hop va cham nho hon hinh gai de cong bang hon
    size = obstacle["size"]

    return pygame.Rect(
        int(obstacle["x"] + size * 0.22),
        GROUND_Y - int(size * 0.78),
        int(size * 0.56),
        int(size * 0.78)
    )


# ==============================
# HIEU UNG HAT
# ==============================
def add_particles(x, y, color, amount=10):
    for _ in range(amount):
        angle = random.uniform(0, math.tau)
        velocity = random.uniform(50, 220)

        particles.append({
            "x": float(x),
            "y": float(y),
            "vx": math.cos(angle) * velocity,
            "vy": math.sin(angle) * velocity,
            "life": random.uniform(0.2, 0.55),
            "color": color,
            "size": random.randint(2, 5)
        })


def update_particles(dt):
    for particle in particles[:]:
        particle["x"] += particle["vx"] * dt
        particle["y"] += particle["vy"] * dt
        particle["vy"] += 350 * dt
        particle["life"] -= dt

        if particle["life"] <= 0:
            particles.remove(particle)


def draw_particles():
    for particle in particles:
        if particle["life"] <= 0:
            continue

        radius = max(1, int(particle["size"] * min(
            1.0, particle["life"] * 3
        )))

        pygame.draw.circle(
            screen, particle["color"],
            (int(particle["x"]), int(particle["y"])),
            radius
        )


# ==============================
# KHOI TAO LAI GAME
# ==============================
def reset_game():
    global player_y, player_vy, on_ground, player_angle
    global obstacles, particles, score, speed
    global spawn_timer, next_spawn, game_time

    player_y = float(GROUND_Y - PLAYER_SIZE)
    player_vy = 0.0
    on_ground = True
    player_angle = 0.0

    obstacles.clear()
    particles.clear()

    score = 0
    speed = 330.0
    spawn_timer = 0.0
    next_spawn = 1.0
    game_time = 0.0


def jump():
    global player_vy, on_ground

    if on_ground and game_state == PLAYING:
        player_vy = JUMP_VELOCITY
        on_ground = False

        add_particles(
            PLAYER_X + PLAYER_SIZE // 2,
            GROUND_Y - 2,
            CYAN, 5
        )


# ==============================
# CAP NHAT GAME
# ==============================
def update_game(dt):
    global player_y, player_vy, on_ground, player_angle
    global score, speed, spawn_timer, next_spawn
    global game_state, best_score, game_time

    game_time += dt

    # Tang toc do tu tu
    speed = min(330 + game_time * 9, 620)

    # Vat ly nhay
    old_y = player_y

    player_vy += GRAVITY * dt
    player_y += player_vy * dt

    # Dap dat chinh xac
    if player_y >= GROUND_Y - PLAYER_SIZE:
        player_y = float(GROUND_Y - PLAYER_SIZE)

        if not on_ground:
            add_particles(
                PLAYER_X + PLAYER_SIZE // 2,
                GROUND_Y - 2,
                PURPLE, 5
            )

        player_vy = 0.0
        on_ground = True

    # Xoay nhan vat khi bay
    if not on_ground:
        player_angle = (player_angle - 360 * dt) % 360
    else:
        player_angle = round(player_angle / 90) * 90

    # Sinh gai theo khoang thoi gian co dinh
    spawn_timer += dt

    if spawn_timer >= next_spawn:
        create_obstacle()
        spawn_timer = 0.0
        next_spawn = random.uniform(0.95, 1.35)

    # Di chuyen gai
    for obstacle in obstacles:
        obstacle["x"] -= speed * dt

    obstacles[:] = [
        obstacle for obstacle in obstacles
        if obstacle["x"] + obstacle["size"] > 0
    ]

    # Cap nhat diem
    score += dt * 10

    # Hop va cham cua nhan vat
    player_rect = pygame.Rect(
        PLAYER_X + 5,
        int(player_y + 5),
        PLAYER_SIZE - 10,
        PLAYER_SIZE - 10
    )

    # Kiem tra va cham
    for obstacle in obstacles:
        if player_rect.colliderect(get_obstacle_rect(obstacle)):
            game_state = GAME_OVER
            best_score = max(best_score, int(score))
            add_particles(
                PLAYER_X + PLAYER_SIZE // 2,
                int(player_y + PLAYER_SIZE // 2),
                PINK, 30
            )
            return


# ==============================
# GIAO DIEN
# ==============================
def draw_hud():
    draw_text(
        f"SCORE: {int(score)}",
        FONT, WHITE, 20, 18, center=False
    )

    draw_text(
        f"BEST: {best_score}",
        SMALL_FONT, YELLOW, 20, 54, center=False
    )

    draw_text(
        f"SPEED: {int(speed)}",
        SMALL_FONT, CYAN, WIDTH - 135, 24, center=False
    )


def draw_menu():
    draw_text(
        "GEOMETRY DASH",
        TITLE_FONT, CYAN, WIDTH // 2, 155
    )

    draw_text(
        "PYTHON EDITION",
        FONT, PINK, WIDTH // 2, 215
    )

    # Nut Start
    button = pygame.Rect(WIDTH // 2 - 120, 270, 240, 58)

    pygame.draw.rect(
        screen, PURPLE, button, border_radius=12
    )
    pygame.draw.rect(
        screen, WHITE, button, 2, border_radius=12
    )

    draw_text(
        "START GAME", FONT, WHITE,
        WIDTH // 2, 299
    )

    draw_text(
        "SPACE / UP / CLICK: JUMP",
        SMALL_FONT, YELLOW, WIDTH // 2, 365
    )


def draw_game_over():
    # Lop toi nen
    overlay = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA
    )
    overlay.fill((5, 5, 20, 180))
    screen.blit(overlay, (0, 0))

    draw_text(
        "GAME OVER", TITLE_FONT, PINK,
        WIDTH // 2, 170
    )

    draw_text(
        f"SCORE: {int(score)}",
        FONT, WHITE, WIDTH // 2, 235
    )

    draw_text(
        f"BEST: {best_score}",
        FONT, YELLOW, WIDTH // 2, 275
    )

    draw_text(
        "PRESS SPACE OR CLICK TO RETRY",
        SMALL_FONT, CYAN, WIDTH // 2, 340
    )


# ==============================
# VONG LAP CHINH
# ==============================
def main():
    global game_state

    running = True

    while running:
        # Gioi han delta time de tranh loi vat ly
        dt = min(clock.tick(FPS) / 1000.0, 0.033)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key in (
                    pygame.K_SPACE, pygame.K_UP, pygame.K_w
                ):
                    if game_state == MENU:
                        reset_game()
                        game_state = PLAYING

                    elif game_state == PLAYING:
                        jump()

                    elif game_state == GAME_OVER:
                        reset_game()
                        game_state = PLAYING

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game_state == MENU:
                        reset_game()
                        game_state = PLAYING

                    elif game_state == PLAYING:
                        jump()

                    elif game_state == GAME_OVER:
                        reset_game()
                        game_state = PLAYING

        # Ve va cap nhat
        draw_background(dt)

        if game_state == MENU:
            draw_menu()

            # Nhan vat mau de trang tri
            draw_player()

        elif game_state == PLAYING:
            update_game(dt)

            draw_obstacles()
            update_particles(dt)
            draw_particles()
            draw_player()
            draw_hud()

        elif game_state == GAME_OVER:
            update_particles(dt)
            draw_obstacles()
            draw_particles()
            draw_player()
            draw_hud()
            draw_game_over()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if _name_ == "_main_":
    main()
