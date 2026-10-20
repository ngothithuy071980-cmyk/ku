
import pygame
import random
import sys

pygame.init()

# Cấu hình cửa sổ game
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash - Python")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28, bold=True)
big_font = pygame.font.SysFont("Arial", 48, bold=True)

# Màu sắc
BLACK = (15, 18, 35)
WHITE = (255, 255, 255)
CYAN = (0, 240, 255)
PINK = (255, 50, 130)
PURPLE = (130, 70, 255)
YELLOW = (255, 230, 60)

# Mặt đất
GROUND_Y = 420

# Nhân vật
PLAYER_SIZE = 36
player_x = 130
player_y = GROUND_Y - PLAYER_SIZE
player_vy = 0
GRAVITY = 0.8
JUMP_POWER = -14
on_ground = True

# Game
obstacles = []
particles = []
score = 0
speed = 6
spawn_timer = 0
game_state = "menu"
best_score = 0


def reset_game():
    global player_y, player_vy, on_ground
    global obstacles, particles, score, speed, spawn_timer

    player_y = GROUND_Y - PLAYER_SIZE
    player_vy = 0
    on_ground = True
    obstacles = []
    particles = []
    score = 0
    speed = 6
    spawn_timer = 0


def draw_text(text, font_obj, color, x, y, center=True):
    image = font_obj.render(text, True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def create_obstacle():
    size = random.choice([30, 38, 45])
    obstacles.append({
        "x": WIDTH + 20,
        "size": size
    })


def draw_background():
    screen.fill(BLACK)

    # Lưới nền
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, (30, 38, 65),
                         (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (30, 38, 65),
                         (0, y), (WIDTH, y), 1)

    # Mặt đất phát sáng
    pygame.draw.rect(
        screen, PURPLE,
        (0, GROUND_Y, WIDTH, 5)
    )
    pygame.draw.rect(
        screen, (25, 28, 55),
        (0, GROUND_Y + 5, WIDTH, HEIGHT - GROUND_Y)
    )


def draw_player():
    rect = pygame.Rect(
        int(player_x), int(player_y),
        PLAYER_SIZE, PLAYER_SIZE
    )

    pygame.draw.rect(screen, CYAN, rect, border_radius=5)
    pygame.draw.rect(screen, WHITE, rect, 3, border_radius=5)

    # Mắt nhân vật
    pygame.draw.rect(
        screen, BLACK,
        (player_x + 22, player_y + 8, 6, 6)
    )


def draw_obstacles():
    for obs in obstacles:
        size = obs["size"]
        x = int(obs["x"])

        points = [
            (x, GROUND_Y),
            (x + size // 2, GROUND_Y - size),
            (x + size, GROUND_Y)
        ]

        pygame.draw.polygon(screen, PINK, points)
        pygame.draw.polygon(screen, WHITE, points, 2)


def update_game():
    global player_y, player_vy, on_ground
    global score, speed, spawn_timer, best_score
    global game_state

    # Trọng lực
    player_vy += GRAVITY
    player_y += player_vy

    if player_y >= GROUND_Y - PLAYER_SIZE:
        player_y = GROUND_Y - PLAYER_SIZE
        player_vy = 0
        on_ground = True

    # Tạo chướng ngại vật
    spawn_timer += 1
    if spawn_timer >= random.randint(48, 78):
        create_obstacle()
        spawn_timer = 0

    # Di chuyển chướng ngại vật
    for obs in obstacles:
        obs["x"] -= speed

    obstacles[:] = [
        obs for obs in obstacles
        if obs["x"] + obs["size"] > 0
    ]

    # Kiểm tra va chạm
    player_rect = pygame.Rect(
        int(player_x + 5),
        int(player_y + 5),
        PLAYER_SIZE - 10,
        PLAYER_SIZE - 5
    )

    for obs in obstacles:
        size = obs["size"]

        # Hộp va chạm gần đúng hình tam giác
        obstacle_rect = pygame.Rect(
            int(obs["x"] + 5),
            GROUND_Y - size + 10,
            size - 10,
            size - 10
        )

        if player_rect.colliderect(obstacle_rect):
            game_state = "over"
            best_score = max(best_score, score)
            return

    score += 1
    speed = min(6 + score // 500, 13)


def main():
    global game_state, player_vy, on_ground

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if game_state == "menu":
                        reset_game()
                        game_state = "playing"
                    elif game_state == "playing" and on_ground:
                        player_vy = JUMP_POWER
                        on_ground = False
                    elif game_state == "over":
                        reset_game()
                        game_state = "playing"

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "menu":
                    reset_game()
                    game_state = "playing"
                elif game_state == "playing" and on_ground:
                    player_vy = JUMP_POWER
                    on_ground = False
                elif game_state == "over":
                    reset_game()
                    game_state = "playing"

        draw_background()

        if game_state == "menu":
            draw_text("GEOMETRY DASH", big_font, CYAN,
                      WIDTH // 2, 160)
            draw_text("PYTHON EDITION", font, PINK,
                      WIDTH // 2, 215)
            draw_text("PRESS SPACE TO START", font, WHITE,
                      WIDTH // 2, 300)
            draw_text("SPACE / UP / CLICK TO JUMP",
                      font, YELLOW, WIDTH // 2, 350)

        elif game_state == "playing":
            update_game()
            draw_player()
            draw_obstacles()

            draw_text(f"SCORE: {score // 10}", font,
                      WHITE, 20, 20, center=False)
            draw_text(f"SPEED: {speed}", font,
                      CYAN, 20, 55, center=False)

        elif game_state == "over":
            draw_player()
            draw_obstacles()

            draw_text("GAME OVER", big_font, PINK,
                      WIDTH // 2, 175)
            draw_text(f"SCORE: {score // 10}", font,
                      WHITE, WIDTH // 2, 240)
            draw_text(f"BEST: {best_score // 10}", font,
                      YELLOW, WIDTH // 2, 280)
            draw_text("PRESS SPACE TO RESTART", font,
                      CYAN, WIDTH // 2, 340)

        pygame.display.flip()


if _name_ == "_main_":
    main()
