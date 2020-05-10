import pygame, random
import tkinter as tk
from tkinter import ttk

# colour variables
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
PURPLE = (255,0,255)

# screen variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# font variables
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

# image variables
carIMG = pygame.image.load("Game-Assignment\media\car.png")
obstacleIMG = pygame.image.load("Game-Assignment\media/blueCar.png")
backgroundIMG = pygame.image.load("Game-Assignment\media/background1.jpg")

# This class represents the character that the player controls
class Player(pygame.sprite.Sprite):

    def __init__(self):

       super().__init__()

       # Set height and width
       width = 40
       height = 60
       self.image = pygame.Surface([width, height])
       self.image = carIMG
       self.rect = self.image.get_rect()

       self.change_x = 0
       self.change_y = 0

       self.level = None

    def update(self, obstacle_list):

        # move let and right
        self.rect.x += self.change_x

        #did this make the player hit the wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.level.obstacle_list, False)
        for block in block_hit_list:
            #If moving right, set right side to the left side of the item hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if moving left, do opposite
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        #did this make the player hit the wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.level.obstacle_list, False)
        for block in block_hit_list:
            #If moving right, set right side to the top/bottom of the item hit
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                # Otherwise if moving left, do opposite
                self.rect.top = block.rect.bottom

                #stop moving up
                self.change_y = 0

                if isinstance(block, MovingObstacle):
                    self.rect.x += block.change_x

        # define player controlled movement
    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6
        
    def go_up(self):
        self.change_y = -6
        
    def go_down(self):
        self.change_y = 6

    def stopX(self):
        self.change_x = 0

    def stopY(self):
        self.change_y = 0


# This class represents the walls/barriers in the game #
class Obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image = obstacleIMG
        self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x

# class to define an obstacle
class MovingObstacle(Obstacle):

    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None
    level = None

    def update(self):
        #move the platform

        #move obstalce left/right
        self.rect.x += self.change_x

        #see if we hit the player car
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # the obstacle hit the player
            popupmsg("you hit an obstacle!")
            # the obstacle hit the player, so kill the player
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        #move obstalce up/down
        self.rect.y += self.change_y

        #see if we hit the player car
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # the obstacle hit the player
            popupmsg("you hit an obstacle!")
            # the obstacle hit the player, so kill the player
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.boundary_bottom

# Base class for all car-parks #
class CarPark(object):

    obstacle_list = None
    #construct to create the lists of walls and enemies
    def __init__(self, player):
        self.obstacle_list = pygame.sprite.Group()
        self.enemy_objects = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = backgroundIMG

    #update everything on the level
    def update(self):
        self.obstacle_list.update()
        self.enemy_objects.update()

    def draw(self, screen):
        #draw everthing on the level
        screen.fill(GREEN)

        self.obstacle_list.draw(screen)
        self.enemy_objects.draw(screen)


# Level one - creates all walls in level 1
class CarPark1(CarPark):

    def __init__(self, player):
        #make the walls using x, y, width and height from above)
        CarPark.__init__(self, player)

        #This is the list of walls in the form [x, y, width, height]
        obstacle = [[0, 0, 20, 250],
                 [0, 350, 20, 250],
                 [780, 0, 20, 250],
                 [780, 350, 20, 250],
                 ]

        # Loop through the list to create the wall, then add to the list
        # for the level
        for item in obstacle:
            block = Obstacle(item[0], item[1], item[2], item[3])
            self.obstacle_list.add(block)

        # add a moving obstacle
        block = MovingObstacle(70, 40, 250, 250)
        block.rect.x = 300
        block.rect.y = 300
        block.boundary_left = 400
        block.boundary_right = 400
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.obstacle_list.add(block)

        # add a moving obstacle
        block = MovingObstacle(0, 350, 250, 250)
        block.rect.x = 100
        block.rect.y = 100
        block.boundary_left = 400
        block.boundary_right = 400
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.obstacle_list.add(block)

# Level Two - creates all walls in level 2
class CarPark2(CarPark):
    def __init__(self, player):
        #make the walls using x, y, width and height from above)
        CarPark.__init__(self, player)

        #This is the list of walls in the form [x, y, width, height]
        obstacle = [[0, 0, 20, 250],
                 [0, 350, 20, 250],
                 [780, 0, 20, 250],
                 [780, 350, 20, 250],
                 ]

        # Loop through the list to create the wall, then add to the list
        # for the level
        for item in obstacle:
            block = Obstacle(item[0], item[1], item[2], item[3])
            self.obstacle_list.add(block)

        # add a moving obstacle
        block = MovingObstacle(0, 350, 250, 250)
        block.rect.x = 100
        block.rect.y = 100
        block.boundary_left = 400
        block.boundary_right = 400
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.obstacle_list.add(block)

        # add another moving obstacle
        block = MovingObstacle(70, 70, 250, 250)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 400
        block.boundary_bottom = 400
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.obstacle_list.add(block)

# Level Three - creates all walls in level 3
class CarPark3(CarPark):
    def __init__(self, player):
        #make the walls using x, y, width and height from above)
        CarPark.__init__(self, player)

        #This is the list of walls in the form [x, y, width, height, colour]
        obstacle = [[50, 50, 500, 550],
                 [50, 50, 800, 400],
                 [50, 50, 1000, 500],
                 [50, 50, 1200, 280],
                 [50, 50, 700, 300],
                 [50, 50, 800, 400],
                 [50, 50, 1200, 280],
                 ]

        # Loop through the list to create the wall, then add to the list
        # for the level
        for item in obstacle:
            block = Obstacle(item[0], item[1], item[2], item[3])
            self.obstacle_list.add(block)

        # add a moving obstacle
        block = MovingObstacle(70, 40, 250, 250)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 400
        block.boundary_right = 400
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.obstacle_list.add(block)

        # add another moving obstacle
        block = MovingObstacle(70, 70, 250, 250)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 400
        block.boundary_bottom = 400
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.obstacle_list.add(block)

        # add a moving obstacle
        block = MovingObstacle(60, 30, 250, 250)
        block.rect.x = 1200
        block.rect.y = 300
        block.boundary_left = 400
        block.boundary_right = 400
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.obstacle_list.add(block)

# Main Program - using above classes #
def main():

    #Initiate pygame library
    pygame.init()

    #create an 800x600 pixel screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # set the game window title
    pygame.display.set_caption('Car Park')

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

    player.rect.x = 40
    player.rect.y = 60
    active_sprite_list.add(player)

    #loop the game until the player hits the exit button
    done = False
    
    # initialise a clock to set game speed/FPS
    clock = pygame.time.Clock()

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
       # active_sprite_list.update()

        # update items in the level
       # current_level.update()

        player.update(current_level.obstacle_list)

        # is the player moving out of the carPark?
        if player.rect.x < -15: #left side of screen
            if current_level_num == 0:
                current_level_num = 2
                current_level = CarPark_list[current_level_num]
                player.rect.x = 790 #edge of screen
            elif current_level_num == 2:
                current_level_num = 1
                current_level = CarPark_list[current_level_num]
                player.rect.x = 790 #edge of screen
            else:
                current_level_num = 0
                current_level = CarPark_list[current_level_num]
                player.rect.x = 790 #edge of screen

        if player.rect.x > 801: #right side of screen
            if current_level_num == 0:
                current_level_num = 1
                current_level = CarPark_list[current_level_num]
                player.rect.x = 0 #edge of screen
            elif current_level_num == 1:
                current_level_num = 2
                current_level = CarPark_list[current_level_num]
                player.rect.x = 0 #edge of screen
            else:
                current_level_num = 0
                current_level = CarPark_list[current_level_num]
                player.rect.x = 0 #edge of screen

        # draw the screen
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(60) #60 FPS

        #update the screen
        pygame.display.flip()

        

    pygame.quit()

if __name__ == "__main__":
    main()