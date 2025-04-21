import pygame
import spritesheet

class CharacterAnimation:
    def __init__(self, image_path, animation_steps, frame_heights, frame_widths, cooldown, unwanted_colors, pos, scale):
        sprite_sheet_image = pygame.image.load(image_path).convert_alpha()
        self.sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        self.animation_list = []
        self.frame_heights = frame_heights
        self.frame_widths = frame_widths
        self.scale = scale
        self.cooldown = cooldown
        self.unwanted_colors = unwanted_colors
        self.pos = list(pos)  # x, y
        self.frame = 0
        self.action = 0
        self.last_update = pygame.time.get_ticks()
        self.visible = True

        self.load_frames(animation_steps)

    def load_frames(self, animation_steps):
        step_counter = 0
        for i, steps in enumerate(animation_steps):
            temp_list = []
            for _ in range(steps):
                img = self.sprite_sheet.get_image(
                    step_counter,
                    self.frame_heights[i],
                    self.frame_widths[i],
                    1,
                    self.unwanted_colors
                )
                if self.scale != 1:
                    width = int(img.get_width() * self.scale)
                    height = int(img.get_height() * self.scale)
                    img = pygame.transform.scale(img, (width, height))
                temp_list.append(img)
                step_counter += 1
            self.animation_list.append(temp_list)

    def update(self):
        if not self.visible:
            return
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.cooldown:
            self.frame += 1
            self.last_update = now
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0
                if self.action != 0:
                    self.action = 0  # Return to idle/walk

    def draw(self, screen):
        if self.visible:
            screen.blit(self.animation_list[self.action][self.frame], self.pos)

    def set_action(self, action_index):
        if action_index < len(self.animation_list):
            self.action = action_index
            self.frame = 0

    def move(self, dx=0, dy=0):
        self.pos[0] += dx
        self.pos[1] += dy