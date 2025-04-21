import pygame
from characterMovementAll import CharacterAnimation

from pathlib import Path
import stage1

pygame.init()
font = pygame.font.SysFont("Times New Roman", 24)

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 736
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Time Marathon")

Blue = (0, 162, 232)
unwanted_colors = [Blue]
bullet_path = Path("assets") / "character" / "Bullet_animation.png"

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
scene = stage1.Scenes()

while run:
    scene.emptyBg(3)
    scene.cutscene1()

    if scene.gameplay_started and not is_jumping and scene.finn.action != 0:
        scene.finn.set_action(0)
    scene.finn.move(dx=0)

    if is_jumping:
        finn_y_velocity += gravity
        scene.finn.pos[1] += finn_y_velocity
        if scene.finn.pos[1] >= 250:  # ground level now is 250
            scene.finn.pos[1] = 250
            is_jumping = False
            scene.finn.set_action(1)

    for bullet in bullets[:]:
        bullet.pos[0] += BULLET_SPEED
        bullet.update()

    if bullet_explosion and pygame.time.get_ticks() - explosion_timer > 800:
        special_effect_visible = False
        bullet_explosion = False

    scene.finn.update()
    scene.pb.update()
    scene.ice_king.update()
    scene.special_effect.update()

    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    for bullet in bullets:
        bullet.draw(screen)
    scene.finn.draw(screen)
    scene.pb.draw(screen)
    scene.ice_king.draw(screen)
    if scene.special_effect_visible:
        scene.special_effect.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and scene.gameplay_started:
                scene.finn.set_action(1)  # jump animation
                is_jumping = True
                finn_y_velocity = jump_velocity

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if scene.gameplay_started:
                scene.finn.set_action(2)
                new_bullet = CharacterAnimation(bullet_path, [4], [50], [100], 60, unwanted_colors, [scene.finn.pos[0] + 40, scene.finn.pos[1] + 10], scale=0.5)
                new_bullet.set_action(0)
                bullets.append(new_bullet)

    pygame.display.update()
    clock.tick(60)

pygame.quit()