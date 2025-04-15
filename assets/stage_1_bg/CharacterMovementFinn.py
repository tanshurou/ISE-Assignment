import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

# Load your spritesheet image
sprite_sheet_image = pygame.image.load("Finn_Running.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# Colors
BG = (50, 50, 50)
Blue = (0, 162, 232)

# Group all unwanted colors into a list
unwanted_colors = [
    Blue
]

# Animation settings
Finn_animation_list = []
Finn_animation_steps = [10, 10, 8]
action = 0
last_update = pygame.time.get_ticks()
Finn_animation_cooldown = 100  # faster cooldown for smoother animation
frame = 0
step_counter = 0

# Load all frames
for i, animation in enumerate(Finn_animation_steps):
    temp_img_list = []
    for _ in range(animation):
        if i == 1:  # Jump
            img = sprite_sheet.get_image(step_counter, 75.3, 88, 1, unwanted_colors)
        elif i == 2: # Shoot
            img = sprite_sheet.get_image(step_counter, 83.5, 88, 1, unwanted_colors)
        else:
            img = sprite_sheet.get_image(step_counter, 66, 88, 1, unwanted_colors)
        temp_img_list.append(img)
        step_counter += 1
    Finn_animation_list.append(temp_img_list)

run = True
while run:
    # Update background
    screen.fill(BG)

    # Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= Finn_animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(Finn_animation_list[action]):
            frame = 0
            if action != 0:  # If not right-running, return to it
                action = 0

    # Display current frame
    screen.blit(Finn_animation_list[action][frame], (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Jump animation
                action = 1
                frame = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Shoot animation
                action = 2
                frame = 0

    pygame.display.update()

pygame.quit()
