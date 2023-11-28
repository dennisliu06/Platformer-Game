import pygame
import os
from os import listdir
from os.path import join
from shared import WIDTH, HEIGHT

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_VEL = 5

#draws the background, player, all object, and scrolling
def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    
    pygame.display.update()

#checks if player falls 
def handle_player_fall(player):
    if player.rect.y > HEIGHT * 2:
        print("below")


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

            if obj and obj.name == "spikes":
                player.make_hit()

            if obj and obj.name == "fire":
                player.make_hit()

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
    """ it hit when the player touches the side of the block, not wanted
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
    """
        

# passes the location of the file, the width and height of the spritesheets, and if it has a direction
def load_sprite_sheets(dir1, dir2, width, height, direction=False, dir3=None):
    # creates the path to the location of the file, if there is a dir3 it will add it
    if dir3:
        path = join('assets', dir1, dir2, dir3)
    else:
        path = join('assets', dir1, dir2)

    # adds files into 'images' after checking if it is a normal file
    images = [f for f in listdir(path) if os.path.isfile(join(path, f))]

    # dictionary to represent name with a sprite
    all_sprites = {}

    # load each sprite sheet
    for image in images:
        # loads the image, and converts it into a transparent background
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        # creates an array of sprites within the image
        sprites = []

        # counts the number of sprites there is given the width of the sprite
        for i in range(sprite_sheet.get_width() // width):
            # creates a surface for a sprite
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)

            # creates a rect object which represents the area to be copied
            rect = pygame.Rect(i * width, 0, width, height)

            # blits the portion of the sprite sheet onto the surface
            surface.blit(sprite_sheet, (0, 0), rect)

            # scaled it 2x and also added to sprites array
            sprites.append(pygame.transform.scale2x(surface))

        # if it has a direction it will create two sets of sprites, left and right
        if direction:
            all_sprites[image.replace('.png', '_right')] = sprites
            all_sprites[image.replace('.png', '_left')] = flip(sprites)
        # if no direction, just adds it to all_sprites with corresponding name
        else:
            all_sprites[image.replace('.png', '')] = sprites

    # returns all the sprites loaded
    return all_sprites

# flip the sprites so it faces left
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]