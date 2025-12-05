import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

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

run = True
while run:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(bg, (0, 0))

    pygame.display.update() 

pygame.quit()
