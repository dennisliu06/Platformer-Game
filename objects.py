import pygame
from os.path import join
from game_logic import load_sprite_sheets

#gets the block used
def get_block(size, x, y):
    path = join("assets", "Terrain", "Terrain.png")

    #turns image into transparent
    image = pygame.image.load(path).convert_alpha()

    #creates a surface with size of the block
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)

    #creates the rectangle representing the block and location of it on the sprite sheet
    rect = pygame.Rect(x, y, size, size)

    #copies the image with rect onto surface
    surface.blit(image, (0, 0), rect)

    #scales and returns the block
    return pygame.transform.scale2x(surface)


#Creating a super class for all objects extending from Sprite superclass in pygame
class Object(pygame.sprite.Sprite):

    #creates rect of the object and surface for the image
    def __init__ (self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    #draw the block onto the window
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

#creates a subclass of 'Object', size will just be one value because it is a square
class Block(Object):
    
    def __init__ (self, x, y, size, imageX, imageY):
        super().__init__(x, y, size, size)
        block = get_block(size, imageX, imageY)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Slab(Object):
    def __init__ (self, x, y, width, height, imageX, imageY):
        super().__init__(x, y, width, height)
        

#creates a subclass of 'Object' for Fire
class Fire(Object):
    #delay between each animation
    ANIMATION_DELAY = 3

    #inherits parent class variables
    def __init__ (self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")

        #loads sprite sheets of all fire sprites
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)

        #sets image to off
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)

        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    #animates the fire
    def loop(self):
        #find type of fire, goes through all indexes
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // 
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0    

#creates subclass of 'Object' for Spikes
class Spikes(Object):

    #inherits parent class variables
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spikes")
        self.spikes = load_sprite_sheets("Traps", "Spikes", width, height)

        self.image = self.spikes["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
    