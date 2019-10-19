import pygame
import time

from Network import network

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255,0,0)
light_grey = (220,220,220)

green = (0,155, 0)
light_green = (0,255,0)

yellow = (200,200,0)
light_yellow = (255,255,0)

gameDisplay = pygame.display.set_mode((1275,650))
background_clouds = pygame.image.load("CloudsFinal.jpg")
gameDisplay.fill(white)
gameDisplay.blit(background_clouds,[0,0])

pygame.draw.rect(gameDisplay, light_yellow, (0, 0, 1275, 60))

pygame.display.update()

FPS=30
clock=pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)


def text_objects(msg, color, size="small"):
    # the below statement added just to prevent error local variable used before refernce
    textSurface = smallfont.render(msg, True, color)

    if size == "small":
        textSurface = smallfont.render(msg, True, color)
    elif size == "meduim":
        textSurface = medfont.render(msg, True, color)
    elif size == "large":
        textSurface = largefont.render(msg, True, color)
    return textSurface, textSurface.get_rect()


def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight,size="small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)),(buttony+(buttonheight/2)))
    gameDisplay.blit(textSurf,textRect)


def button(text,x,y,width,height,inactive_color,active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # click has tuple containing 3 elements. first one left click,second one mouse scroll, third one right click

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay,active_color,(x,y,width,height))
        if click[0] == 1 and action != None:

            if action=="quit":
                pygame.quit()
                quit()

            if action=="chat":
                chat_box()

    else:
        pygame.draw.rect(gameDisplay,inactive_color,(x,y,width,height))

    text_to_button(text,black,x,y,width,height)

def chat_box():

    pygame.display.update()

    current_string = []

    writing = True
    while writing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    current_string = current_string[0:-1]
                elif event.key == pygame.K_RETURN:
                    writing = False
                    break
                elif event.key == pygame.K_MINUS:
                    current_string.append("_")
                elif event.key <= 127:
                    current_string.append(chr(event.key))

            output = "".join(current_string)
            text = smallfont.render(output, True, black)
            gameDisplay.blit(text, [3, 29])
            pygame.display.update()


def gameLoop():
    # to be able to modify direction

    # Event Handling
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                pass


        button("Chat",1200,11,60,40,red,light_red)
        pygame.display.update()

        clock.tick(FPS)


    pygame.quit()
    quit()

gameLoop()
