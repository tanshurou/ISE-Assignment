import pygame
from pathlib import Path
import stage1
import test

def main():
    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 736
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Adventure Time → Boss Battle")

    # Run Stage 1
    #stage1.run_stage1(screen)

    # optionally clear or fade out music, reset any globals here…

    # Run Stage 2
    test.run_stage2()

    pygame.quit()

if __name__ == "__main__":
    main()
