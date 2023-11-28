import pygame
from player import Player
from objects import Block, Fire, Spikes
from background import get_background
from game_logic import handle_move, draw, handle_player_fall
from shared import WIDTH, HEIGHT, FPS
pygame.init()

#creates the window
window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Platformer!")

def main(window):
    clock = pygame.time.Clock()

    #get the background image
    background, bg_image = get_background("Green.png")

    #size of block terrains
    block_size = 96

    # Set the initial position of the player
    initial_player_x = - WIDTH // block_size * block_size
    floor_height = HEIGHT - (block_size * 2)

    #creates player
    player = Player(initial_player_x + block_size, floor_height, 50, 50)

    #creates fire
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)

    #creates spikes
    spikes1 = Spikes(-511, HEIGHT - block_size - 32, 16, 16)
    spikes2 = Spikes(-543, HEIGHT - block_size - 32, 16, 16)
    spikes3 = Spikes(-575, HEIGHT - block_size - 32, 16, 16)

    #sets fire to turn on
    fire.on()

    #loop through and make the floors
    floor = [Block(i * block_size, HEIGHT - block_size, block_size, 96, 0) 
             for i in range(-WIDTH // block_size, (WIDTH *2) // block_size)]
    
    #wall in the beginning
    starting_wall = [Block(initial_player_x - block_size, (i * block_size) - 64, block_size, 0, 128) 
                     for i in range(-HEIGHT // block_size, (WIDTH * 2) // block_size)]

    #all objects
    objects = [*floor,
               *starting_wall, 
               Block(0, HEIGHT - block_size * 2, block_size, 0, 128), 
               fire, 
               Block(block_size, HEIGHT - block_size * 5, block_size, 0, 128),
               spikes1,
               spikes2,
               spikes3
               ]

    #set the offset and area before scrolls
    offset_x = initial_player_x - (WIDTH // 10)
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

        handle_player_fall(player)

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
    