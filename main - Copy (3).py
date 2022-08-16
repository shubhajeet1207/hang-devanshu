import pygame
import math
import random

pygame.init()
YELLOW = (255, 255, 0)
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")


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

LETTER_FONT = pygame.font.SysFont('comicsans', 30)
WORD_FONT = pygame.font.SysFont('comicsans', 50)
TITLE_FONT = pygame.font.SysFont('comicsans', 30)

images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)
print(images)

hangman_status = 0
words = ["CHEETAH", "GIRAFFE", "MICROWAVE"]
word = random.choice(words)
guessed = []

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

FPS = 60
clock = pygame.time.Clock()
run = True


def draw():
    win.fill(WHITE)

    if word == words[0]:
        text = TITLE_FONT.render("Hint: Fastest animal in the world", 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))
    if word == words[1]:
        text = TITLE_FONT.render("Hint: Animal who has the longest neck", 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))
    if word == words[2]:
        text = TITLE_FONT.render("Hint: Electronic Device used for Baking", 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    if hangman_status == 3:
        text = TITLE_FONT.render("Warning: Only 3 chances LEFT", 1, RED)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 60))
    if hangman_status == 4:
        text = TITLE_FONT.render("Warning: Only 2 chances LEFT", 1, BLUE)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 60))
    if hangman_status == 5:
        text = TITLE_FONT.render("Warning: Only 1 chance LEFT", 1, MAGENTA)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 60))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (260, 200))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    win.blit(images[hangman_status], (50, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 -
                    text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


score = 0
while score != 20:
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
                                    Bold = True
                                    won = True
                                    for letter in word:
                                        if letter not in guessed:
                                            won = False
                                            break
                                        if won:
                                            display_message("CORRECT!")
                                            score = score + 1
                                        if hangman_status == 6:
                                            display_message("WRONG!The word was {}".format(word))
                                            pygame.quit()
