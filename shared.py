import pygame

# Shared constants
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

# Shared function or any other shared code
def init_window():
    return pygame.display.set_mode((WIDTH, HEIGHT))