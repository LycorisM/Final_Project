import pygame
import random
from pygame import mixer
from pygame.locals import *


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# Initialize Pygame
pygame.init()
pygame.font.init()

#Setting the FPS for the game
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Starboard Strike')

gamemusic_fx = pygame.mixer.Sound("sounds/gamemusic.mp3")
gamemusic_fx.set_volume(0.35)


explosion_fx = pygame.mixer.Sound("sounds/explosion.mp3")
explosion_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("sounds/laser.wav")
laser_fx.set_volume(0.25)

playerdeath_fx = pygame.mixer.Sound("sounds/player_death.mp3")
playerdeath_fx.set_volume(0.25)

# Define game variables
rows = 5
cols = 5
alien_cooldown = 1000 # Bullet cooldown in milliseconds
last_alien_shot = pygame.time.get_ticks()

# 0 = Game Over, 1 = Player Win, -1 = Player Lose
game_over = 0


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
        game_over = 0


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
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        
        # Update mask
        self.mask = pygame.mask.from_surface(self.image)

        # Draw the Health bar for the Player
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, "large")
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over


# Play the music
gamemusic_fx.play()

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
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)


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



# Create Alien Bullets Class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion_fx.play()
            
            #reduce ship health
            player.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)
             

# Create Explosion Animation Class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size="small"):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"images/exp{num}.png")

        if size == "large":
                # Scale up by 2x for a big player explosion
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        elif size == "medium":
                # Scale up by 1.5x for a medium explosion
                img = pygame.transform.scale(img, (int(img.get_width() * 1.5), int(img.get_height() * 1.5)))
            # If size is "small" (default), no scaling is applied

        #Add image list
        self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0


    def update(self):
        explosion_speed = 12

        # Update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1

            center = self.rect.center
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=center)

        # Animation ends, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


# Create png groups for easier readability/organization
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

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


    # Create random alien bullets
    # Record current time
    time_now = pygame.time.get_ticks()
    # Shoot
    if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now

    # All Aliens are killed
    if len(alien_group) == 0:
        game_over = 1

    if game_over == 0:
        # Update the player
        game_over = player.update()


        # Update sprite groups
        bullet_group.update()
        alien_group.update()
        alien_bullet_group.update()
        explosion_group.update()


    # Draw the pngs on the screen
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    pygame.display.update() 

pygame.mixer.music.stop()
pygame.quit()
