import pygame
import time

from Network import network

count = 0
pygame.init()

net = network()

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)
light_grey = (220, 220, 220)

green = (0, 155, 0)
light_green = (0, 255, 0)

# different colours for health bar
gren = (0, 200, 0)
yelow = (100, 100, 0)
rde = (200, 0, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
blue = (32, 139, 185)
light_blue = (0, 0, 255)
pause = False

# for player 1
hit1 = 0
kill1 = 0
# for player 2
hit2 = 0
kill2 = 0
font = pygame.font.SysFont('comicsans', 40, True)
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
player_1 = pygame.image.load("idle1.png")
bullet_right = pygame.image.load("bulletright.png")
bullet_right = pygame.transform.smoothscale(bullet_right, (12, 12))
walkright = [pygame.image.load('Run (1).png'),
             pygame.image.load('Run (2).png'),
             pygame.image.load('Run (3).png'),
             pygame.image.load('Run (4).png'),
             pygame.image.load('Run (5).png'),
             pygame.image.load('Run (6).png'),
             pygame.image.load('Run (7).png'),
             pygame.image.load('Run (8).png')]
walkright1 = [pygame.image.load('Run (1).png'),
              pygame.image.load('Run (2).png'),
              pygame.image.load('Run (3).png'),
              pygame.image.load('Run (4).png'),
              pygame.image.load('Run (5).png'),
              pygame.image.load('Run (6).png'),
              pygame.image.load('Run (7).png'),
              pygame.image.load('Run (8).png')]

walkleft = [pygame.image.load('runss1.png'),
            pygame.image.load('runss2.png'),
            pygame.image.load('runss3.png'),
            pygame.image.load('runss4.png'),
            pygame.image.load('runss5.png'),
            pygame.image.load('runss6.png'),
            pygame.image.load('runss7.png'),
            pygame.image.load('runss8.png')]
walkleft1 = [pygame.image.load('runss1.png'),
             pygame.image.load('runss2.png'),
             pygame.image.load('runss3.png'),
             pygame.image.load('runss4.png'),
             pygame.image.load('runss5.png'),
             pygame.image.load('runss6.png'),
             pygame.image.load('runss7.png'),
             pygame.image.load('runss8.png')]
walk = 0
left = False
right = False
jump = False
standr = True
standl = False

pygame.display.update()

FPS = 32
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
timer_count = 0

player_health = 100
enemy_health = 100
playerX = 32
playerY = 400
opponent_X = 1248
opponent_Y = 400
opponent_X_old = 1248
opponent_X_change = 0
opponent_Y_old = 400
opponent_Y_change = 0
# size is 24X24
player_bullet_x = 1285  # player_bullet_x is X coordinate of players bullet
player_bullet_y = 645  # player_bullet_y is Y coordinate of player's bullet
enemy_bullet_x = 1285
enemy_bullet_y = 645
bullet_direction_player = 'r'  # bullet_direction_player values 'r','l'
bullet_direction_enemy = 'l'
player_direction = 'r'
enemy_direction = 'l'
air = False

if net.id == '1':
    playerX = 1248
    playerY = 400
    opponent_X = 32
    opponent_Y = 400
    player_direction = 'l'
    enemy_direction = 'r'
    bullet_direction_enemy = 'r'
    bullet_direction_player = 'l'

walk1 = 0
left1 = False
right1 = False
jump1 = False
standr1 = False
standl1 = True


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
    text = smallfont.render(printchat, True, black)
    gameDisplay.blit(text, [20, 60])

    text_to_button(time_str, black, 623, 24, 30, 30, 'medium')
    health_bars(player_health, enemy_health)
    player_draw(playerX, playerY, player_1)
    player_draw(opponent_X, opponent_Y, player_1, True)
    gameDisplay.blit(bullet_right, (enemy_bullet_x, enemy_bullet_y))

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
        message_to_screen("HEALTH BARS CONSTANTLY KEEPS A CHECK ON YOUR HEALTH AS WELL AS YOUR ENEMY'S HEALTH", black,
                          120, "small")
        message_to_screen("SCORE ON TOP LEFT CORNER SIGNIFIES RATIO OF TOTAL KILLS TO TOTAL DEATHS", black, 180,
                          "small")
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
        gameDisplay.blit(text, [20, 60])
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

        gameDisplay.blit(text, [20, 60])
        pygame.display.update()

        # pygame.time.wait(5000)
        # chatStr = ""
        # printchat = ""
        # # print("DONE")
        # chat_screen_update()


def send_data(output):
    """
    Send position to server
    return: None
    """
    global playerX, playerY, opponent_X, opponent_Y, player_bullet_x, player_bullet_y, enemy_bullet_x, enemy_bullet_y, timer_count, player_direction, enemy_direction
    # print(enemy_bullet_x,enemy_bullet_y)
    data = str(net.id) + ":" + output + '?' + str(playerX) + ',' + str(playerY) + ',' + str(
        player_bullet_x) + ',' + str(player_bullet_y) + ',' + str(player_direction)
    reply = net.send(data)
    arr = reply.split('?')
    timer_count = int(arr[3])

    if net.id == "0":
        opponent_X = int(arr[2][2:].split(',')[0])
        opponent_Y = int(arr[2][2:].split(',')[1])
        enemy_bullet_x = int(arr[2][2:].split(',')[2])
        enemy_bullet_y = int(arr[2][2:].split(',')[3])
        enemy_direction = (arr[2][2:].split(',')[4])
        playerX = int(arr[1][2:].split(',')[0])
        playerY = int(arr[1][2:].split(',')[1])
        player_bullet_x = int(arr[1][2:].split(',')[2])
        player_bullet_y = int(arr[1][2:].split(',')[3])
        player_direction = (arr[1][2:].split(',')[4])
    else:
        opponent_X = int(arr[1][2:].split(',')[0])
        opponent_Y = int(arr[1][2:].split(',')[1])
        enemy_bullet_x = int(arr[1][2:].split(',')[2])
        enemy_bullet_y = int(arr[1][2:].split(',')[3])
        enemy_direction = (arr[1][2:].split(',')[4])
        playerX = int(arr[2][2:].split(',')[0])
        playerY = int(arr[2][2:].split(',')[1])
        player_bullet_x = int(arr[2][2:].split(',')[2])
        player_bullet_y = int(arr[2][2:].split(',')[3])
        player_direction = (arr[2][2:].split(',')[4])

    global opponent_Y_old, opponent_Y_change, opponent_X_old, opponent_X_change
    opponent_X_change = opponent_X - opponent_X_old
    opponent_Y_change = opponent_Y - opponent_Y_old
    opponent_X_old = opponent_X
    opponent_Y_old = opponent_Y
    reply = arr[0]
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
        # timeadd += 1
        # if timeadd % 15 == 0:
        #   start_tick += 1000
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
        if int(hit1) > int(hit2):

            largetext = pygame.font.SysFont("comicsansms", 90)
            smalltext = pygame.font.SysFont("comicsansms", 50)

            textsurf, textrect = text_objects("YOU WON", red, "large")
            textrect.center = (957, 177)
            gameDisplay.blit(textsurf, textrect)
            textsurf1, textrect1 = text_objects("PLAYER 1 :" + " + " + str(hit1) + "   - " + str(kill1), black, "small")
            textrect1.center = (957, 277)
            gameDisplay.blit(textsurf1, textrect1)
            textsurf2, textrect2 = text_objects("PLAYER 2 :" + " + " + str(hit2) + "   - " + str(kill2), black, "small")
            textrect2.center = (957, 327)
            gameDisplay.blit(textsurf2, textrect2)

        elif int(hit1) < int(hit2):

            largetext = pygame.font.SysFont("comicsansms", 90)
            smalltext = pygame.font.SysFont("comicsansms", 50)
            textsurf, textrect = text_objects("YOU LOSE", red, "large")
            textrect.center = (957, 177)
            gameDisplay.blit(textsurf, textrect)
            textsurf1, textrect1 = text_objects("PLAYER 1 :" + " + " + str(hit1) + "   - " + str(kill1), black, "small")
            textrect1.center = (957, 277)
            gameDisplay.blit(textsurf1, textrect1)
            textsurf2, textrect2 = text_objects("PLAYER 2 :" + " + " + str(hit2) + "   - " + str(kill2), black, "small")
            textrect2.center = (957, 327)
            gameDisplay.blit(textsurf2, textrect2)
        else:

            largetext = pygame.font.SysFont("comicsansms", 90)
            smalltext = pygame.font.SysFont("comicsansms", 50)
            textsurf, textrect = text_objects("TIE", red, "large")
            textrect.center = (957, 177)
            gameDisplay.blit(textsurf, textrect)
            textsurf1, textrect1 = text_objects("PLAYER 1 :" + " + " + str(hit1) + "   - " + str(kill1), black, "small")
            textrect1.center = (957, 277)
            gameDisplay.blit(textsurf1, textrect1)
            textsurf2, textrect2 = text_objects("PLAYER 2 :" + " + " + str(hit2) + "   - " + str(kill2), black, "small")
            textrect2.center = (957, 327)
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
        clock.tick(10)


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
        clock.tick(10)


def chatWithPlay():
    global chatStr, printchat, printchatcheck, FPScount

    if FPScount == 150:
        chatStr = ""
        printchat = ""
        # print("DONE")
        chat_screen_update()


def timer(start_tick):
    global time_left
    time_left = 150 - (pygame.time.get_ticks() - start_tick) / 1000
    min, sec = divmod(time_left, 60)
    if int(min) == int(0) and int(sec) == int(0):
        # print("helllllo")
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


def player_draw(player_x, player_y, image, mirror=False):
    # pygame.draw.rect(gameDisplay, red, (player_x, player_y + 32, 32, 32))
    # pygame.draw.rect(gameDisplay, black, (player_x, player_y, 32, 16))
    global walk1
    global left1
    global right1
    global standr1
    global standl1
    global walk
    global left
    global right
    global standr
    global standl
    player_x -= 16
    if net.id == '1':
        mirror = not mirror
    if mirror:
        image = pygame.transform.flip(image, True, False)
    if net.id == '1':
        text = font.render('Score  ' + str(hit1) + " : " + str(kill1), 1, (0, 0, 0))
    else:
        text = font.render('Score  ' + str(kill1) + " : " + str(hit1), 1, (0, 0, 0))
    gameDisplay.blit(text, (10, 20))
    if net.id != '1':
        if not mirror:
            if walk + 1 >= 32:
                walk = 0
            if left:
                gameDisplay.blit(walkleft[walk // 4], [player_x, player_y])
                walk += 1
                left = False
                standl = True
                standr = False
            elif right:
                gameDisplay.blit(walkright[walk // 4], [player_x, player_y])
                walk += 1
                right = False
                standr = True
                standl = False
            elif standr:
                gameDisplay.blit(image, [player_x, player_y])
            elif standl:
                # image = pygame.transform.flip(image, True, False)
                gameDisplay.blit(image, [player_x, player_y])
        else:
            if walk1 + 1 >= 32:
                walk1 = 0
            elif opponent_X_change > 0:
                gameDisplay.blit(walkright1[walk1 // 4], [player_x, player_y])
                walk1 += 1
                right1 = False
                standl1 = False
                standr1 = True
            elif opponent_X_change < 0:
                gameDisplay.blit(walkleft1[walk1 // 4], [player_x, player_y])
                walk1 += 1
                left1 = False
                standl1 = True
                standr1 = False
            elif standr1:
                gameDisplay.blit(image, [player_x, player_y])
            elif standl1:
                # image = pygame.transform.flip(image, True, False)
                gameDisplay.blit(image, [player_x, player_y])
    else:
        if mirror:
            if walk1 + 1 >= 32:
                walk1 = 0
            if left1:
                gameDisplay.blit(walkleft1[walk1 // 4], [player_x, player_y])
                walk1 += 1
                left1 = False
                standl1 = True
                standr1 = False
            elif right1:
                gameDisplay.blit(walkright1[walk1 // 4], [player_x, player_y])
                walk1 += 1
                right1 = False
                standr1 = True
                standl1 = False
            elif standr1:
                gameDisplay.blit(image, [player_x, player_y])
            elif standl1:
                # image = pygame.transform.flip(image, True, False)
                gameDisplay.blit(image, [player_x, player_y])
        else:
            if walk + 1 >= 32:
                walk = 0
            if opponent_X_change < 0:
                gameDisplay.blit(walkleft[walk // 4], [player_x, player_y])
                walk += 1
                left = False
                standl = True
                standr = False
            elif opponent_X_change > 0:
                gameDisplay.blit(walkright[walk // 4], [player_x, player_y])
                walk += 1
                right = False
                standr = True
                standl = False
            elif standr:
                gameDisplay.blit(image, [player_x, player_y])
            elif standl:
                # image = pygame.transform.flip(image, True, False)
                gameDisplay.blit(image, [player_x, player_y])
    # gameDisplay.blit(image, [player_x - 16, player_y])
    # chat_screen_update()


def obstacle_check(player_x, player_y, change_x, change_y, air_stay, direction, obstacle_x, obstacle_y, width, height,
                   player_width=28, player_height=60):
    if obstacle_x <= player_x + change_x <= obstacle_x + width or obstacle_x <= player_x + player_width + change_x <= obstacle_x + width:
        if obstacle_y <= player_y + change_y <= obstacle_y + height or obstacle_y <= player_y + player_height + change_y <= obstacle_y + height or player_y <= obstacle_y < player_y + player_height or player_y <= obstacle_y + height <= player_y + player_height:
            global air

            if player_width == 24 and player_height == 24:
                air_stay = True
            if direction["right"] and direction["up"] == 0 and direction["down"] == 0:
                change_x = obstacle_x - player_x - player_width
            elif direction["left"] and direction["up"] == 0 and direction["down"] == 0:
                change_x -= obstacle_x + width - player_x
            elif direction["up"] == 0 and direction["down"] == 0:
                if abs(obstacle_x - player_x - player_width) < abs(obstacle_x + width - player_x):
                    change_x = obstacle_x - player_x - player_width
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
                if obstacle_y < player_y + player_height + change_y < obstacle_y + height:
                    change_y = obstacle_y - player_y - player_height
                    direction["up"] = 0
                    direction["down"] = 0
                    air_stay = 0
                    air = False
                if air_stay != 0:
                    change_x = 0
    return change_x, change_y, air_stay, direction


def obstacles(playerX, playerY, x_change, y_change, air_stay_count, direction, player_width=28, player_height=60):
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 128, 352, 32, 32, player_width,
                                                                   player_height)  # plank 2
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 480, 512, 32, player_width,
                                                                   player_height)  # ground 1
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 512, 480, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 544, 448, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 576, 416, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 608, 384, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 224, 288, 192, 32, player_width,
                                                                   player_height)  # plank 3
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 256, 320, 128, 64, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 192, 128, 32, player_width,
                                                                   player_height)  # plank 1
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 224, 96, 64, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 288, 64, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 0, 320, 32, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 544, 224, 128, 96, player_width,
                                                                   player_height)  # plank 4
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 800, 256, 128, 96, player_width,
                                                                   player_height)  # plank 5
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 640, 480, 192, 32, player_width,
                                                                   player_height)  # ground 2
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 672, 512, 128, 64, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 704, 576, 64, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 960, 480, 320, 32, player_width,
                                                                   player_height)  # ground 3
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 992, 512, 288, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1024, 544, 256, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1056, 576, 224, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1088, 608, 192, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1120, 352, 32, 32, player_width,
                                                                   player_height)  # plank 7
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1056, 256, 32, 32, player_width,
                                                                   player_height)  # plank 6
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1152, 192, 128, 32, player_width,
                                                                   player_height)  # plank 8
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1184, 224, 96, 64, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1216, 288, 64, 32, player_width,
                                                                   player_height)
    x_change, y_change, air_stay_count, direction = obstacle_check(playerX, playerY, x_change, y_change, air_stay_count,
                                                                   direction, 1248, 320, 32, 32, player_width,
                                                                   player_height)

    return x_change, y_change, air_stay_count, direction


def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = gren
    elif player_health > 50:
        player_health_color = yelow
    else:
        player_health_color = rde

    if enemy_health > 75:
        enemy_health_color = gren
    elif enemy_health > 50:
        enemy_health_color = yelow
    else:
        enemy_health_color = rde
    if net.id == '0':
        pygame.draw.rect(gameDisplay, player_health_color, (430, 25, player_health, 30))
        pygame.draw.rect(gameDisplay, enemy_health_color, (750, 25, enemy_health, 30))
    else:
        pygame.draw.rect(gameDisplay, player_health_color, (750, 25, player_health, 30))
        pygame.draw.rect(gameDisplay, enemy_health_color, (430, 25, enemy_health, 30))


def fire(playerY, face, move_fire, direc):
    global player_bullet_y
    fire_bullet = True
    if face == "left":
        direc["left"] = 1
        move_fire -= 16
        if move_fire < 0:
            fire_bullet = False
        X, Y, air, direc = obstacles(move_fire, player_bullet_y, -16, 0, 0, direc, 24, 24)
    else:
        direc["right"] = 1
        move_fire += 16
        if move_fire > 1280:
            fire_bullet = False
        X, Y, air, direc = obstacles(move_fire, player_bullet_y, 16, 0, 0, direc, 24, 24)
    if air:
        fire_bullet = False
    # pygame.draw.circle(gameDisplay,light_green,(move_fire,player_bullet_y),12)
    gameDisplay.blit(bullet_right, [move_fire, player_bullet_y])
    return fire_bullet, move_fire


def gameLoop():
    global count
    global left, left1
    global right, right1
    global jump, jump1
    global pause
    # to be able to modify direction

    # Event Handling
    gameDisplay.fill(white)
    gameDisplay.blit(background_clouds, [0, 0])
    gameExit = False

    global player_health, enemy_health, kill1, hit1, kill2, hit2
    player_health = 100
    enemy_health = 100

    direction = {"right": 0, "left": 0, "up": 0, "down": 0}

    global playerX, playerY, opponent_X, opponent_Y
    playerX = 32
    playerY = 400
    opponent_X = 1248
    opponent_Y = 400

    global player_bullet_x, player_bullet_y, bullet_direction_player, enemy_bullet_x, enemy_bullet_y

    if net.id == '1':
        playerX = 1248
        playerY = 400
        opponent_X = 32
        opponent_Y = 400

    air_stay_count = 0
    x_change = 0
    y_change = 0
    face = "left"

    move_fire = 1285  # firing
    fire_y = 685
    fire_bullet = False
    direc_fire = {"left": 0, "right": 0, "up": 0, "down": 0}
    direc_fire_const = direc_fire
    face_const = face

    global start_tick, player_direction, enemy_direction, bullet_direction_player, bullet_direction_enemy, air
    start_tick = pygame.time.get_ticks()
    temp_air = False
    temp_air_E = False
    while not gameExit:
        count += 1
        print(opponent_X_change)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        keys = pygame.key.get_pressed()  # movements
        if keys[pygame.K_UP] and air_stay_count == 0 and direction["down"] == 0 and air == False:
            jump = True
            direction["up"] = 1
            air_stay_count = 32
            air = True
        if keys[pygame.K_LEFT]:
            if net.id != '1':
                left = True
                right = False
                jump = False
            elif net.id == '1':
                left1 = True
                right1 = False
                jump1 = False
            x_change = -4
            face = "left"
            direction["left"] = 1
            direction["right"] = 0
        if keys[pygame.K_RIGHT]:
            if net.id != '1':
                right = True
                left = False
                jump = False
            elif net.id == '1':
                right1 = True
                left1 = False
                jump1 = False

            x_change = +4
            face = "right"
            direction["left"] = 0
            direction["right"] = 1
        if keys[pygame.K_SPACE] and fire_bullet == False:
            move_fire = playerX
            fire_y = playerY
            fire_bullet = True
            direc_fire_const = direc_fire
            face_const = face
            if face_const == "right":
                bullet_direction_player = 'r'
            else:
                bullet_direction_player = 'l'
            player_bullet_x = move_fire
            player_bullet_y = playerY + 12
        if keys[pygame.K_p]:
            pygame.draw.rect(gameDisplay, red, (1180, 55, 90, 40))
            pause = True
            paused()

        button("Chat", 1180, 11, 90, 40, yellow, light_yellow, action="chat")
        button("PAUSE", 1180, 55, 90, 40, red, light_red, action="paused")

        if timer_count < 2:
            start_tick = pygame.time.get_ticks()
        timer(start_tick)

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
        chatting()
        chatWithPlay()
        if playerY + y_change >= 520:
            air_stay_count = 0
            y_change = 0
            playerY = 576
            player_health = 0
            air = False
            x_change = 0
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

        if opponent_Y >= 512:
            enemy_health = 0

        if player_health != 0:
            x_change, y_change, air_stay_count, direction = obstacles(playerX, playerY, x_change, y_change,
                                                                      air_stay_count,
                                                                      direction)  # obstacles
        playerX += x_change
        playerY += y_change
        x_change = 0
        y_change = 0
        direction["down"] = 0
        direction["up"] = 0
        direction["right"] = 0
        direction["left"] = 0

        chat_screen_update()
        if fire_bullet:
            if temp_air:
                fire_bullet = False
                player_bullet_x = 1285
                player_bullet_y = 645
                enemy_health -= 10
                temp_air = False
            else:
                fire_bullet, move_fire = fire(fire_y, face_const, move_fire, direc_fire_const)
                player_bullet_x = move_fire
                if face_const == "left":
                    player_1_2_x, player_1_2_y, temp_air, temp_dict = obstacle_check(player_bullet_x, player_bullet_y,
                                                                                     -16, 0, 0,
                                                                                     direc_fire_const, opponent_X,
                                                                                     opponent_Y, 32, 32, 24, 24)
                else:
                    player_1_2_x, player_1_2_y, temp_air, temp_dict = obstacle_check(player_bullet_x, player_bullet_y,
                                                                                     16, 0, 0,
                                                                                     direc_fire_const, opponent_X,
                                                                                     opponent_Y, 32, 32, 24, 24)

        else:
            player_bullet_x = 1285
            player_bullet_y = 645
        if not temp_air_E:
            player_1_2_x, player_1_2_y, temp_air_E, temp_dict = obstacle_check(enemy_bullet_x, enemy_bullet_y, -16, 0,
                                                                               0,
                                                                               direc_fire_const, playerX, playerY, 32,
                                                                               64
                                                                               , 24, 24)
            if not temp_air_E:
                player_1_2_x, player_1_2_y, temp_air_E, temp_dict = obstacle_check(enemy_bullet_x, enemy_bullet_y, 16,
                                                                                   0, 0,
                                                                                   direc_fire_const, playerX, playerY,
                                                                                   32,
                                                                                   64
                                                                                   , 24, 24)
        else:
            player_health -= 10
            temp_air_E = False
        if enemy_health == 0:
            kill1 += 1
            hit2 += 1
            enemy_health = 100
            if net.id == '1':
                opponent_X = 32
                opponent_Y = 400
            else:
                opponent_X = 1248
                opponent_Y = 400
        if player_health == 0:
            hit1 += 1
            kill2 += 1
            player_health = 100
            if net.id == '0':
                playerX = 32
                playerY = 400
            else:
                playerX = 1248
                playerY = 400

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()


game_intro()
