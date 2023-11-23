import pygame
import os
import math
import random
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer!")

#sets the width and height for the box of the screen
WIDTH, HEIGHT = 1000, 800
#set FPS so it runs smoothly on every device
FPS = 60
#velocity when player moves left or right
PLAYER_VEL = 5

#creates the window
window = pygame.display.set_mode((WIDTH, HEIGHT))

#flip the sprites so it faces left 
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

#passes the location of the file, the width and height of the spritesheets, and if it has a direction
def load_sprite_sheets(dir1, dir2, width, height, direction=False, dir3=None):
    #creates the path to the location of the file, if there is a dir3 it will add it
    if dir3:
        path = join('assets', dir1, dir2, dir3)
    else:
        path = join('assets', dir1, dir2)

    #adds files into 'images' after checking if it is a normal file
    images = [f for f in listdir(path) if isfile(join(path, f))]

    #dictionary to represent name with a sprite
    all_sprites = {}

    #load each sprite sheet
    for image in images:
        #loads the image, and converts it into transparent background
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        #creates an array of sprites within the image
        sprites = []

        #counts the number of sprites there is given the width of the sprite
        for i in range(sprite_sheet.get_width() // width):
            #creates a surface for a sprite
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)

            #creates a rect object which represent the area to be copied
            rect = pygame.Rect(i * width, 0, width, height)

            #blits the portion of the sprite sheet onto the surface
            surface.blit(sprite_sheet, (0, 0), rect)

            #scaled it 2x and also added to sprites array
            sprites.append(pygame.transform.scale2x(surface))
        
        #if it has a direction it will create two sets of sprites, left and right
        if direction:
            all_sprites[image.replace('.png', '_right')] = sprites
            all_sprites[image.replace('.png', '_left')] = flip(sprites)
        #if no direction, just adds it to all_sprites with corresponding name
        else:
            all_sprites[image.replace('.png', '')] = sprites

    #returns all the sprites loaded
    return all_sprites

#gets the block used
def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")

    #turns image into transparent
    image = pygame.image.load(path).convert_alpha()

    #creates a surface with size of the block
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)

    #creates the rectangle representing the block and location of it on the sprite sheet
    rect = pygame.Rect(96, 0, size, size)

    #copies the image with rect onto surface
    surface.blit(image, (0, 0), rect)

    #scales and returns the block
    return pygame.transform.scale2x(surface)

#class for player extending off Sprite in pygame
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    #gravity of the player
    GRAVITY = 1

    #loads the sprite sheet
    SPRITES = load_sprite_sheets('MainCharacters', 'NinjaFrog', 32, 32, True)
    
    #delay between each sprite 
    ANIMATION_DELAY = 3

    #initialize the player
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    #decrease y vel (down is positve), update animation, jump_count, fall_count
    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    #adding moving rect by the displacement of x, y
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    #make vel negative, change direction to left and start animation
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    #make vel positive, change direction to right and start animation
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    #constantly bring the player down with gravity, checks if player is moving, update the fall count, updates hit
    def loop(self, fps):
        #imitates acceleration
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit = 0


        self.update_sprite()

    #resets fall_count, y_vel, jump_count
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
    
    #checks what state the player is in, updates sprite accordingly
    def update_sprite(self):
        sprite_sheet = 'idle'
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            if self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > (self.GRAVITY * 2):
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        
        #gets the sprite sheet name based on player state
        sprite_sheet_name = sprite_sheet + '_' + self.direction

        #finds the sprite sheet in all of the sprites
        sprites = self.SPRITES[sprite_sheet_name]

        #gets the index of current
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    #keeps player hitbox and mask synchronized with current sprite
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    #draws player
    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

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
    
    def __init__ (self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

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

#draws the background, player, all object, and scrolling
def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    
    pygame.display.update()

#checks if player is collding with a block vertically
def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            #if player is moving down and touching object, it will be ontop
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()

            #if player is moving up and touching object, it reverse the y_vel
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects

#check for collision
def collide(player, objects, dx):
    #move player to impending position
    player.move(dx, 0)
    player.update()
    collided_object = None
    
    #check if player is touching an object
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    #move back the player to original position
    player.move(-dx, 0)
    player.update()

    return collided_object

#handles the movement of player
def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    
    #check if player is colliding
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 3)
    collide_right = collide(player, objects, PLAYER_VEL * 3)

    #if the key is pressed
    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)

    #handle verticle collision
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)

    #checks if player hit a 'fire' trap
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

def main(window):
    clock = pygame.time.Clock()

    #get the background image
    background, bg_image = get_background("Green.png")

    #size of block terrains
    block_size = 96

    #creates player
    player = Player(100, 100, 50, 50)

    #creates fire
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)

    #sets fire to turn on
    fire.on()

    #loop through and make the floors
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) 
             for i in range(-WIDTH // block_size, (WIDTH *2) // block_size)]
    
    #all objects
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size), fire, Block(block_size, HEIGHT - block_size * 5, block_size)]

    #set the offset and area before scrolls
    offset_x = 0
    scroll_area_width = 200

    #running until quit
    run = True
    while run:
        clock.tick(FPS)

        #check for all keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #check for jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                    
        #loop through all player events
        player.loop(FPS)

        #loop through all fire events
        fire.loop()

        #check if player can move and move them
        handle_move(player, objects)

        #draws player on screen
        draw(window, background, bg_image, player, objects, offset_x)

        #handles scrolling
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)