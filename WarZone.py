import pygame
import time

from Network import network

pygame.init()

net = network()

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)
light_grey = (220, 220, 220)

green = (0, 155, 0)
light_green = (0, 255, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
blue=(32,139,185)
light_blue=(0,0,255)
pause=False

gameDisplay = pygame.display.set_mode((1280, 640))
background_clouds = pygame.image.load("Background.png")
pygame.display.set_caption("WAR ZONE")
icon=pygame.image.load("log.png")
pygame.display.set_icon(icon)
img=pygame.image.load('guiii.png')

pygame.display.update()

FPS = 30
clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

chatStr = ""
printchat = ""
printchatcheck = ""
FPScount=0

def message_to_screen(msg,color,y_displace=0,size="small"):
    
    textsurf, textRect=text_objects(msg,color,size)
    textRect.center=(640,200+y_displace)
    gameDisplay.blit(textsurf,textRect)


# to clear the text printed on the screen after 5 seconds
def chat_screen_update():
    gameDisplay.fill(white)
    gameDisplay.blit(background_clouds, [0, 0])
    button("Chat", 1200, 11, 60, 40, yellow, light_yellow)

    # bande bhi yahan update honge taaki purana text overwrite ho jaaye


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


def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth / 2)), (buttony + (buttonheight / 2)))
    gameDisplay.blit(textSurf, textRect)


def helps():
    helps=True
    while helps:
        gameDisplay.fill(green)
        message_to_screen("HELP",red,-100,"large")
        message_to_screen("SHOOT AND KILL THE ENEMY ",black,0,"small")
        message_to_screen("PRESS SPACEBAR TO JUMP",black,80,"small")
        message_to_screen("PRESS CHAT BUTTON TO SEND A MESSAGE ",black,160,"small")
        
        
        cur=pygame.mouse.get_pos()#it returns tuple of position of mouse on screen
        click=pygame.mouse.get_pressed()#it returns a tuple of which mouse button is pressed whether left ceter or right for eg (1,0,0) means left is pressed
        if 130+150>cur[0]>130 and 535+50>cur[1]>535:
            #to lighten the button when mouse is over it
            pygame.draw.rect(gameDisplay,light_red,(130,535,150,50))
            if click[0]==1:#that is on left click
                game_intro()
                
        else:
            pygame.draw.rect(gameDisplay,red,(130,535,150,50))
        if 885+150>cur[0]>885 and 535+50>cur[1]>535:
            pygame.draw.rect(gameDisplay,light_yellow,(885,535,150,50))
            if click[0]==1:
                gameLoop()
        else:
            pygame.draw.rect(gameDisplay,yellow,(885,535,150,50))


        #to put text in the button 
        text_to_button("BACK",black,130,535,150,50)
        text_to_button("PLAY",black,885,535,150,50)
        pygame.display.update()
        for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    pygame.quit()
                    quit()

        clock.tick(15)


def button(text, x, y, width, height, inactive_color, active_color, action=None):
    global pause
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # click has tuple containing 3 elements. first one left click,second one mouse scroll, third one right click

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:

            if action == "quit":
                pygame.quit()
                quit()

            if action == "chat":
                chat_box()
            if action=="paused":
                pause=True
                paused()
            if action=="unpause":
                unpause()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    text_to_button(text, black, x, y, width, height)


def chat_box():
    chat_screen_update()
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
            chat_screen_update()
            gameDisplay.blit(text, [20, 29])
            pygame.display.update()

        # Send Network Stuff- yahan opposition player ki position update karni padegi

    global chatStr
    chatStr = output

def chating():
    global chatStr, printchat, printchatcheck,FPScount
    reply = send_data(chatStr)
    if reply != printchatcheck:
        printchat = reply
        FPScount=0

    if FPScount<=151: FPScount += 1

    if len(printchat) > 0 and FPScount==1:
        text = smallfont.render(printchat, True, black)
        printchatcheck = printchat

        gameDisplay.blit(text, [20, 29])
        pygame.display.update()

        # pygame.time.wait(5000)
        # chatStr = ""
        # printchat = ""
        # # print("DONE")
        # chat_screen_update()


def send_data(output):
    """
    Send position to server
    :return: None
    """
    data = str(net.id) + ":" + output
    reply = net.send(data)

    return reply[2:]

def unpause():
    global pause
    pause=False
    

def paused():
    largetext=pygame.font.SysFont("comicsansms",115)
    textsurf,textrect=text_objects("PAUSED",red,"large")
    textrect.center=((630),(200))
    gameDisplay.blit(textsurf,textrect)
    
    while pause:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        #gameDisplay.fill(white)
        #message_to_screen("PAUSED",red,-100,"large")
        button("CONTINUE",300,372,150,50,red,light_red,action="unpause")
        button("QUIT",842,372,150,50,blue,light_blue,action="quit")
        
        pygame.display.update()
        clock.tick(15)
    else:
        chat_screen_update()


def game_intro():
    intro=True
    while intro:
    
        
        gameDisplay.fill(white)
        gameDisplay.blit(img,[0,0])
        cur=pygame.mouse.get_pos()#it returns tuple of position of mouse on screen
        click=pygame.mouse.get_pressed()#it returns a tuple of which mouse button is pressed whether left ceter or right for eg (1,0,0) means left is pressed
        if 842+150>cur[0]>842 and 291+50>cur[1]>291:
            #to lighten the button when mouse is over it
            pygame.draw.rect(gameDisplay,light_red,(842,291,150,50))
            if click[0]==1:#that is on left click
                gameLoop()
        else:
            pygame.draw.rect(gameDisplay,red,(842,291,150,50))
        if 842+150>cur[0]>842 and 372+50>cur[1]>372:
            pygame.draw.rect(gameDisplay,light_yellow,(842,372,150,50))
            if click[0]==1:
                helps()
        else:
            pygame.draw.rect(gameDisplay,yellow,(842,372,150,50))
        if 842+150>cur[0]>842 and 456+50>cur[1]>456:
            pygame.draw.rect(gameDisplay,light_blue,(842,456,150,50))
            if click[0]==1:
                pygame.quit()
                #to quit pygame
                quit()
        else:
            pygame.draw.rect(gameDisplay,blue,(842,456,150,50))
        

        #to put text in the button 
        text_to_button("PLAY",black,842,291,150,50)
        text_to_button("HELP",black,842,372,150,50)
        text_to_button("QUIT",black,842,456,150,50)
        
        pygame.display.update()
        for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    pygame.quit()
                    quit()
        clock.tick(30)

def chatWithPlay():
    global chatStr, printchat, printchatcheck, FPScount

    if FPScount == 150:
        chatStr = ""
        printchat = ""
        # print("DONE")
        chat_screen_update()


def gameLoop():
    # to be able to modify direction

    # Event Handling
    gameDisplay.fill(white)
    gameDisplay.blit(background_clouds,[0,0])
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                pass

        button("Chat", 1200, 11, 60, 40, yellow, light_yellow, action="chat")
        button("PAUSE",1180,55,80,40,red,light_red,action="paused")
        chating()
        chatWithPlay()

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()

