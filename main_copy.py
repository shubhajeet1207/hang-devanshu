import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images.
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
words = ["IDE", "REPLIT", "PYTHON", "PYGAME"]
word = random.choice(words)
guessed = []

# variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
display_width = 900
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))


def draw():
    win.fill(WHITE)

    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def quitGame():
    pygame.quit()
    quit()


def text_object(text, font, color=BLACK):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def display_message(message):
    text = pygame.font.SysFont('comicsansms', 20)
    global used
    for i in used:
        textSurf, textRect = text_object(i, text)
        for j in range(int(len(used[i]) / 2)):
            textRect.center = (used[i][2 * j], used[i][2 * j + 1])
            gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def button(msg, x, y, w, h, c1, c2, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global first
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, c1, (x, y, w, h))
        if click[0] and action:
            first = 1
            quitGame()
    else:
        pygame.draw.rect(gameDisplay, c2, (x, y, w, h))
    font = pygame.font.SysFont('comicsansms', 30)
    textSurf, textRect = text_object(msg, font)
    textRect.center = ((x + w / 2), (y + h / 2))
    gameDisplay.blit(textSurf, textRect)


def game_start():
    pygame.mixer.music.play(-1)
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        gameDisplay.fill(WHITE)
        button('Start..!', 200, 400, 150, 100)
        button('Exit', 500, 400, 150, 100)
        pygame.display.update()


def main():
    global hangman_status
    global button
    global win_time
    win_time = 0
    loss_time = 0

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            pause = 1
            display_message('You won..!')
            if win_time == 0:
                win_time = 1
                if win_time != 20:
                    main()
                else:
                    pygame.quit()
            break

        if hangman_status == 6:
            display_message("You LOST!")
            break


while True:
    main()
pygame.quit()
