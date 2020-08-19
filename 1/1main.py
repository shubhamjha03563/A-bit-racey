import pygame
import time
import random

pygame.init() #initiates pygame and all modules that come with it(compulsory)

crash_sound = pygame.mixer.Sound("crash.wav")
pygame.mixer.music.load("backmusic.mp3")

display_width = 800
display_height = 600
black = (0, 0, 0)  # R G B 
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

block_color = (53, 115, 255) #R G B
car_width = 72
gameDisplay = pygame.display.set_mode((display_width, display_height)) #size of the game window
pygame.display.set_caption('A bit Racey') #game title
clock = pygame.time.Clock() #game clock
carImg = pygame.image.load('racecar.jpg') #load image
pause = False

def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Dodged: "+ str(count), True, black)
    gameDisplay.blit(text, (0, 0))

def things(thingx, thingy, thingw, thingh, color) :
    #draws a block(rectangle) on the game screen
    pygame.draw.rect(gameDisplay, block_color, [thingx, thingy, thingw, thingh])

def car(x, y):
    gameDisplay.blit(carImg, (x, y)) #display image
    '''blit() draws the background stuff (here: carImg) that we want to display and /
    other parameter(here:(x, y)) is where to show the image.'''
    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect() #gets the rectangle(can be used to position the text(line 49))

def crash():

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    largeText = pygame.font.SysFont("comicsansms", 115)
    textSurf, textRect = text_objects("You Crashed", largeText)
    textRect.center = ((display_width / 2), (display_height / 2))#Places rectangle at the center     
    gameDisplay.blit(textSurf, textRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)
        button("Play Again", 150, 450, 100, 50, green, bright_green, game_loop) #here 'game_loop' is an object
        button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)
        pygame.display.update()
        clock.tick(15)

def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos() #gets live position of mouse
    click = pygame.mouse.get_pressed() #gets clicked position
    
    #coordinates of mouse-> (mouse[0], mouse[1])
    if x+w > mouse[0] > x and y+h > mouse[1] >y:
        #pygame.draw.rect(Surface, color, (x, y, width, height))
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h)) #draws a rectangle
        #'click[0]' indicates left mouse button and its value '1' indicates that mouse is clicked
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
 
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg,smallText )
    textRect.center = ((x+(w/2)), y+(h/2))
    gameDisplay.blit(textSurf, textRect)

def quit_game():
    pygame.quit()
    quit()

def unpause():
    global pause
    pygame.mixer.music.unpause()  
    pause = False

def paused():
    pygame.mixer.music.pause()

    largeText = pygame.font.SysFont("comicsansms", 115)
    textSurf, textRect = text_objects("Paused", largeText)
    textRect.center = ((display_width / 2), (display_height / 2))#Places rectangle at the center     
    gameDisplay.blit(textSurf, textRect)
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)
        button("Continue", 150, 450, 100, 50, green, bright_green, unpause) #here 'game_loop' is an object
        button("Quit!", 550, 450, 100, 50, red, bright_red, quit_game)
        pygame.display.update()
        clock.tick(15)

def game_intro():
    
    intro = False
    while not intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms", 115)
        textSurf, textRect = text_objects("A bit Racey", largeText)
        textRect.center = ((display_width / 2), (display_height / 2))#Places rectangle at the center     
        gameDisplay.blit(textSurf, textRect)
        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop) #here 'game_loop' is an object
        button("Quit!", 550, 450, 100, 50, red, bright_red, quit_game)
        pygame.display.update()
        clock.tick(15)

def game_loop():
    
    global pause
    pygame.mixer.music.play(-1) #-1 means playing infinitely   

    #NOTE: Origin is at the top left corner of the game window
    x = (display_width * 0.37) #Increases to the right
    y = (display_height * 0.72) #Increases downwards
    x_change = 0 #change in horizontal position of car

    #Initialising the block's position(starting values)
    '''random.randrange() selects random options available between the parameters provided /
    but when loop repeats its value of 'thing_startx' remains same, thus we need to redefine its value each time(line 135)'''
    thing_startx = random.randrange(100, 700) #horizontal position of block
    thing_starty = -600 #horizontal position of block
    '''If 'thing_starty = 0', then user won't get any time to be ready,thus we initialise the block pretty early/
    but after the first block, other blocks appear immediately(line 132)'''
    thing_speed = 2 #speed of block
    thing_height = 100 #Size of block
    thing_width = 100
    dodged = 0 #no.of blocks dodged
    
    gameExit = False
    while not gameExit:

        '''pygame.event.get() gets any event that happens(eg > mouse_click, key_press, cursor_movement) and /
        creates a list of events that have happened(per frames per sec); i.e; generally only one thing's gonna happen.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #when any key is pressed
            if event.type == pygame.KEYDOWN:
                #when left arrow key is pressed
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            #when any key is released after pressing
            if event.type == pygame.KEYUP:
                #when left or right arrow key is released(after pressing)
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    x_change = 0
                    
        x += x_change
        if x > display_width - car_width or x < 0:
            x -= x_change
        gameDisplay.fill(white) #paints over the whole game window
        
        #things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, black)

        thing_starty += thing_speed #Making the blocks move
        car(x, y) # #Coordinates of image (x -> leftmost position / y -> uppermost position)
        things_dodged(dodged) #No.of blocks dodged

        #if car touches horizontal boundaries

        #if a block passes through
        if thing_starty > display_height:
            thing_starty = 0 - thing_height #After a block has passed, another block shows up immediately
            thing_startx = random.randrange(0, 700) #Redefining intial value of 'thing_startx'
            dodged += 1 #No.of blocks dodged
            thing_speed += 0.2 #increases incoming block's speed after a block has passed
            thing_width += (dodged * 1.2)
        
        ''' CRASH RULES'''
        #when bottom of block reaches top of car 
        if y < thing_starty + thing_height:
            #if leftmost or rightmost position of car touches the bottom of block anywhere
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                crash()
                
        '''pygame.display.update() -> if parameter not provided: updates everything and /
        if parameter provided: updates just the parameter '''
        pygame.display.update() 
        '''pygame.display.flip() can be used instead but it can't take any parameter /
        and thus it updates everything.'''
        
        clock.tick(150) #Moving the frame(speed of car:60 frames per secm)

game_intro()
game_loop()
pygame.quit()#stops pygame from running
quit()#pops up a quit question in python IDLE
