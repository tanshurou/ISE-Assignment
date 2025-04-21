import pygame
from characterMovementAll import CharacterAnimator

from pathlib import Path

pygame.init()
font = pygame.font.SysFont("Times New Roman", 24)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Time Marathon")

background_path = Path("assets") / "stage_1_bg" / "stage_1_bg.png"

background = pygame.image.load(background_path)

Blue = (0, 162, 232)
unwanted_colors = [Blue]

finn_path = Path("assets") / "character" / "Finn_Running.png"
pb_path = Path("assets") / "character" / "Princess_Bubblegum.png"
ice_king_path = Path("assets") / "character" / "Ice_King.png"
special_effect_path = Path("assets") / "character" / "Special_effect.png"
bullet_path = Path("assets") / "character" / "Bullet_animation.png"

finn = CharacterAnimator(finn_path, [10, 10, 8], [66, 75.3, 83.5], [88, 88, 88, 88], 60, unwanted_colors, [50, 280], scale=0.8)
pb = CharacterAnimator(pb_path, [8, 8, 5], [52, 52, 63.8], [120, 120, 120], 60, unwanted_colors, [200, 280], scale=0.6)
ice_king = CharacterAnimator(ice_king_path, [6, 7, 5], [106, 143, 131.25], [150, 150, 150], 60, unwanted_colors, [1000, 250], scale=0.7)
special_effect = CharacterAnimator(special_effect_path, [4, 5], [50, 100], [100, 100], 60, unwanted_colors, [100,250], scale=1)

cutscene_state = 0
cutscene_start_time = pygame.time.get_ticks()
special_effect_visible = False
gameplay_started = False
bg_x = 0
bg_scroll_speed = 0

is_jumping = False
jump_velocity = -12
gravity = 0.5
finn_y_velocity = 0

bullets = []
BULLET_SPEED = 6
bullet_explosion = False
explosion_timer = 0

clock = pygame.time.Clock()
run = True

while run:
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + background.get_width(), 0))
    now = pygame.time.get_ticks()

    if cutscene_state == 0:
        if finn.action != 0:
            finn.set_action(0)
        finn.move(dx=1)

        if pb.action != 0:
            pb.set_action(0)
        pb.move(dx=1)
        bg_scroll_speed = 1

        if finn.pos[0] >= 300:
            cutscene_state = 1
            cutscene_start_time = now

    elif cutscene_state == 1:
        if pb.action != 1:
            pb.set_action(1)
        if now - cutscene_start_time > 5000:
            cutscene_state = 2
            cutscene_start_time = now
            ice_king.pos = [-100, -150]

    elif cutscene_state == 2:
        if ice_king.action != 0:
            ice_king.set_action(0)
        ice_king.move(dx=4, dy=2)
        if ice_king.pos[0] >= pb.pos[0] - 50:
            cutscene_state = 3
            cutscene_start_time = now

    elif cutscene_state == 3:
        if ice_king.action != 1:
            ice_king.set_action(1)
        if pb.action != 2:
            pb.set_action(2)
        if not special_effect_visible:
            special_effect.set_action(0)
            special_effect_visible = True
            special_effect.pos = [pb.pos[0], pb.pos[1] - 10]
        if now - cutscene_start_time > 1000:
            pb.visible = False
            special_effect_visible = False
            cutscene_state = 4
            cutscene_start_time = now

    elif cutscene_state == 4:
        if ice_king.action != 2:
            ice_king.set_action(2)
        ice_king.move(dx=5, dy=-1)
        if ice_king.pos[0] > SCREEN_WIDTH:
            cutscene_state = 5
            cutscene_start_time = now

    elif cutscene_state == 5:
        if finn.action != 2:
            finn.set_action(2)
        if now - cutscene_start_time > 2000:
            cutscene_state = 6
            cutscene_start_time = now

    elif cutscene_state == 6:
        bg_scroll_speed = 2
        gameplay_started = True
        cutscene_state = 7

    bg_x -= bg_scroll_speed
    if bg_x <= -background.get_width():
        bg_x = 0

    if gameplay_started and not is_jumping and finn.action != 0:
        finn.set_action(0)
    finn.move(dx=0)

    if is_jumping:
        finn_y_velocity += gravity
        finn.pos[1] += finn_y_velocity
        if finn.pos[1] >= 250:  # ground level now is 250
            finn.pos[1] = 250
            is_jumping = False
            finn.set_action(1)

    for bullet in bullets[:]:
        bullet.pos[0] += BULLET_SPEED
        bullet.update()

        if ice_king.visible and bullet.pos[0] > ice_king.pos[0] and bullet.pos[0] < ice_king.pos[0] + 50:
            bullet_explosion = True
            explosion_timer = pygame.time.get_ticks()
            special_effect.pos = [ice_king.pos[0], ice_king.pos[1]]
            special_effect.set_action(1)
            special_effect_visible = True
            ice_king.visible = False
            bullets.remove(bullet)
        elif bullet.pos[0] > SCREEN_WIDTH:
            bullets.remove(bullet)

    if bullet_explosion and pygame.time.get_ticks() - explosion_timer > 800:
        special_effect_visible = False
        bullet_explosion = False

    finn.update()
    pb.update()
    ice_king.update()
    special_effect.update()

    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    for bullet in bullets:
        bullet.draw(screen)
    finn.draw(screen)
    pb.draw(screen)
    ice_king.draw(screen)
    if special_effect_visible:
        special_effect.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and gameplay_started:
                finn.set_action(1)  # jump animation
                is_jumping = True
                finn_y_velocity = jump_velocity

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gameplay_started:
                finn.set_action(2)
                new_bullet = CharacterAnimator(bullet_path, [4], [50], [100], 60, unwanted_colors, [finn.pos[0] + 40, finn.pos[1] + 10], scale=0.5)
                new_bullet.set_action(0)
                bullets.append(new_bullet)

    pygame.display.update()
    clock.tick(60)

pygame.quit()