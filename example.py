import pygame

# colour variables
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
PURPLE = (255,0,255)

# This class represents the walls/barriers in the game #
class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color):
        super().__init__()

        # Make a blue wall, using dimensions provided in the function
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make the player start in the top left corner
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# This class represents the character that the player controls
class Player(pygame.sprite.Sprite):

    # Speed vector
    change_x = 0
    change_y = 0

    def __init__(self, x, y):
       super().__init__()

       # Set height and width
       self.image = pygame.Surface([15,15])
       self.image.fill(WHITE) #replace this with image when working

       # Make player start at top left corner
       self.rect = self.image.get_rect()
       self.rect.y = y
       self.rect.x = x

    # change speed of the player, with a press of arrow keys
    def changespeed(self, x,y):
        self.change_x += x
        self.change_y += y

    #Find a new position for the player
    def move(self, walls):

        #Move left/right
        self.rect.x += self.change_x

        #did this make the player hit the wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            #If moving right, set right side to the left side of the item hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if moving left, do opposite
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        #did this make the player hit the wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            #If moving right, set right side to the top/bottom of the item hit
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                # Otherwise if moving left, do opposite
                self.rect.top = block.rect.bottom

# Base class for all car-parks #
class CarPark(object):
    #Each car-park has a list of walls, and of enemy objects
    wall_list = None #start empty to initiate
    enemy_objects = None 

    #construct to create the lists of walls and enemies
    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_objects = pygame.sprite.Group()

# Level one - creates all walls in level 1
class CarPark1(CarPark):
    def __init__(self):
        #make the walls using x, y, width and height from above)
        super().__init__()

        #This is the list of walls in the form [x, y, width, height]
        walls = [[0, 0, 20, 250, WHITE],
                 [0, 350, 20, 250, WHITE],
                 [780, 0, 20, 250, WHITE],
                 [780, 350, 20, 250, WHITE],
                 [20, 0, 760, 20, WHITE],
                 [20, 580, 760, 20, WHITE],
                 [390, 50, 20, 500, BLUE]
                ]

        # Loop through the list to create the wall, then add to the list
        # for the level
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

# Level Two - creates all walls in level 2
class CarPark2(CarPark):
    def __init__(self):
        #make the walls using x, y, width and height from above)
        super().__init__()

        #This is the list of walls in the form [x, y, width, height]
        walls = [[0, 0, 20, 250, RED],
                 [0, 350, 20, 250, RED],
                 [780, 0, 20, 250, RED],
                 [780, 350, 20, 250, RED],
                 [20, 0, 760, 20, RED],
                 [20, 580, 760, 20, RED],
                 [190, 50, 20, 500, GREEN],
                 [590, 50, 20, 500, GREEN]
                ]

        # Loop through the list to create the wall, then add to the list
        # for the level
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

# Level Three - creates all walls in level 3
class CarPark3(CarPark):
    def __init__(self):
        #make the walls using x, y, width and height from above)
        super().__init__()

        #This is the list of walls in the form [x, y, width, height]
        walls = [[0, 0, 20, 250, PURPLE],
                 [0, 350, 20, 250, PURPLE],
                 [780, 0, 20, 250, PURPLE],
                 [780, 350, 20, 250, PURPLE],
                 [20, 0, 760, 20, PURPLE],
                 [20, 580, 760, 20, PURPLE]
                ]

        # Loop through the list to create the wall, then add to the list
        # for the level
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        #create 'random' red walls at the below x and y coordination for position
        for x in range(100, 800, 100):
            for y in range(50, 451, 300):
                wall = Wall(x, y, 20, 200, RED)
                self.wall_list.add(wall)
        #create 'random' white walls at the below x and y coordination for position
        for x in range(150, 700, 100):
            wall = Wall(x, 200, 20, 200, WHITE)
            self.wall_list.add(wall)

# Main Program - using above classes #
def main():

    #Initiate pygame library
    pygame.init()

    #create an 800x600 pixel screen
    screen = pygame.display.set_mode([800, 600])

    # set the game window title
    pygame.display.set_caption('Car Park')

    # Create the player car object
    player = Player (50,50)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    # create an empty list of carPark levels to fill with levels below
    carParks = []

    #create the Car Parks using above pre-defined classes
    # level 1
    carPark = CarPark1()
    carParks.append(carPark)

    # level 2
    carPark = CarPark2()
    carParks.append(carPark)

    # level 3
    carPark = CarPark3()
    carParks.append(carPark)

    #current level
    current_carPark_no = 0
    current_carPark = carParks[current_carPark_no]

    # initialise a clock to set game speed/FPS
    clock = pygame.time.Clock()

    # game running logic
    done = False
    
    while not done:

        # process an event in the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True #game over or manaully closed

        # set code for using arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5)
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -5)

        # game logic

        player.move(current_carPark.wall_list)

        # is the player moving out of the carPark?
        if player.rect.x < -15: #left side of screen
            if current_carPark_no == 0:
                current_carPark_no = 2
                current_carPark = carParks[current_carPark_no]
                player.rect.x = 790 #edge of screen
            elif current_carPark_no == 2:
                current_carPark_no = 1
                current_carPark = carParks[current_carPark_no]
                player.rect.x = 790 #edge of screen
            else:
                current_carPark_no = 0
                current_carPark = carParks[current_carPark_no]
                player.rect.x = 790 #edge of screen

        if player.rect.x > 801: #right side of screen
            if current_carPark_no == 0:
                current_carPark_no = 1
                current_carPark = carParks[current_carPark_no]
                player.rect.x = 0 #edge of screen
            elif current_carPark_no == 1:
                current_carPark_no = 2
                current_carPark = carParks[current_carPark_no]
                player.rect.x = 0 #edge of screen
            else:
                current_carPark_no = 0
                current_carPark = carParks[current_carPark_no]
                player.rect.x = 0 #edge of screen

        # draw the screen
        screen.fill(BLACK)

        #draw characters and walls on the screen
        movingsprites.draw(screen)
        current_carPark.wall_list.draw(screen)

        #update the screen
        pygame.display.flip()

        clock.tick(60) #60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()