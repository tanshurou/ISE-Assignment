import pygame
from pathlib import Path

def resizeObject(oriObj, scaledFactor):
  scaledObj = pygame.transform.scale_by(oriObj, scaledFactor)
  return (scaledObj)


def getImage(spritesheet, frame, width, height, scale, colour=None):
    # Create a new surface with per-pixel alpha transparency
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(spritesheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image
