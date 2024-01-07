import pygame
import random
import os
from pygame import mixer
mixer.init()
mixer.music.load(r"C:\Users\Roni\mu_code\age of war\Age of War - Theme Soundtrack.mp3")
mixer.music.set_volume(0.2)
mixer.music.play()
# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1080
HEIGHT = 432
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Age of War")

# Load background image
background = pygame.image.load(r"C:\Users\Roni\mu_code\age of war\bg1.jpg")
tent = pygame.image.load(r"C:\Users\Roni\mu_code\age of war\tent.png")
enemytent = pygame.transform.flip(tent,1,0)
#menu images
army = pygame.transform.scale(pygame.image.load(r"C:\Users\Roni\mu_code\age of war\army.png"),(50,50))
buyturret = pygame.transform.scale(pygame.image.load(r"C:\Users\Roni\mu_code\age of war\buyturret.png"),(50,50))
sellturret = pygame.transform.scale(pygame.image.load(r"C:\Users\Roni\mu_code\age of war\sellturret.png"),(50,50))
evolve = pygame.transform.scale(pygame.image.load(r"C:\Users\Roni\mu_code\age of war\evolve.png"),(50,50))
goback = pygame.transform.scale(pygame.image.load(r"C:\Users\Roni\mu_code\age of war\goback.png"),(50,50))
archerpfp=pygame.transform.scale(pygame.image.load(r"C:\Users\Roni\mu_code\age of war\archerpfp.png"),(50,50))
spearmanpfp=pygame.transform.scale(pygame.image.load(r"C:\Users\Roni\mu_code\age of war\spearmanpfp.png"),(50,50))
# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
# Set the completion bar position and dimensions
bar_width = 300
bar_height = 20
bar_x = (WIDTH - bar_width) // 2
bar_y = 20
money = 0
hitbox1=pygame.Rect(850,0,50,50)
hitbox2=pygame.Rect(910,0,50,50)
hitbox3=pygame.Rect(970,0,50,50)
hitbox4=pygame.Rect(1030,0,50,50)
costspearman=75
costarcher=100
startingcash=1250000
hitbox1cost=75
hitbox2cost=100
moneytotal=startingcash
#counter = 0
# Set the training time (in frames) and the current training progress
training_time = FPS * 2  # 2 seconds
training_progress = 0
max_queue_size = 5
elapsed_time = 0
attack_time=0
exptimer=0
exp=0
# Create a list to store the training queue
training_queue = []
training_type=[]
# Function to draw the completion bar
def draw_completion_bar():
    # Calculate the width of the progress bar based on the training progress
    progress_width = int(bar_width * (training_progress / training_time))
    # Draw the background bar
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))

    # Draw the progress bar
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, progress_width, bar_height))

# Load sprite images
folder_path_spearman = r"C:\Users\Roni\mu_code\age of war\spearman"
folder_path_archer = r"C:\Users\Roni\mu_code\age of war\archer"
folder_path_attack_spearman = r"C:\Users\Roni\mu_code\age of war\attack_spearman"
folder_path_attack_archer = r"C:\Users\Roni\mu_code\age of war\attack_archer"
folder_path_death_spearman = r"C:\Users\Roni\mu_code\age of war\death_spearman"
folder_path_death_archer = r"C:\Users\Roni\mu_code\age of war\death_archer"

spearman_images = []
for filename in os.listdir(folder_path_spearman):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(folder_path_spearman, filename)
        image = pygame.image.load(image_path)
        spearman_images.append(image)

archer_images = []
for filename in os.listdir(folder_path_archer):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(folder_path_archer, filename)
        image = pygame.image.load(image_path)
        archer_images.append(image)

attack_spearman_images = []
for filename in os.listdir(folder_path_attack_spearman):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(folder_path_attack_spearman, filename)
        image = pygame.image.load(image_path)
        attack_spearman_images.append(image)

attack_archer_images = []
for filename in os.listdir(folder_path_attack_archer):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(folder_path_attack_archer, filename)
        image = pygame.image.load(image_path)
        attack_archer_images.append(image)

death_spearman_images = []
for filename in os.listdir(folder_path_death_spearman):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(folder_path_death_spearman, filename)
        image = pygame.image.load(image_path)
        death_spearman_images.append(image)

death_archer_images = []
for filename in os.listdir(folder_path_death_archer):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(folder_path_death_archer, filename)
        image = pygame.image.load(image_path)
        death_archer_images.append(image)


# Sprite animation states
IDLE = "idle"
ATTACK = "attack"
DEATH = "death"
STANDSTILL="standstill"
DEFAULT="default"
BUYSOLDIER="soldier"
menuState=DEFAULT
# Set sprite properties
sprite_width = 100
sprite_height = 100
sprite_speed = 5
square_x = 400
square_y = 100
# List to store sprite positions, images, type, and animation state
sprites = []

# Function to spawn a sprite
def spawn_sprite(image_list, attack_images, death_images):
    sprite_x = 0
    sprite_y = HEIGHT - sprite_height * 2+30
    sprite_image = image_list[0]
    sprite_type = image_list  # Assigning the image list as the sprite type for simplicity
    sprite_state = IDLE
    sprite_frame = 0
    sprite_frame_count = len(image_list)
    sprite_animation_speed = 50  # Number of frames to wait before changing the animation frame
    attack_completed = False  # Flag to track if the attack animation has been completed

    sprites.append((sprite_x, sprite_y, sprite_image, sprite_type, sprite_state, sprite_frame, sprite_frame_count, sprite_animation_speed, attack_images, death_images, attack_completed))

# Function to update the sprites
def update_sprites():
    global attack_time
    spacing = 10  # Spacing between sprites in the queue

    for i, sprite in enumerate(sprites):
        sprite_x, sprite_y, sprite_image, sprite_type, sprite_state, sprite_frame, sprite_frame_count, sprite_animation_speed, attack_images, death_images, attack_completed = sprite

        if sprite_state == IDLE:
            sprite_frame += 1
            if i == 0 or sprites[i - 1][4] != ATTACK:  # Check if it's the first sprite or the previous sprite is not attacking
                if sprite_x < WIDTH - sprite_width - (i * (sprite_width + spacing)):
                    sprite_x += 5
                elif sprite_x >= WIDTH- sprite_width:
                    sprite_state = ATTACK
            if sprite_frame >= sprite_frame_count:
                sprite_frame = 0
            sprite_image = sprite_type[sprite_frame]
            sprite_animation_speed = FPS*50
        elif sprite_state== STANDSTILL:
            sprite_image = sprite_type[0]
        elif sprite_state == ATTACK:
            sprite_frame += 1
            if sprite_frame >= sprite_frame_count:
                sprite_frame = 0
                attack_completed = True
            sprite_image = attack_images[sprite_frame]
            sprite_animation_speed = FPS*500
            sprite_state = IDLE

        elif sprite_state == DEATH:
            sprite_frame += 1
            if sprite_frame >= len(death_images):
                sprites.pop(i)
                continue
            sprite_image = death_images[sprite_frame]

        sprites[i] = (
            sprite_x,
            sprite_y,
            sprite_image,
            sprite_type,
            sprite_state,
            sprite_frame,
            sprite_frame_count,
            sprite_animation_speed,
            attack_images,
            death_images,
            attack_completed
        )
def drawMenuDefault():
    screen.blit(army,(850,0))
    screen.blit(buyturret,(910,0))
    screen.blit(sellturret,(970,0))
    screen.blit(evolve,(1030,0))
def drawMenuSoldier():
    screen.blit(spearmanpfp,(850,0))
    textcostspearman=fontcost.render(str(costspearman), True, WHITE)
    screen.blit(textcostspearman, (865, 60))
    pygame.draw.ellipse(screen,(255, 192, 0),(850,60,10,10))
    textcostarcher=fontcost.render(str(costarcher), True, WHITE)
    pygame.draw.ellipse(screen,(255, 192, 0),(915,60,10,10))
    screen.blit(textcostarcher, (925, 60))
    screen.blit(archerpfp,(910,0))
    #screen.blit(sellturret,(970,0))
    screen.blit(goback,(1030,0))
    hitbox1cost=75
    hitbox2cost=100
def drawHollowSquare(x):

    square_size = 50
    square_thickness = 2
    pygame.draw.rect(screen, BLACK, pygame.Rect(square_x+x, square_y, square_size, square_thickness))  # Top line
    pygame.draw.rect(screen, BLACK, pygame.Rect(square_x+x, square_y, square_thickness, square_size))  # Left line
    pygame.draw.rect(screen, BLACK, pygame.Rect(square_x+x, square_y + square_size - square_thickness, square_size, square_thickness))  # Bottom line
    pygame.draw.rect(screen, BLACK, pygame.Rect(square_x+x + square_size - square_thickness, square_y, square_thickness, square_size))  # Right line

def drawQueue(x):
    drawHollowSquare(0)
    drawHollowSquare(60)
    drawHollowSquare(120)
    drawHollowSquare(180)
    drawHollowSquare(240)
    if x==1:
        screen.blit(training_type[0],(square_x,square_y))
    if x==2:
        screen.blit(training_type[0],(square_x,square_y))
        screen.blit(training_type[1],(square_x+60,square_y))
    if x==3:
        screen.blit(training_type[0],(square_x,square_y))
        screen.blit(training_type[1],(square_x+60,square_y))
        screen.blit(training_type[2],(square_x+60+60,square_y))
    if x==4:
        screen.blit(training_type[0],(square_x,square_y))
        screen.blit(training_type[1],(square_x+60,square_y))
        screen.blit(training_type[2],(square_x+60+60,square_y))
        screen.blit(training_type[3],(square_x+60+60+60,square_y))
    if x==5:
        screen.blit(training_type[0],(square_x,square_y))
        screen.blit(training_type[1],(square_x+60,square_y))
        screen.blit(training_type[2],(square_x+60+60,square_y))
        screen.blit(training_type[3],(square_x+60+60+60,square_y))
        screen.blit(training_type[4],(square_x+60+60+60+60,square_y))
font = pygame.font.SysFont(None, 24)
fontcost=pygame.font.SysFont(None, 18)

# Game loop
running = True
clock = pygame.time.Clock()

# Spawn initial sprites
# spawn_sprite(spearman_images, attack_spearman_images, death_spearman_images)
# spawn_sprite(archer_images, attack_archer_images, death_archer_images)
attack_state = False
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if hitbox1.collidepoint(event.pos) and menuState == BUYSOLDIER and moneytotal-hitbox1cost>=0:
                    if len(training_queue) < max_queue_size:
                        training_queue.append(training_time)
                        training_type.append(spearmanpfp)
                        moneytotal-=hitbox1cost
                elif hitbox2.collidepoint(event.pos) and menuState == BUYSOLDIER and moneytotal-hitbox2cost>=0:
                    if len(training_queue) < max_queue_size:
                        training_queue.append(training_time)
                        training_type.append(archerpfp)
                        moneytotal-=hitbox2cost
                # spawn_sprite(archer_images, attack_archer_images, death_archer_images)  # Spawn an archer
            elif event.key == pygame.K_a:
                for i in range(len(sprites)):
                    sprite = sprites[i]
                    sprite_x, sprite_y, sprite_image, sprite_type, sprite_state, sprite_frame, sprite_frame_count, sprite_animation_speed, attack_images, death_images, attack_completed = sprite
                    if sprite_state != DEATH:
                        sprites[i] = (
                            sprite_x, sprite_y, sprite_image, sprite_type, ATTACK, sprite_frame, sprite_frame_count,
                            sprite_animation_speed, attack_images, death_images, False
                        )
    mouse_pos = pygame.mouse.get_pos()
    L,M,R =pygame.mouse.get_pressed()
    elapsed_time += clock.tick(FPS) / 1000  # Divide by 1000 to convert milliseconds to seconds
    exptimer+=clock.tick(FPS)/1000
    # Check if 1 second has passed
    if elapsed_time >= 0.2:
        moneytotal += 1  # Increment the money variable by 1
        elapsed_time = 0
    if exptimer >= 0.5:
        exp += 1  # Increment the exp variable by 1
        exptimer = 0
    for sprite in sprites:
        sprite_rect = pygame.Rect(sprite[0], sprite[1], sprite_width, sprite_height)
        if sprite_rect.collidepoint(mouse_pos):
            sprites.remove(sprite)


    # Update

    if training_queue:
        training_time = training_queue[0]
        if training_progress < training_time:
            training_progress += 1
        else:
            training_queue.pop(0)  # Remove the first soldier from the queue
            if training_type[0]==spearmanpfp:
                spawn_sprite(spearman_images, attack_spearman_images, death_spearman_images)  # Spawn the soldier
                training_type.pop(0)
            elif training_type[0]==archerpfp:
                spawn_sprite(archer_images, attack_archer_images, death_archer_images)  # Spawn the soldier
                training_type.pop(0)
            training_progress = 0  # Reset the training progress
    # Render

    update_sprites()
    screen.blit(background, (0, 0))
    screen.blit(tent, (-50,80))
    screen.blit(enemytent, (WIDTH-200,80))
    #money

    pygame.draw.ellipse(screen,(255, 192, 0),(50,20,15,15))
    cash = font.render(str(moneytotal), True, WHITE)
    experience=font.render("Exp:"+str(exp), True, WHITE)
    screen.blit(cash, (70, 20))
    screen.blit(experience, (34, 40))
    drawQueue(len(training_queue))
    if training_queue:
        draw_completion_bar()
    for sprite in sprites:
        sprite_x, sprite_y, sprite_image, sprite_type, sprite_state, sprite_frame, sprite_frame_count, sprite_animation_speed, attack_images, death_images, attack_completed = sprite
        screen.blit(sprite_image, (sprite_x, sprite_y))

    if(menuState==DEFAULT):
        drawMenuDefault()
        if(hitbox1.collidepoint(mouse_pos)and L==1):
            menuState=BUYSOLDIER
        if(hitbox2.collidepoint(mouse_pos)and L==1):
            menuState=BUYSOLDIER
    if(menuState==BUYSOLDIER):
        drawMenuSoldier()
        if(hitbox4.collidepoint(mouse_pos)and L==1):
            menuState=DEFAULT
    pygame.display.flip()

    # Set the FPS
    clock.tick(FPS)

# Quit the game
pygame.quit()
