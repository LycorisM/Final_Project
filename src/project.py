import pygame
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
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


#Create png groups for easier readability/organization
spaceship_group = pygame.sprite.Group()



# Player Location/Starting Point
player = Spaceship(int(screen_width / 2), screen_height - 100)
spaceship_group.add(player)

run = True
while run:

    clock.tick(fps)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(bg, (0, 0))

    # Draw the pngs on the screen
    spaceship_group.draw(screen)

    pygame.display.update() 

pygame.quit()
