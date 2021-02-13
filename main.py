import pygame
import pygame.freetype
from game import *

def main():
    pygame.display.init()
    pygame.freetype.init()
    screen = pygame.display.set_mode((480, 270), pygame.RESIZABLE)
    pygame.display.set_caption("Tic-Tac-Toe Game")

    return screen


if __name__ == "__main__":
    screen = main()
    game(screen)
    pygame.quit()