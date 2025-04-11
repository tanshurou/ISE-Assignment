import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

# Load your spritesheet image
sprite_sheet_image = pygame.image.load("C:\\Users\\user\\Documents\\Degree Level 2\\Degree Semester 2\\Imaging & Special Effects\\MainMenu & Character\\Finn_Running.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# Colors
BG = (50, 50, 50)
Green = (0, 255, 80)
Border = (0, 128, 128)
O1Border = (0, 129, 128)
O2Border = (0, 129, 127)
O3Border = (0, 130, 127)
O1Green = (0, 254, 80)
O2Green = (0, 253, 79)
O3Green = (0, 253, 80)
O4Green = (0, 252, 79)
O5Green = (0, 254, 81)
O6Green = (0, 253, 81)
O7Green = (0, 250, 79)
O8Green = (0, 251, 79)
White = (255, 255, 255)
Blue = (0, 162, 232)

# Group all unwanted colors into a list
unwanted_colors = [
    Green, Border, O1Border, O2Border, O3Border,
    O1Green, O2Green, O3Green, O4Green,
    O5Green, O6Green, O7Green, O8Green, Blue
]

# Animation settings
Finn_animation_list = []
Finn_animation_steps = [10, 10, 10, 10]
action = 1
last_update = pygame.time.get_ticks()
Finn_animation_cooldown = 100  # faster cooldown for smoother animation
frame = 0
step_counter = 0

# Load all frames
for i, animation in enumerate(Finn_animation_steps):
    temp_img_list = []
    for _ in range(animation):
        if i == 2:  # Down
            img = sprite_sheet.get_image(step_counter, 66.48, 92, 1, unwanted_colors)
        elif i == 3:  # Up
            img = sprite_sheet.get_image(step_counter, 64.55, 92, 1, unwanted_colors)
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

    # Display current frame
    screen.blit(Finn_animation_list[action][frame], (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Up animation
                action = 3
                frame = 0
            elif event.key == pygame.K_s:  # Down animation
                action = 2
                frame = 0
            elif event.key == pygame.K_a:  # Left animation
                action = 1 
                frame = 0
            elif event.key == pygame.K_d:  # Right animation
                action = 0
                frame = 0


    pygame.display.update()

pygame.quit()
