import pygame
from game_logic import load_sprite_sheets
from shared import WIDTH, HEIGHT


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
        self.lives = 5

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
        self.lives -= 1

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

    def update_lives(self, fps):
        if fps * 2 < self.hit_count:
            self.lives -= 1

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
            

        if self.lives <= 0:
            print("you died")

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