import pygame
from os.path import join

WIDTH, HEIGHT = 1000, 800

#create the background
def get_background(name):

    #locate the Background folder
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    #creates a 2d array of tiles
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    
    return tiles, image