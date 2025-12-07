import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

#Setting the FPS for the game
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Starboard Strike')


# Define game variables
rows = 5
cols = 5

# Define the colours for the game
red = (255, 0, 0)
green = (0, 255, 0)


# Load the background image for the game
image_path = 'images/background1.png' 
try:
    bg_original = pygame.image.load(image_path).convert()
    
    # Scale the image to fit the screen dimensions
    bg = pygame.transform.scale(bg_original, (screen_width, screen_height))

except pygame.error as e:
    print(f"Error loading or scaling background image: {e}")

    # Fallback: create a red surface if image fails
    bg = pygame.Surface((screen_width, screen_height))
    bg.fill((255, 0, 0)) 

# Creating the player class aka Spaceship
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        # Creating the set movement speed
        speed = 8

        # Set cooldown for bullet time
        cooldown = 500


        # Movement keys, WASD to move player
        key = pygame.key.get_pressed ()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        # Record current time
        time_now = pygame.time.get_ticks()

        # Shoot the bullets
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # Draw the Health bar for the Player
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        

# Create Bullets Class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()


# Create the Aliens Class (Enemy)
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor=2.5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/alien" + str(random.randint(1,5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

        # Rescale the alien sprite images
        original_image = pygame.image.load("images/alien" + str(random.randint(1,5)) + ".png").convert_alpha()
        
        # Get the original size
        original_width, original_height = original_image.get_size()
        
        # Calculate new dimensions
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        
        # Get the rectangle of the *newly scaled* image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
    


# Create png groups for easier readability/organization
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()


# Create the Aliens
def create_aliens():

    # Generate the enemy aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)

create_aliens()


# Player Location/Starting Point
player = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(player)

run = True
while run:

    clock.tick(fps)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(bg, (0, 0))


    # Update the player
    player.update()


    # Update sprite players
    bullet_group.update()


    # Update aliens 
    alien_group.update()


    # Draw the pngs on the screen
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)

    pygame.display.update() 

pygame.quit()
