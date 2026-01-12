import pygame
import random
import sys

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 420, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ִֶָ𓂃 ࣪ ִֶָ🦢་༘࿐ Flappy Bird clone ִֶָ𓂃 ࣪ ִֶָ🦢་༘࿐")
clock = pygame.time.Clock()

#Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 28)

#Game constants
GRAVITY = 0.5
JUMP_VELOCITY = -7
PIPE_SPEED = 3
PIPE_WIDTH = 80
PIPE_GAP = 170
PIPE_SPACING = 220  # <<< distance between pipes

# bird(ball here)
BIRD_X = 110
BIRD_RADIUS = 18


def reset_game():
    bird_y = HEIGHT // 2
    bird_vy = 0.0
    pipes = []
    score = 0
    game_over = False
    started = False
    return bird_y, bird_vy, pipes, score, game_over, started


bird_y, bird_vy, pipes, score, game_over, started = reset_game()


def spawn_pipe():
    margin = PIPE_GAP // 2 + 20
    gap_y = random.randint(margin, HEIGHT - margin)
    return {"x": WIDTH + 30, "gap_y": gap_y, "scored": False}


def bird_rect(y):
    return pygame.Rect(
        BIRD_X - BIRD_RADIUS,
        int(y) - BIRD_RADIUS,
        BIRD_RADIUS * 2,
        BIRD_RADIUS * 2
    )


def pipe_rects(pipe):
    x = int(pipe["x"])
    gap_y = pipe["gap_y"]

    top_height = gap_y - PIPE_GAP // 2
    bottom_y = gap_y + PIPE_GAP // 2

    top_rect = pygame.Rect(x, 0, PIPE_WIDTH, top_height)
    bottom_rect = pygame.Rect(x, bottom_y, PIPE_WIDTH, HEIGHT - bottom_y)

    return top_rect, bottom_rect


def draw_center_text(text, y, small=False):
    f = small_font if small else font
    surf = f.render(text, True, (255, 255, 255))
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)


#GAME LOOP
while True:
    clock.tick(60)

    #EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not started:
                    started = True
                    pipes.append(spawn_pipe())
                elif not game_over:
                    bird_vy = JUMP_VELOCITY
                else:
                    bird_y, bird_vy, pipes, score, game_over, started = reset_game()

            if event.key == pygame.K_r:
                bird_y, bird_vy, pipes, score, game_over, started = reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not started:
                started = True
                pipes.append(spawn_pipe())
            elif not game_over:
                bird_vy = JUMP_VELOCITY
            else:
                bird_y, bird_vy, pipes, score, game_over, started = reset_game()

    
    if started and not game_over:
        # Bird physics
        bird_vy += GRAVITY
        bird_y += bird_vy

        # Move pipes
        for pipe in pipes:
            pipe["x"] -= PIPE_SPEED

        # Spawn new pipe (distance-based)
        if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - PIPE_SPACING:
            pipes.append(spawn_pipe())

        # Remove off-screen pipes
        pipes = [p for p in pipes if p["x"] + PIPE_WIDTH > -10]

        # Score
        for pipe in pipes:
            if not pipe["scored"] and pipe["x"] + PIPE_WIDTH < BIRD_X - BIRD_RADIUS:
                pipe["scored"] = True
                score += 1

        # Collisions
        brect = bird_rect(bird_y)

        # Ground / ceiling
        if bird_y + BIRD_RADIUS >= HEIGHT or bird_y - BIRD_RADIUS <= 0:
            game_over = True

        # Pipe collision
        for pipe in pipes:
            top_rect, bottom_rect = pipe_rects(pipe)
            if brect.colliderect(top_rect) or brect.colliderect(bottom_rect):
                game_over = True
                break

    #DRAW
    screen.fill((25, 35, 50))

    # Pipes
    for pipe in pipes:
        top_rect, bottom_rect = pipe_rects(pipe)
        pygame.draw.rect(screen, (90, 200, 120), top_rect)
        pygame.draw.rect(screen, (90, 200, 120), bottom_rect)

    # Bird
    pygame.draw.circle(screen, (250, 220, 90), (BIRD_X, int(bird_y)), BIRD_RADIUS)

    # Score
    score_surf = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 20))

    # Overlays
    if not started:
        draw_center_text("Click / SPACE", HEIGHT // 2 - 20)
        draw_center_text("to start & jump", HEIGHT // 2 + 25, small=True)

    if game_over:
        draw_center_text("GAME OVER", HEIGHT // 2 - 30)
        draw_center_text("SPACE to restart", HEIGHT // 2 + 20, small=True)
        draw_center_text("R to reset", HEIGHT // 2 + 50, small=True)

    pygame.display.flip()
