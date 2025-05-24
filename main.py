import pygame
from pathlib import Path
from stage1 import startStage1
from stage2 import run_stage2

def main():
    pygame.init()
    pygame.mixer.init()
    
    # Start Game in Stage 1
    startStage1()
    # After that transition to Stage 2
    run_stage2()

    pygame.quit()

if __name__ == "__main__":
    main()
