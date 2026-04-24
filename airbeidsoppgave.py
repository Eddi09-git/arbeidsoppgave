import pygame
import sys
import os

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario HARD")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# ---------- PIXELFORGE LOGO (TEKST) ----------
logo_font = pygame.font.SysFont("Arial", 20, bold=True)

def draw_logo():
    # bakgrunnsboks
    pygame.draw.rect(screen, (20, 20, 20), (WIDTH - 190, 10, 180, 60), border_radius=8)
    pygame.draw.rect(screen, (255, 140, 0), (WIDTH - 190, 10, 180, 60), 2, border_radius=8)

    # tekst
    text = logo_font.render("PixelForge", True, (255, 140, 0))
    screen.blit(text, (WIDTH - 175, 25))

# ---------- HIGHSCORE ----------
def load_highscore():
    if os.path.exists("highscore.txt"):
        return int(open("highscore.txt").read())
    return 0

def save_highscore(score):
    open("highscore.txt", "w").write(str(score))

highscore = load_highscore()

# ---------- LEVELS ----------
levels = [
    {
        "platforms": [
            pygame.Rect(0, 350, 2000, 50),
            pygame.Rect(250, 300, 80, 15),
            pygame.Rect(400, 250, 80, 15),
        ],
        "coins": [
            pygame.Rect(260, 270, 15, 15),
            pygame.Rect(410, 220, 15, 15),
        ],
        "enemies": [pygame.Rect(500, 320, 30, 30)],
        "goal": pygame.Rect(700, 300, 40, 50)
    },
    {
        "platforms": [
            pygame.Rect(0, 350, 2000, 50),
            pygame.Rect(300, 300, 60, 15),
            pygame.Rect(450, 260, 60, 15),
            pygame.Rect(600, 220, 60, 15),
        ],
        "coins": [
            pygame.Rect(310, 270, 15, 15),
            pygame.Rect(460, 230, 15, 15),
            pygame.Rect(610, 190, 15, 15),
        ],
        "enemies": [
            pygame.Rect(550, 320, 30, 30),
            pygame.Rect(700, 320, 30, 30)
        ],
        "goal": pygame.Rect(900, 300, 40, 50)
    }
]

current_level = 0

def load_level(i):
    global player, vel_y, on_ground, camera_x
    global platforms, coins, enemies, goal

    level = levels[i]

    player = pygame.Rect(50, 300, 30, 30)
    vel_y = 0
    on_ground = False
    camera_x = 0

    platforms = level["platforms"]
    coins = level["coins"][:]
    enemies = [e.copy() for e in level["enemies"]]
    goal = level["goal"]

load_level(current_level)

score = 0
game_over = False

# ---------- GAME LOOP ----------
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                score = 0
                current_level = 0
                load_level(current_level)
                game_over = False

    keys = pygame.key.get_pressed()

    if not game_over:
        dx = 0
        if keys[pygame.K_RIGHT]:
            dx = 6
        if keys[pygame.K_LEFT]:
            dx = -6

        if keys[pygame.K_SPACE] and on_ground:
            vel_y = -11
            on_ground = False

        vel_y += 0.6
        player.y += vel_y
        player.x += dx

        on_ground = False

        for p in platforms:
            if player.colliderect(p):
                if vel_y > 0:
                    player.bottom = p.top
                    vel_y = 0
                    on_ground = True

        if player.y > HEIGHT:
            game_over = True

        for c in coins[:]:
            if player.colliderect(c):
                coins.remove(c)
                score += 1

        for e in enemies:
            e.x += 2
            if e.x < 500 or e.x > 800:
                e.x -= 2

            if player.colliderect(e):
                game_over = True

        if player.colliderect(goal):
            current_level += 1
            if current_level >= len(levels):
                game_over = True
                if score > highscore:
                    save_highscore(score)
                    highscore = score
            else:
                load_level(current_level)

        camera_x = player.x - 200

    # ---------- DRAW ----------
    screen.fill((92,148,252))

    for p in platforms:
        pygame.draw.rect(screen, (0,200,0), (p.x - camera_x, p.y, p.w, p.h))

    for c in coins:
        pygame.draw.rect(screen, (255,215,0), (c.x - camera_x, c.y, c.w, c.h))

    for e in enemies:
        pygame.draw.rect(screen, (255,0,0), (e.x - camera_x, e.y, e.w, e.h))

    pygame.draw.rect(screen, (255,255,255), (goal.x - camera_x, goal.y, goal.w, goal.h))
    pygame.draw.rect(screen, (255,255,0), (player.x - camera_x, player.y, player.w, player.h))

    # UI
    screen.blit(font.render(f"Score: {score}", True, (0,0,0)), (10,10))
    screen.blit(font.render(f"Highscore: {highscore}", True, (0,0,0)), (10,40))
    screen.blit(font.render(f"Level: {current_level+1}", True, (0,0,0)), (10,70))

  
    draw_logo()

    if game_over:
        screen.blit(font.render("GAME OVER - Press R", True, (0,0,0)), (250,200))

    pygame.display.flip()