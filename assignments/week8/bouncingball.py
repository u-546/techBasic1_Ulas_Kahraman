import pygame
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 300
BACKGROUND_COLOR = (255, 255, 255)

pygame.init()

# load the boing sound effect, I made it myself by editing my voice! I stacked the boing and pitched it up to make a chord
boing = pygame.mixer.Sound("boing.mp3")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bouncing Ball')

# load the ball image
img = pygame.image.load("ball.png").convert_alpha()
img = pygame.transform.scale(img, (80, 80))
SIZE = 80

# place the ball at a random starting position every time you run the program
ball_x = random.randint(0, SCREEN_WIDTH - SIZE)
ball_y = random.randint(0, SCREEN_HEIGHT - SIZE)

# give the ball a random speed and direction
vx = random.choice([-1, 1]) * random.randint(3, 6)
vy = random.choice([-1, 1]) * random.randint(3, 6)

#used to stretch the ball when it hits a wall
squash = 1.0
squash_timer = 0

clock = pygame.time.Clock()

flag = True
while flag:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    # move the ball by adding velocity to its position each frame
    ball_x += vx
    ball_y += vy

    bounced = False

    # check if the ball hit the left or right wall, and flip horizontal
    if ball_x <= 0:
        ball_x = 0
        vx = abs(vx)
        bounced = True
        boing.play()
    elif ball_x >= SCREEN_WIDTH - SIZE:
        ball_x = SCREEN_WIDTH - SIZE
        vx = -abs(vx)
        bounced = True
        boing.play()

    # check if the ball hit the top or bottom wall, and flip vertical
    if ball_y <= 0:
        ball_y = 0
        vy = abs(vy)
        bounced = True
        boing.play()
    elif ball_y >= SCREEN_HEIGHT - SIZE:
        ball_y = SCREEN_HEIGHT - SIZE
        vy = -abs(vy)
        bounced = True
        boing.play()

    # when the ball hits a wall, trigger the squash effect
    if bounced:
        squash = 1.4
        squash_timer = 10

    # slowly bring the squash back to normal over 10 frames
    if squash_timer > 0:
        squash_timer -= 1
        squash = 1.0 + 0.4 * (squash_timer / 10)
    else:
        squash = 1.0

    # stretch the image to a squish squash on impact, my mind couldn't comprehend this so I had help from ai
    squashed_w = int(SIZE * squash)
    squashed_h = int(SIZE / squash)
    img_draw = pygame.transform.scale(img, (squashed_w, squashed_h))

    # offset so the ball stays centered while squishing
    offset_x = (squashed_w - SIZE) // 2
    offset_y = (squashed_h - SIZE) // 2

    screen.fill(BACKGROUND_COLOR)
    screen.blit(img_draw, (int(ball_x) - offset_x, int(ball_y) - offset_y))
    pygame.display.flip()

pygame.quit()
exit(0)
