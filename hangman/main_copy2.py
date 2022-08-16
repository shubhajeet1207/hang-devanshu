# imports
import time, random, pygame

# pygame module initialisation
pygame.init()

# GUI color palette
white = (255, 255, 255)
CYAN = (0, 255, 255)
gray = (128, 128, 128)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)

# GUI display configuration
display_width = 900
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))

# Image imports
pygame.display.set_caption('Hangman')
img = pygame.image.load('hangman.jpg')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# taking random words from txt file
fileptr = open('wordlist', 'r')
words = fileptr.read()
words = words.split('\n')
words_length = len(words)

# keyboard input variables declarations
used = {}
left = {}
pressed = {}
word = ''
word_length = 0
line_x = 0
line_y = 0
bar = 15
count = 0
pause = 0
correct = 0
clock = pygame.time.Clock()
first = 0
score = 0


# game quit function
def quitGame():
    pygame.quit()
    quit()


# text model function for representation of text on screen
def text_object(text, font, color=BLACK):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


# display function aka GUI screen
def display_used():
    # font and font size declaration
    text = pygame.font.SysFont('comicsans', 20)
    global used
    for i in used:
        textSurf, textRect = text_object(i, text)
        for j in range(int(len(used[i]) / 2)):
            textRect.center = (used[i][2 * j], used[i][2 * j + 1])
            gameDisplay.blit(textSurf, textRect)
    pygame.display.update()


# function for underline or blank space for filling up the space
def showleft():
    text = pygame.font.SysFont('comicsans', 20)
    global left
    for i in left:
        textSurf, textRect = text_object(i, text, BLUE)
        for j in range(int(len(left[i]) / 2)):
            textRect.center = (left[i][2 * j], left[i][2 * j + 1])
            gameDisplay.blit(textSurf, textRect)


# button function for taking user action
def button(msg, x, y, w, h, c1, c2, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global first
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, c1, (x, y, w, h))
        if click[0] and action:
            first = 1
            action()
            if action == closing or action == closing1:
                quitGame()
    else:
        pygame.draw.rect(gameDisplay, c2, (x, y, w, h))
    font = pygame.font.SysFont('comicsans', 30)
    textSurf, textRect = text_object(msg, font)
    textRect.center = ((x + w / 2), (y + h / 2))
    gameDisplay.blit(textSurf, textRect)


# letter function for presenting the words on the blanks
def letter(msg, x, y, w, h, c1, c2):
    # taking user input from mouse as well keyboard
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global used, pressed, word, correct, correct, word_length, line_x, line_y, bar, count, pause, first
    if x + w > mouse[0] > x and y + h > mouse[1] > y and pause == 0:
        pygame.draw.rect(gameDisplay, c1, (x, y, w, h))
        if click[0] == 1:
            if first == 1:
                first = 0
            else:
                pressed[msg] = 1
                change = 0
                for i in range(word_length):
                    if word[i] == msg:
                        correct += 1
                        change = 1
                        if msg not in used:
                            used[msg] = [15 * (i + 1) + bar * i + int(bar / 2), line_y - 20]
                        else:
                            used[msg].append(15 * (i + 1) + bar * i + int(bar / 2))
                            used[msg].append(line_y - 20)
                if change == 0:
                    count += 1
    else:
        pygame.draw.rect(gameDisplay, c2, (x, y, w, h))
    font = pygame.font.SysFont('comicsans', 30)
    textSurf, textRect = text_object(msg, font)
    textRect.center = ((x + w / 2), (y + h / 2))
    gameDisplay.blit(textSurf, textRect)


def letter_pressed(msg, x, y):
    pygame.draw.rect(gameDisplay, WHITE, (x, y, 50, 50))
    font = pygame.font.SysFont('comicsans', 30)
    textSurf, textRect = text_object(msg, font, RED)
    textRect.center = ((x + 25), (y + 25))
    gameDisplay.blit(textSurf, textRect)


# closing function which will be activated when user is trying to exit the game(aka animation effect)
def closing():
    for i in range(1, 730):
        gameDisplay.fill(white)
        pygame.draw.circle(gameDisplay, BLACK, (575, 450), i)
        pygame.display.update()


# closing function which will be activated when user is trying to exit the game(aka whoop out animation effect)
def closing1():
    for i in range(1, 730):
        gameDisplay.fill(white)
        pygame.draw.circle(gameDisplay, BLACK, (350, 150), i)
        pygame.display.update()


# opening function which will be activated when user is play the game for the first time(aka whoop in animation effect)
def opening():
    for i in range(700, -1, -1):
        gameDisplay.fill(white)
        pygame.draw.circle(gameDisplay, BLACK, (275, 450), i)
        pygame.display.update()
        x = 150
        y = 400
    # displaying keyboard on the screen with ease in animation
    gameDisplay.fill(WHITE)
    for i in 'QWERTYUIOP':
        time.sleep(.1)
        letter(i, x, y, 50, 50, RED, gray)
        pygame.display.update()
        x += 55
    x = 180
    y = 455
    for i in 'ASDFGHJKL':
        time.sleep(.1)
        letter(i, x, y, 50, 50, RED, gray)
        x += 55
        pygame.display.update()
    x = 235
    y = 510
    for i in 'ZXCVBNM':
        time.sleep(.1)
        letter(i, x, y, 50, 50, RED, gray)
        x += 55
        pygame.display.update()
    game_loop()


# function for the message box on screen in the text_object area
def message_display(text):
    largeText = pygame.font.SysFont('comicsans', 100)
    TextSurf, TextRect = text_object(text, largeText)
    TextRect.center = (300, 80)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


# function for hangman image construction when the user is predicting wrong words
def hangman():
    if count > 0:
        pygame.draw.line(gameDisplay, BLACK, (750, 300), (850, 300), 5)
        pygame.draw.line(gameDisplay, BLACK, (800, 300), (800, 80), 5)
        pygame.draw.line(gameDisplay, BLACK, (700, 80), (800, 80), 5)
        pygame.draw.line(gameDisplay, BLACK, (750, 300), (800, 250), 5)
        pygame.draw.line(gameDisplay, BLACK, (700, 80), (700, 100), 5)
    if 1 < count < 8:
        pygame.draw.circle(gameDisplay, BLACK, (700, 135), 35)
        pygame.draw.circle(gameDisplay, BLACK, (700, 135), 32)
    if count > 2:
        pygame.draw.line(gameDisplay, BLACK, (700, 170), (700, 250), 3)
    if 3 < count < 8:
        pygame.draw.line(gameDisplay, BLACK, (700, 195), (660, 175), 3)
    if 4 < count < 8:
        pygame.draw.line(gameDisplay, BLACK, (700, 195), (740, 175), 3)
    if count > 5:
        pygame.draw.line(gameDisplay, BLACK, (700, 250), (660, 280), 3)
    if count > 6:
        pygame.draw.line(gameDisplay, BLACK, (700, 250), (740, 280), 3)
    if count > 7:
        pygame.draw.circle(gameDisplay, BLACK, (680, 145), 35)
        pygame.draw.circle(gameDisplay, WHITE, (680, 145), 32)
        pygame.draw.line(gameDisplay, BLACK, (700, 118), (700, 100), 5)
        pygame.draw.line(gameDisplay, BLACK, (700, 195), (660, 230), 3)
        pygame.draw.line(gameDisplay, BLACK, (700, 195), (740, 230), 3)
        global word, used, bar, line_x, line_y, left, word_length, pause
        # loop for continues construction of body whenever user s predicting wrong word
        for i in range(word_length):
            if word[i] not in used:
                if word[i] not in left:
                    left[word[i]] = [15 * (i + 1) + bar * i + int(bar / 2), line_y - 20]
                else:
                    left[word[i]].append(15 * (i + 1) + bar * i + int(bar / 2))
                    left[word[i]].append(line_y - 20)
    # refreshing screen after completion of game using update function
    pygame.display.update()


# function for starting game
def game_start():
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        gameDisplay.fill(white)
        gameDisplay.blit(img, (110, 50))
        # buttons for starting and exiting the game at initial interface
        button('Start..!', 200, 400, 150, 100, gray, WHITE, opening) # parameters of button customization
        button('Exit', 500, 400, 150, 100, gray, WHITE, closing) # parameters of button customization
        pygame.display.update()


# function for gaming session
def game_loop():
    game = True
    global used, left, count, pressed, word, word_length, correct, pause, line_x, line_y, bar
    left = {}
    pressed = {}
    used = {}
    pygame.display.update()
    correct = 0
    pause = 0
    count = 0
    prev = 0
    win_time = 0
    loss_time = 0
    while 1:
        word = words[random.randint(0, words_length - 1)].upper()
        word_length = len(word)
        if word_length == 0:
            continue
        else:
            break
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        gameDisplay.fill(WHITE)
        line_x = 0
        line_y = 300
        bar = int((550 - word_length * 8) / word_length)
        for i in range(word_length):
            pygame.draw.line(gameDisplay, BLACK, (line_x, line_y), (line_x + 15, line_y))
            line_x += 15
            pygame.draw.line(gameDisplay, BLACK, (line_x, line_y), (line_x + bar, line_y))
            line_x += bar
        x = 150
        y = 400
        # loop for continues inout from the user
        for i in 'QWERTYUIOP':
            if i not in pressed:
                letter(i, x, y, 50, 50, RED, gray)
            else:
                letter_pressed(i, x, y)
            x += 55
        x = 180
        y = 455
        # loop for continues inout from the user
        for i in 'ASDFGHJKL':
            if i not in pressed:
                letter(i, x, y, 50, 50, RED, gray)
            else:
                letter_pressed(i, x, y)
            x += 55
        x = 235
        y = 510
        # loop for continues inout from the user
        for i in 'ZXCVBNM':
            if i not in pressed:
                letter(i, x, y, 50, 50, RED, gray)
            else:
                letter_pressed(i, x, y)
            x += 55
        if correct == word_length:
            pause = 1
            message_display('You won..!')
            if win_time == 0:
                win_time = 1
                # whenever the game is complete new game will be automatically restart
                game_loop()
        if count > 7:
            pause = 1
            message_display('You Lost..!')
            if loss_time == 0:
                loss_time = 1
            button('Play Again', 100, 150, 180, 100, RED, gray, game_loop)
            button('Exit', 300, 150, 150, 100, RED, gray, closing1)
        display_used()
        showleft()
        hangman()
        pygame.display.update()
        clock.tick(20)


game_start()
