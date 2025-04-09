import pygame

def resizeObject(oriObj, scaledFactor):
  scaledObj = pygame.transform.scale_by(oriObj, scaledFactor)
  return (scaledObj)