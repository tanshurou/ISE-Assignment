import pygame
from pathlib import Path
from stage1 import startStage1
from stage2 import run_stage2

def main():
    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 736  
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Adventure Time → Boss Battle")

    # Start Game 
    startStage1()

    # Run Stage 2
    run_stage2()

    pygame.quit()

if __name__ == "__main__":
    main()
