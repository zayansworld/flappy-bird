# to create the pipes at random heights
import random
import sys 
import pygame
from pygame.locals import *


# screen size and global variables
window_width = 600
window_height = 499

window = pygame.display.set_mode ((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
fps = 32
pipe = 'images/pipe.png'
bg = 'images/background.jpg'
bird ='images/bird.png'
base = 'images/base.jfif'

# The start of the game
if __name__ == "__main__":

    pygame.init()

    # for bird speed
    fps_clock  = pygame.time.Clock()

    pygame.display.set_caption('Definitely real Flappy Bird')


    # adding images
    game_images['scoreimages'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),        
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )

    game_images['flappybird'] = pygame.image.load(bird).convert_alpha()                  
    game_images['sea_level'] = pygame.image.load(base).convert_alpha()
    game_images['background'] = pygame.image.load(bg).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180), pygame.image.load(pipe).convert_alpha())
    
    print("Welcome to the definitely real Flappy Bird")
    print("press space or enter to start the game")


                
def createPipe():
    offset = window_height/3
    pipeHeight = game_images['pipeimage'][0].get_height()

    # generating random height of pipes
    y2 = offset + random.randrange( 0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))  
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        
        # upper Pipe
        {'x': pipeX, 'y': -y1},
        
        # lower Pipe
        {'x': pipeX, 'y': y2}  
    ]
    return pipe

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0: 
        return True

    # Checking if bird hits the upper pipe or not
    for pipe in up_pipes:    
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
            
    # Checking if bird hits the lower pipe or not
    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False

def flappygame():
    your_score = 0
    horizontal = int(window_width/5)
    vertical = int(window_width/2)
    ground = 0
    mytempheight = 100

    # Generating two pipes for blitting on window
    first_pipe = createPipe()
    second_pipe = createPipe()

    # List containing lower pipes
    down_pipes = [
        {'x': window_width+300-mytempheight,'y': first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),'y': second_pipe[1]['y']},
    ]

    # List Containing upper pipes 
    up_pipes = [
        {'x': window_width+300-mytempheight,'y': first_pipe[0]['y']},
        {'x': window_width+200-mytempheight+(window_width/2),'y': second_pipe[0]['y']},
    ]

    pipeVelX = -4 #pipe velocity along x

    bird_velocity_y = -9  # bird velocity
    bird_Max_Vel_Y = 10   
    bird_Min_Vel_Y = -8
    birdAccY = 1

    # velocity while flapping
    bird_flap_velocity = -8

    # It is true only when the bird is flapping
    bird_flapped = False  
    
    while True:

        # Handling the key pressing events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # This function will return true if the flappybird is crashed
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            return

        # check for your_score
        playerMidPos = horizontal + game_images['flappybird'].get_width()/2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
# Printing the score
                your_score += 1
                print(f"Your your_score is {your_score}")

        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY

        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about
        # to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))
        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))
        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0
        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1
        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num], (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
        # Refreshing the game window and displaying the score.
        pygame.display.update()
        # Set the fps
        fps_clock.tick(fps)

black=(0,0,0)
#initializing the birds position
while True:

    #setting co-ords for bird
    horizontal = int(window_width/5)
    vertical = int((window_height - game_images['flappybird'].get_height())/2)

    

    #for base
    ground = 0
    while True:
        for event in pygame.event.get():

            # clicking the "x" to leave
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()

                #exit game
                sys.exit()


            #I the user presses space or up key
            #start game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                flappygame()

                #if no key pressed nothing will happen
            else:
                window.blit(game_images['background'], (0, 0))
                window.blit(game_images['flappybird'], (horizontal, vertical))
                window.blit(game_images['sea_level'], (ground, elevation))

                font = pygame.font.SysFont("Comic Sans", 25)
                intro_text = font.render("Welcome to the definitely real Flappy Bird", True, black)
                start_text = font.render("press space or the up arrow to start the game", True, black)
                window.blit(intro_text,(220 - intro_text.get_width() // 3, 150 - intro_text.get_height() // 3))
                window.blit(start_text,(200 - intro_text.get_width() // 3, 200 - start_text.get_height() // 3))

                # Just Refresh the screen
                pygame.display.update()        

                    # set the rate of frame per second
                fps_clock.tick(fps)