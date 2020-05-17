import pygame, random, sys
import tkinter as tk
from tkinter import ttk

pygame.init()

# initialise a clock to set game speed/FPS
clock = pygame.time.Clock()

# colour variables
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
pause = False

# screen variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
#create an 800x600 pixel screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

# music settings
# Audio files
car_crash_sound = pygame.mixer.Sound("media/car_crash.wav")
car_start_sound = pygame.mixer.Sound("media/car_start.wav")
pygame.mixer.music.load("media/game_music.wav")

#button variables
button_w = 160
button_h = 60

# font variables
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

# image variables
carIMG = pygame.image.load("Game-Assignment\media\car.png")
obstacleIMG = pygame.image.load("Game-Assignment\media/obstacleCar.png")
movingIMG = pygame.image.load("Game-Assignment\media/redCar.png") # might not use this...just here if needed in the code
backgroundIMG = pygame.image.load("Game-Assignment\media/background1.jpg")

# text stuff for next level screen update...
def message(text, textSize, textColor, textCenterPos):
    textFont = pygame.font.Font("freesansbold.ttf", textSize)
    textSurf = textFont.render(text, True, textColor)
    textRect = textSurf.get_rect()
    textRect.center = textCenterPos
    screen.blit(textSurf, textRect)

# define the button for the game menu
def button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))
    message(text, 22, WHITE, (x + w / 2, y + h / 2))

# A popup message to uss throughout the game
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

# Crash Event
def crash():
    message('You Crashed!', 48, bright_red, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
    pygame.mixer.Sound.play(car_crash_sound)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        button('PLAY AGAIN', SCREEN_WIDTH / 2 - button_w / 2, SCREEN_HEIGHT / 2, button_w, button_h, GREEN, bright_green, main)
        button('MAIN MENU', SCREEN_WIDTH / 2 - button_w / 2, SCREEN_HEIGHT / 2 + 3 * button_h / 2, button_w, button_h, RED,
               RED, gameintro)
        pygame.display.update()
        clock.tick(15)

# define the unpause function, used for the menu
def unpause():
    global pause
    pause = False
    pygame.mixer.music.unpause()

# define the pause function, used for the menu
def paused():
    pygame.mixer.music.pause()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        screen.fill(WHITE)
        button('RESUME', SCREEN_HEIGHT / 2 - button_w / 2, SCREEN_HEIGHT / 2, button_w, button_h, GREEN, bright_green, unpause)
        button('QUIT', SCREEN_WIDTH / 2 - button_w / 2, SCREEN_HEIGHT / 2 + 3 * button_h / 2, button_w, button_h, RED, bright_red,
               gameintro)
        message('Game Paused', 64, BLACK, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        pygame.display.update()
        clock.tick(15)

# define the quit game button used when you click the quit button
def quitgame():
    pygame.quit()
    sys.exit()


# Load Screen
def loading():
    pygame.mixer.Sound.play(car_start_sound)
    screen.fill(WHITE)
    message('LOADING', 42, BLACK, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    x = SCREEN_WIDTH / 5
    endx = 4 * x
    y = 2 * SCREEN_HEIGHT / 3
    while x <= endx:
        x += 15
        pygame.draw.rect(screen, BLACK, (x, y, 15, 5))
        pygame.display.update()
        clock.tick(10)
    gameintro()


# Intro Screen
def gameintro():
    pygame.mixer.music.play(-1)
    screen.fill(WHITE)
    pygame.time.delay(2000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        screen.fill(WHITE)
        button('PLAY', SCREEN_WIDTH / 2 - button_w / 2, SCREEN_HEIGHT / 2, button_w, button_h, GREEN, bright_green, main)
        button('QUIT', SCREEN_WIDTH / 2 - button_w / 2, SCREEN_HEIGHT / 2 + 3 * button_h / 2, button_w, button_h, RED, bright_red,
               quitgame)
        message('Car Park Game', 72, BLACK, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        pygame.display.update()
        clock.tick(15)

# This class represents the character that the player controls
class Player(pygame.sprite.Sprite):

    def __init__(self):

       super().__init__()

       # Set height and width of the square that the player car is (invisible)...like a box around the player image
       width = 45
       height = 45
       self.image = pygame.Surface([width, height])
       self.image = carIMG
       self.rect = self.image.get_rect()

       # Player speed
       self.change_x = 0
       self.change_y = 0

       self.level = None

    def update(self):

        # move let and right
        self.rect.x += self.change_x

        #did this make the player hit the wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.level.obstacle_list, False)
        for block in block_hit_list:
            #If moving right, set right side to the left side of the item hit
            if self.change_x > 0:
                crash()
                #self.rect.right = block.rect.left - testing pupup window
            elif self.change_x < 0:
                crash()
                # Otherwise if moving left, do opposite
                #self.rect.left = block.rect.right testing pupup window

        # Move up/down
        self.rect.y += self.change_y

        #did this make the player hit the wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.level.obstacle_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                crash()
            elif self.change_y < 0:
                #popupmsg("you hit an obstacle!")
                #stop moving up
                self.change_y = 0
                if isinstance(block, MovingObstacle):
                    self.rect.x += block.change_x

    # classes to define player controlled movement using the arrow keys
    def go_left(self):
        self.change_x = -6 #go left 6 pixels

    def go_right(self):
        self.change_x = 6 #go right 6 pixels
        
    def go_up(self):
        self.change_y = -6 #go up 6 pixels
        
    def go_down(self):
        self.change_y = 6 #go down 6 pixels

    def stopX(self):
        self.change_x = 0

    def stopY(self):
        self.change_y = 0


# This class represents the walls/barriers in the game #
class Obstacle(pygame.sprite.Sprite):

    def __init__(self, width, height): #(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image = obstacleIMG
        self.rect = self.image.get_rect()

# Base class for all car-parks
class CarPark(object):
    #construct to create the lists of walls and enemies
    def __init__(self, player):
        self.obstacle_list = pygame.sprite.Group()
        self.player = player
        # Background image
        self.background = backgroundIMG

        #how far has the level been scrolled left or right?
        self.level_shift = 0
        self.level_limit = -1000

    #update everything on the level
    def update(self):
        self.obstacle_list.update()

    def draw(self, screen):
        #draw everthing on the level
        screen.blit(backgroundIMG, (0,0))
        self.obstacle_list.draw(screen)

    def shift_level(self, shift_x): 
        # Keep track of the shift amount
        self.level_shift += shift_x
 
        # Go through all the sprite lists and shift
        for obstacle in self.obstacle_list:
            obstacle.rect.x += shift_x
            
# Level one - creates all walls in level 1
class CarPark1(CarPark):

    def __init__(self, player):
        #make the walls using x, y, width and height from above)
        CarPark.__init__(self, player)

        self.level_limit = -1500

        #This is the list of walls in the form [x, y, width, height] width and height should be consistent for image size
        # screen dimension are x = 800 y = 480
        obstacle = [[50, 50, 500, 300],
                 [50, 50, 800, 200],
                 [50, 50, 1000, 300],
                 [50, 50, 1120, 180],
                 ]

        # Loop through the list to create the wall, then add to the list
        # for the level
        for item in obstacle:
            block = Obstacle(item[0], item[1])
            block.rect.x = item[2]
            block.rect.y = item[3]
            block.player = self.player
            self.obstacle_list.add(block)

# Level Two - creates all walls in level 2
class CarPark2(CarPark):
    def __init__(self, player):
        #make the walls using x, y, width and height from above)
        CarPark.__init__(self, player)

        self.level_limit = -1000

        #This is the list of walls in the form [x, y, width, height]
        obstacle = [[50, 50, 500, 450],
                 [50, 50, 800, 300],
                 [50, 50, 1000, 400],
                 [50, 50, 1120, 180],
                 ]

        # Loop through the list to create the wall, then add to the list
        # for the level
        for item in obstacle:
            block = Obstacle(item[0], item[1])
            block.rect.x = item[2]
            block.rect.y = item[3]
            block.player = self.player
            self.obstacle_list.add(block)

# Level Three - creates all walls in level 3
class CarPark3(CarPark):
    def __init__(self, player):
        #make the walls using x, y, width and height from above)
        CarPark.__init__(self, player)

        self.level_limit = -1000

        #This is the list of walls in the form [x, y, width, height, colour]
        obstacle = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 ]

        # Loop through the list to create the wall, then add to the list
        # for the level
        for item in obstacle:
            block = Obstacle(item[0], item[1])
            block.rect.x = item[2]
            block.rect.y = item[3]
            block.player = self.player
            self.obstacle_list.add(block)

# Main Program - using above classes #
def main():


    # set the game window title
    pygame.display.set_caption('Car Park Level: 1')

    # Create the player car object
    player = Player()

    # create all the Car Park levels
    CarPark_list = []
    CarPark_list.append(CarPark1(player))
    CarPark_list.append(CarPark2(player))
    CarPark_list.append(CarPark3(Player))

    #set the current level
    current_level_num = 0
    current_level = CarPark_list[current_level_num]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    #start the player at the start of the car park
    player.rect.x = 10
    player.rect.y = 220

    #add the player to the active sprite list
    active_sprite_list.add(player)
   
    #loop the game until the player hits the exit button
    done = False
    
        #main game loop    
    while not done:

        # process an event in the game
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True #game over or manaully closed

            # set code for using arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.go_up()
                if event.key == pygame.K_DOWN:
                    player.go_down()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stopX()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stopX()
                if event.key == pygame.K_UP and player.change_y < 0:
                    player.stopY()
                if event.key == pygame.K_DOWN and player.change_y > 0:
                    player.stopY()
        
        # update the player car
        active_sprite_list.update()

        # update items in the level
        current_level.update()

        # If player goes right, shift the world left
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_level(-diff)

        # If player gets near left, shift world right
        if player.rect.left < 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_level(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.level_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_num < len(CarPark_list)-1:
                current_level_num += 1
                pygame.display.set_caption('Car Park' + ' Level: ' + str(current_level_num+1))
                current_level = CarPark_list[current_level_num]
                player.level = current_level
            else:
                popupmsg("You finished the game!")
        # draw the screen
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        pygame.display.flip()
        clock.tick(60) #60 FPS
        #update the screen
        

    #pygame.quit()

loading()
