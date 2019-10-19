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

pygame.display.update()

FPS=30
clock=pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms",20)

def chat_box():

    pygame.draw.rect(gameDisplay,black,(0,0,1275,58))
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

            pygame.draw.rect(gameDisplay, light_grey, (2, 2, 1271, 26))
            pygame.draw.rect(gameDisplay,light_grey,(2,30,1271,26))
            output = "".join(current_string)
            text = smallfont.render(output, True, black)
            gameDisplay.blit(text, [3, 1])
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
                if event.key == pygame.K_t:
                    chat_box()


        pygame.display.update()

        clock.tick(FPS)


    pygame.quit()
    quit()

gameLoop()