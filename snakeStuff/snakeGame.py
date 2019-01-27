"""
'Slip Snoot' game by Gavin Ceballos,
refrenced from the Pygame tutorial on 'The New Boston' youtube channel.
Requires PYGAME and the associated sprites availible on:
https://github.com/Parsnipss/snoot-slip
"""

import pygame
import random

pygame.init()

# Colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (20,84,0)
blue = (0,0,255)

# Window Size
display_width = 800
display_height = 600

# Creates Window + Title
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slip Snoot')

# Not working
icon = pygame.image.load('apple30x30.png')
pygame.display.set_icon(icon)

# Sprites
img = pygame.image.load('snakeHead.PNG')
appleSprite = pygame.image.load('apple30x30.PNG')
poisonSprite = pygame.image.load('poison30x30.PNG')

# Fps Counting
clock = pygame.time.Clock()
#FPS = 15

# Starting Direction
direction = "right"

# Uniform Size
block_size = 20
appleThickness = 30

button_x = (display_width/2)
button_y = 500
button_x_length = 200
button_y_length = 100

# Fonts for text
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

    
def pause():
    
    paused = True
    message_to_screen("Paused",
                      black,
                      -100,
                      size="large")
    message_to_screen("Press ESC to resume or Q to quit.",
                      black,
                      180)
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        clock.tick(5)
        

def score(score, hp):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])
    text = smallfont.render("HP: " + str(hp), True, black)
    gameDisplay.blit(text, [0,20])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - appleThickness)) #/10.0)*10.0 #block_size is subtracted so that it does not spawn out of bounds
    randAppleY = round(random.randrange(0, display_height - appleThickness)) #/10.0)*10.0 #Rounded to align with snake coordinates (multiples of 10)            
    
    return randAppleX, randAppleY

def randPoisonAppleGen(): #CHANGE 2 Poison Apples Can Kill the snake (Replication of normal apple code w/ modifications)
    randPoisonAppleX = round(random.randrange(0, display_width - appleThickness))
    randPoisonAppleY = round(random.randrange(0, display_height - appleThickness))

    return randPoisonAppleX, randPoisonAppleY

def start_button(): #CHANGE 4 Created a start button (Documentation about mouse position and press functions)
    text = smallfont.render("Start Game", True, white)
    pygame.draw.rect(gameDisplay, green, (button_x - (button_x_length/2), button_y, button_x_length, button_y_length))
    gameDisplay.blit(text, [button_x - (button_x_length/2),button_y +(button_y_length/2)])
                      
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    (mouse1, mouse2, mouse3) = pygame.mouse.get_pressed()
    if mouse_x > button_x - (button_x_length/2) and mouse_y > button_y:
        if mouse_x < button_x + (button_x_length/2) and mouse_y < button_y + button_y_length and mouse1 == 1:
            print('Clicked!')
            intro = False
            return intro
    
def game_intro():
    
    intro = True
    
    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        
        gameDisplay.fill(black)
        message_to_screen("Welcome to Slip Snoot",
                          green,
                          -100,
                          size="medium")
        message_to_screen("The objective of the game is to eat red apples.",
                          white,
                          -30
                          )
        message_to_screen("The more apples you eat, the longer you get.",
                          white,
                          10
                          )
        message_to_screen("If you run into yourself or the edges, you die.",
                          white,
                          50
                          )
        message_to_screen("There are also poison apples (Those will kill you).",
                          white,
                          90
                          )
        message_to_screen("The shift key will allow you to move faster, be careful though!",
                          white,
                          130
                          )
        message_to_screen("Click the button to play, ESC to pause, or Q to quit.",
                          white,
                          180
                          )
        introState = start_button()
        if introState == False:
            intro = False
        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakeList):
    
    #Rotation Logic
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
        
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
        
    if direction == "up":
        head = img
    
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
    
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    
    for XnY in  snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])
        #pygame.draw.circle(gameDisplay, green, (XnY[0], XnY[1]), 10) #int(block_size/2)
        
def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
        
    return textSurface, textSurface.get_rect()
    

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)
    
    
def gameLoop():
    global direction # Direction can be modified by game loop

    global FPS

    FPS = 15
        
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0
    
    snakeList = []
    snakeLength = 1

    hp = 3
    
    randAppleX, randAppleY = randAppleGen()
    randPoisonAppleX, randPoisonAppleY = randPoisonAppleGen()
    
    while not gameExit:

        if gameOver == True:
            message_to_screen("Game over", 
                              red,
                              -50, 
                              size="large")
            message_to_screen("Press C to play again or Q to quit.", 
                              black, 
                              50,
                              size = "medium")
            pygame.display.update()
            
        while gameOver == True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        #CHANGE 3 Fixed movement to prevent doubling-over (refrenced exsisting code and made full use of 'direction' component
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN: # User Inputs
                if event.key == pygame.K_LEFT or event.key == pygame.K_a and direction != "right":
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d and direction != "left":
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w and direction != "down":
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s and direction != "up":
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_ESCAPE:
                    pause()
                elif event.key == pygame.K_LSHIFT:  #CHANGE 1 Added a "sprint" fucntionality (based on pygame documentation and ideas about using KEYUP)
                    FPS = FPS + 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    FPS = FPS - 10
                    
        
        #Creates Death Bounds
        if lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0:
            gameOver = True


        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        #Sprite Drawing
        gameDisplay.blit(appleSprite, (randAppleX, randAppleY))
        gameDisplay.blit(poisonSprite,(randPoisonAppleX, randPoisonAppleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        
        if len(snakeList) > snakeLength:
            del snakeList[0]
            
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        
        snake(block_size, snakeList)

        #CHANGE 5 Health Points (using what we learned about accumulators)
        score(snakeLength - 1, hp)
        
        pygame.display.update()
        
        # Collison Code (including Poison Apples)
        if lead_x > randAppleX and lead_x < randAppleX + appleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + appleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + appleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen()
                randPoisonAppleX, randPoisonAppleY = randPoisonAppleGen()
                snakeLength += 1

        #Poisen apple collision
        elif lead_x > randPoisonAppleX and lead_x < randPoisonAppleX + appleThickness or lead_x + block_size > randPoisonAppleX and lead_x + block_size < randPoisonAppleX + appleThickness:
            if lead_y > randPoisonAppleY and lead_y < randPoisonAppleY + appleThickness or lead_y + block_size > randPoisonAppleY and lead_y + block_size < randPoisonAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen()
                randPoisonAppleX, randPoisonAppleY = randPoisonAppleGen()
                hp = hp - 1
                if hp == 0:
                    gameOver = True
        #FPS = frames_per_second(snakeLength)
        clock.tick(FPS)

    pygame.quit()
    quit()
    
game_intro()    
gameLoop()
