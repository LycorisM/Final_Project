import pygame  # Import the Pygame library
import sys    # Import the sys module for exiting the program

pygame.init()  # Initialize all the Pygame modules

width = 1000   # Define the width of the game screen
height = 800   # Define the height of the game screen
size = (width, height)  # Create a tuple representing the screen size

screen = pygame.display.set_mode(size)  # Create the game window with the specified size
clock = pygame.time.Clock()  # Create a Clock object to control the frame rate

run = 1  # Initialize a flag to control the game loop

while run:  # The main game loop
    screen.fill((0, 0, 0))  # Fill the screen with yellow color (RGB: 255, 255, 0)

    for event in pygame.event.get():  # Iterate through all pending events
        if event.type == pygame.QUIT:  # If the user clicks the close button
            run = 0  # Set the 'run' flag to 0 to exit the loop

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(60)  # Limit the frame rate to 60 frames per second

pygame.quit()  # Uninitialize all Pygame modules
sys.exit()     # Exit the Python program
