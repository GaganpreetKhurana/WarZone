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


#different colours for health bar
gren=(0,200,0)
yelow=(100,100,0)
rde=(200,0,0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
blue = (32, 139, 185)
light_blue = (0, 0, 255)
pause = False

#for player 1
hit1=0
kill1=0
#for player 2
hit2=0
kill2=0
font=pygame.font.SysFont('comicsans',40,True)
time_left = int(300)


display_width = 1280
display_height = 640
gameDisplay = pygame.display.set_mode((display_width, display_height))
background_clouds = pygame.image.load("Background.png")
pygame.display.set_caption("WAR ZONE")
icon = pygame.image.load("log.png")
pygame.display.set_icon(icon)
img = pygame.image.load('guiii.png')
img1 = pygame.image.load('game1.png')
timer_button = pygame.image.load("Timer_button.png")
player_1 = pygame.image.load("Player_1.png")

pygame.display.update()

FPS = 30
clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

chatStr = ""
printchat = ""
printchatcheck = ""
FPScount = 0
time_str = ""
prev = ""
start_tick = 0


def message_to_screen(msg, color, y_displace=0, size="small"):
    textsurf, textRect = text_objects(msg, color, size)
    textRect.center = (640, 200 + y_displace)
    gameDisplay.blit(textsurf, textRect)


# to clear the text printed on the screen after 5 seconds
def chat_screen_update():
    gameDisplay.fill(white)
    gameDisplay.blit(background_clouds, [0, 0])
    button("Chat", 1180, 11, 90, 40, yellow, light_yellow)
    button("PAUSE", 1180, 55, 90, 40, red, light_red, action="paused")
    gameDisplay.blit(timer_button, [580, 10])
    text_to_button(time_str, black, 623, 24, 30, 30, 'medium')
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
    textRect.center = ((buttonx + (buttonwidth // 2)), (buttony + (buttonheight // 2)))
    gameDisplay.blit(textSurf, textRect)


def helps():
    helps = True
    while helps:
        gameDisplay.fill(green)
        message_to_screen("HELP", red, -100, "large")
        message_to_screen("SHOOT AND KILL THE ENEMY ", black, 0, "small")
        message_to_screen("PRESS SPACEBAR TO JUMP", black, 60, "small")
        message_to_screen("HEALTH BARS CONSTANTLY KEEPS A CHECK ON YOUR HEALTH AS WELL AS YOUR ENEMY'S HEALTH", black, 120, "small")
        message_to_screen("SCORE ON TOP LEFT CORNER SIGNIFIES RATIO OF TOTAL KILLS TO TOTAL DEATHS", black, 180, "small")
        message_to_screen("PRESS CHAT BUTTON TO SEND A MESSAGE ", black, 240, "small")

        cur = pygame.mouse.get_pos()  # it returns tuple of position of mouse on screen
        click = pygame.mouse.get_pressed()  # it returns a tuple of which mouse button is pressed whether left ceter or right for eg (1,0,0) means left is pressed
        if 130 + 150 > cur[0] > 130 and 535 + 50 > cur[1] > 535:
            # to lighten the button when mouse is over it
            pygame.draw.rect(gameDisplay, light_red, (130, 535, 150, 50))
            if click[0] == 1:  # that is on left click
                game_intro()

        else:
            pygame.draw.rect(gameDisplay, red, (130, 535, 150, 50))
        if 885 + 150 > cur[0] > 885 and 535 + 50 > cur[1] > 535:
            pygame.draw.rect(gameDisplay, light_yellow, (885, 535, 150, 50))
            if click[0] == 1:
                gameLoop()
        else:
            pygame.draw.rect(gameDisplay, yellow, (885, 535, 150, 50))

        # to put text in the button
        text_to_button("BACK", black, 130, 535, 150, 50)
        text_to_button("PLAY", black, 885, 535, 150, 50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        if click[0] == 1 and action is not None:

            if action == "quit":
                pygame.quit()
                quit()

            if action == "chat":
                chat_box()
            if action == "paused":
                pause = True
                paused()
            if action == "unpause":
                unpause()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    text_to_button(text, black, x, y, width, height)


def chat_box():
    chat_screen_update()
    pygame.display.update()

    current_string = []
    output = ""
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
        timer(start_tick)
        chat_screen_update()
        gameDisplay.blit(text, [20, 29])
        pygame.display.update()

        # Send Network Stuff- yahan opposition player ki position update karni padegi

    global chatStr
    chatStr = output


def chatting():
    global chatStr, printchat, printchatcheck, FPScount
    reply = send_data(chatStr)
    if reply != printchatcheck:
        printchat = reply
        FPScount = 0

    if FPScount <= 151: FPScount += 1

    if len(printchat) > 0 and FPScount == 1:
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
    pause = False


def paused():
    largetext = pygame.font.SysFont("comicsansms", 115)
    textsurf, textrect = text_objects("PAUSED", red, "large")
    textrect.center = (630, 200)
    gameDisplay.blit(textsurf, textrect)
    timeadd = 0
    global start_tick
    while pause:
        timeadd += 1
        if timeadd % 15 == 0:
            start_tick += 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # gameDisplay.fill(white)

        # message_to_screen("PAUSED",red,-100,"large")
        button("CONTINUE", 300, 372, 150, 50, red, light_red, action="unpause")
        button("QUIT", 842, 372, 150, 50, blue, light_blue, action="quit")

        pygame.display.update()
        clock.tick(15)
    else:
        chat_screen_update()


def game_over():
    global hit1
    global kill1
    global hit2
    global kill2
    game_over = True
    while game_over:


        gameDisplay.fill(white)
        gameDisplay.blit(img1, [0, 0])
        if int(hit1)>int(hit2):
            
            largetext = pygame.font.SysFont("comicsansms", 90)
            smalltext=pygame.font.SysFont("comicsansms",50)

            textsurf, textrect = text_objects("YOU WON", red, "large")
            textrect.center = (957,177)
            gameDisplay.blit(textsurf, textrect)
            textsurf1,textrect1=text_objects("PLAYER 1 :"+" + "+str(hit1)+"   - "+str(kill1),black,"small")
            textrect.center = (957,277)
            gameDisplay.blit(textsurf1, textrect1)
            textsurf2,textrect2=text_objects("PLAYER 2 :"+" + "+str(hit2)+"   - "+str(kill2),black,"small")
            textrect.center = (957,327)
            gameDisplay.blit(textsurf2, textrect2)

        elif int(hit1)<int(hit2):
            
            largetext = pygame.font.SysFont("comicsansms", 90)
            smalltext=pygame.font.SysFont("comicsansms",50)
            textsurf, textrect = text_objects("YOU LOSE", red, "large")
            textrect.center = (957,177)
            gameDisplay.blit(textsurf, textrect)
            textsurf1,textrect1=text_objects("PLAYER 1 :"+" + "+str(hit1)+"   - "+str(kill1),black,"small")
            textrect1.center = (957,327)
            gameDisplay.blit(textsurf1, textrect1)
            textsurf2,textrect2=text_objects("PLAYER 2 :"+" + "+str(hit2)+"   -"+str(kill2),black,"small")
            textrect2.center = (957,277)
            gameDisplay.blit(textsurf2, textrect2)
        else:
            
            largetext = pygame.font.SysFont("comicsansms", 90)
            smalltext=pygame.font.SysFont("comicsansms",50)
            textsurf, textrect = text_objects("TIE", red, "large")
            textrect.center = (957,177)
            gameDisplay.blit(textsurf, textrect)
            textsurf1,textrect1=text_objects("PLAYER 1 :"+" + "+str(hit1)+"   - "+str(kill1),black,"small")
            textrect1.center = (957,277)
            gameDisplay.blit(textsurf1, textrect1)
            textsurf2,textrect2=text_objects("PLAYER 2 :"+" + "+str(hit2)+"   - "+str(kill2),black,"small")
            textrect2.center = (957,327)
            gameDisplay.blit(textsurf2, textrect2)
        
        cur = pygame.mouse.get_pos()  # it returns tuple of position of mouse on screen
        click = pygame.mouse.get_pressed()  # it returns a tuple of which mouse button is pressed whether left ceter or right for eg (1,0,0) means left is pressed
        if 770 + 170 > cur[0] > 770 and 560 + 50 > cur[1] > 560:
            # to lighten the button when mouse is over it
            pygame.draw.rect(gameDisplay, light_red, (770, 560, 170, 50))
            if click[0] == 1:  # that is on left click
                gameLoop()
        else:
            pygame.draw.rect(gameDisplay, red, (770, 560, 170, 50))
        if 1010 + 170 > cur[0] > 1010 and 560 + 50 > cur[1] > 560:
            pygame.draw.rect(gameDisplay, light_yellow, (1010, 560, 170, 50))
            if click[0] == 1:
                pygame.quit()
                # to quit pygame
                quit() 
        else:
            pygame.draw.rect(gameDisplay, yellow, (1010, 560, 170, 50))

        # to put text in the button
        text_to_button("PLAY AGAIN", black, 770, 560, 170, 50)
        text_to_button("QUIT", black, 1010, 560, 170, 50)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        clock.tick(30)


def game_intro():
    intro = True
    while intro:

        gameDisplay.fill(white)
        gameDisplay.blit(img, [0, 0])
        cur = pygame.mouse.get_pos()  # it returns tuple of position of mouse on screen
        click = pygame.mouse.get_pressed()  # it returns a tuple of which mouse button is pressed whether left ceter or right for eg (1,0,0) means left is pressed
        if 842 + 150 > cur[0] > 842 and 291 + 50 > cur[1] > 291:
            # to lighten the button when mouse is over it
            pygame.draw.rect(gameDisplay, light_red, (842, 291, 150, 50))
            if click[0] == 1:  # that is on left click
                gameLoop()
        else:
            pygame.draw.rect(gameDisplay, red, (842, 291, 150, 50))
        if 842 + 150 > cur[0] > 842 and 372 + 50 > cur[1] > 372:
            pygame.draw.rect(gameDisplay, light_yellow, (842, 372, 150, 50))
            if click[0] == 1:
                helps()
        else:
            pygame.draw.rect(gameDisplay, yellow, (842, 372, 150, 50))
        if 842 + 150 > cur[0] > 842 and 456 + 50 > cur[1] > 456:
            pygame.draw.rect(gameDisplay, light_blue, (842, 456, 150, 50))
            if click[0] == 1:
                pygame.quit()
                # to quit pygame
                quit()
        else:
            pygame.draw.rect(gameDisplay, blue, (842, 456, 150, 50))

        # to put text in the button
        text_to_button("PLAY", black, 842, 291, 150, 50)
        text_to_button("HELP", black, 842, 372, 150, 50)
        text_to_button("QUIT", black, 842, 456, 150, 50)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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


def timer(start_tick):
    global time_left
    time_left = 10 - (pygame.time.get_ticks() - start_tick) / 1000
    
    
    min, sec = divmod(time_left, 60)
    if int(min)==int(0) and int(sec)==int(0):
        #print("helllllo")
        game_over()
        

    if sec < 10:
        sec = '0' + str(int(sec))
    else:
        sec = str(int(sec))
    global time_str, prev

    time_str = "0" + str(int(min)) + ":" + sec
    if time_str != prev:
        gameDisplay.blit(timer_button, [580, 10])
        text_to_button(time_str, black, 623, 24, 30, 30, 'medium')
        # chat_screen_update()
    prev = time_str
    #if time_str=="0":
     #   print("hii")
        


def player_draw(player_x, player_y, image, mirror=False):
    # pygame.draw.rect(gameDisplay, red, (player_x, player_y + 32, 32, 32))
    # pygame.draw.rect(gameDisplay, black, (player_x, player_y, 32, 16))
    if mirror:
        image = pygame.transform.flip(image, True, False)
    text=font.render('Score  '+ str(hit1) + " : " + str(kill1) ,1,(0,0,0))
    gameDisplay.blit(text,(0,20))
    gameDisplay.blit(image, [player_x - 16, player_y])


def obstacle_check(player_x, player_y, change_x, change_y, air_stay, direction, obstacle_x, obstacle_y, width, height):
    if obstacle_x <= player_x + change_x <= obstacle_x + width or obstacle_x <= player_x + 32 + change_x <= obstacle_x + width:
        if obstacle_y <= player_y + change_y <= obstacle_y + height or obstacle_y <= player_y + 64 + change_y <= obstacle_y + height or player_y <= obstacle_y < player_y + 64 or player_y <= obstacle_y + height <= player_y + 64:
            if direction["right"] and direction["up"] == 0 and direction["down"] == 0:
                change_x = obstacle_x - player_x - 32
            elif direction["left"] and direction["up"] == 0 and direction["down"] == 0:
                change_x -= obstacle_x + width - player_x
            elif direction["up"] == 0 and direction["down"] == 0:
                if abs(obstacle_x - player_x - 32) < abs(obstacle_x + width - player_x):
                    change_x = obstacle_x - player_x - 32
                else:
                    change_x = obstacle_x + width - player_x
            if direction["up"]:
                if obstacle_y < player_y + change_y < obstacle_y + height:
                    change_y = +8
                    change_x = 0
                    direction["up"] = 0
                    direction["down"] = 1
                    air_stay = 32 - air_stay - 2
            elif direction["down"]:
                if obstacle_y < player_y + 64 + change_y < obstacle_y + height:
                    change_y = obstacle_y - player_y - 64
                    direction["up"] = 0
                    direction["down"] = 0
                    air_stay = 0
                if air_stay != 0:
                    change_x = 0
    return change_x, change_y, air_stay, direction


def obstacles(playerX, playerY, x_change, y_change, air_stay_count, direction):
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 128, 352, 32, 32)  # plank 2
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 480, 512, 32)  # ground 1
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 512, 480, 32)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 544, 448, 32)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 576, 416, 32)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 608, 384, 32)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 224, 288, 192, 32)  # plank 3
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 256, 320, 128, 64)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 192, 128, 32)  # plank 1
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 224, 96, 64)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 288, 64, 32)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 320, 32, 32)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 544, 224, 128, 96)  # plank 4
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 800, 256, 128, 96)  # plank 5
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 640, 480, 192, 32)  # ground 2
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 672, 512, 128, 64)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 704, 576, 64, 32)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 960, 480, 320, 160)  # ground 3
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1120, 352, 32, 32)  # plank 7
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1056, 256, 32, 32)  # plank 6
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1152, 192, 128, 32)  # plank 8
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1184, 224, 96, 64)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1216, 288, 64, 32)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1248, 320, 32, 32)
    return x_change, y_change, air_stay_count, direction

def health_bars(player_health,enemy_health):
    if player_health >75:
        player_health_color=gren
    elif player_health >50:
        player_health_color=yelow
    else:
        player_health_color=rde

        
    if enemy_health >75:
        enemy_health_color=gren
    elif enemy_health >50:
        enemy_health_color=yelow
    else:
        enemy_health_color=rde
    pygame.draw.rect(gameDisplay,player_health_color,(430,25,player_health,30))
    pygame.draw.rect(gameDisplay,enemy_health_color,(750,25,enemy_health,30))
                     
    


def gameLoop():
    # to be able to modify direction

    # Event Handling
    gameDisplay.fill(white)
    gameDisplay.blit(background_clouds, [0, 0])
    gameExit = False

    player_health =100
    enemy_health=100

    direction = {"right": 0, "left": 0, "up": 0, "down": 0}
    playerX = 32
    playerY = 400
    air_stay_count = 0
    x_change = 0
    y_change = 0

    opponent_X = 1248
    opponent_Y = 400

    global start_tick
    start_tick = pygame.time.get_ticks()

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        keys = pygame.key.get_pressed()  # movements
        if keys[pygame.K_UP] and air_stay_count == 0 and direction["down"] == 0:
            direction["up"] = 1
            air_stay_count = 32
        if keys[pygame.K_LEFT]:
            x_change = -4
            direction["left"] = 1
            direction["right"] = 0
        if keys[pygame.K_RIGHT]:
            x_change = +4
            direction["left"] = 0
            direction["right"] = 1

        button("Chat", 1180, 11, 90, 40, yellow, light_yellow, action="chat")
        button("PAUSE", 1180, 55, 90, 40, red, light_red, action="paused")

        timer(start_tick)

        chatting()
        chatWithPlay()

        if air_stay_count > 16:  # for staying in air/loop
            air_stay_count -= 1
            y_change = -8
            direction["up"] = 1
            direction["down"] = 0
        elif air_stay_count <= 16:
            air_stay_count -= 1
            y_change = +8
            direction["down"] = 1
            direction["up"] = 0

        x_change, y_change, air_stay_count, direction = obstacles(playerX, playerY, x_change, y_change, air_stay_count,
                                                                  direction)  # obstacles
        if playerY + y_change >= 576:  # boundary checks
            air_stay_count = 0
            y_change = 0
            playerY = 576
            # game over
        elif playerY + y_change <= 0:
            y_change = +8
            direction["up"] = 0
            direction["down"] = 1
            air_stay_count = 32 - air_stay_count - 2
        if playerX + x_change <= 0:
            x_change = 0
            playerX = 0
        elif playerX + x_change + 32 >= 1280:
            x_change = 0
            playerX = 1280 - 32

        playerX += x_change
        playerY += y_change
        x_change = 0
        y_change = 0
        direction["down"] = 0
        direction["up"] = 0
        direction["right"] = 0
        direction["left"] = 0

        chat_screen_update()
        # send_confirmation=send_data(str(playerX)+":"+str(playerY))
        health_bars(player_health,enemy_health)
        player_draw(playerX, playerY, player_1)
        player_draw(opponent_X, opponent_Y, player_1, True)
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()


game_intro()
