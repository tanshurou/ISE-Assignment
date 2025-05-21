import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colours,):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        # Remove multiple background colors
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                current_color = image.get_at((x, y))[:3]
                if current_color in colours:
                    image.set_at((x, y), (0, 0, 0, 0))

        return image