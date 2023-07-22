from random import choice
import threading
import pygame
import time


width  = 850
height = 600

running = True
white = (255,255,255)

paddle_width  = 15
paddle_height = 70
paddle_speed  = 12 # Smaller = faster

ball_radius = 8
ball_speed  = 22 # Smaller = faster


pygame.init()
font = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Pong by Nick Sciarretta')


class LeftPaddle:

    def __init__(self):

        self.score = 0

        self.x = 40+paddle_width
        self.y = (height-paddle_height)//2
        threading.Thread(target=self.move).start()

    
    def move(self):

        while running:

            time.sleep(paddle_speed/10_000)

            keys = pygame.key.get_pressed()

            # w = move paddle up
            if keys[pygame.K_w] and self.y > 0:
                self.y -= 1

            # s = move paddle down
            elif keys[pygame.K_s] and self.y < height-paddle_height:
                self.y += 1


class RightPaddle:

    def __init__(self):

        self.score = 0

        self.x = width-40-paddle_width
        self.y = (height-paddle_height)//2
        threading.Thread(target=self.move).start()

    
    def move(self):

        while running:

            time.sleep(paddle_speed/10_000)

            keys = pygame.key.get_pressed()

            # up arrow = move paddle up
            if keys[pygame.K_UP] and self.y > 0:
                self.y -= 1

            # down arrow = move paddle down
            elif keys[pygame.K_DOWN] and self.y < height-paddle_height:
                self.y += 1


class Ball:

    def __init__(self, left_paddle: LeftPaddle, right_paddle: RightPaddle):

        self.left_paddle  = left_paddle
        self.right_paddle = right_paddle

        self.x  = width//2
        self.y  = height//2
        self.dx = self.dy = 0

        threading.Thread(target=self.move).start()

    
    def move(self):

        self.countdown = 0
        self.reset(choice([-1,1]))

        while running:

            time.sleep(ball_speed/10_000)

            # Ball hit left edge of screen
            if self.x == -ball_radius: 
                self.right_paddle.score += 1
                self.reset(dx=1)

            # Ball hit right edge of screen
            elif self.x == width+ball_radius: 
                self.left_paddle.score += 1
                self.reset(dx=-1)

            # Ball hit top / bottom edge of screen
            elif self.y == ball_radius or self.y == height-ball_radius:
                self.dy *= -1

            # Ball hit left paddle
            elif (
            self.x-ball_radius == self.left_paddle.x and
            self.left_paddle.y-10 < self.y < self.left_paddle.y+paddle_height+10
            ): self.dx *= -1

            # Ball hit right paddle
            elif (
            self.x+ball_radius == self.right_paddle.x and
            self.right_paddle.y-10 < self.y < self.right_paddle.y+paddle_height+10
            ): self.dx *= -1

            self.x += self.dx
            self.y += self.dy


    def reset(self, dx: int):

        self.x  = width//2
        self.y  = height//2
        self.dx = self.dy = 0

        self.countdown = 30
        while running and self.countdown > 0:
            self.countdown -= 1
            time.sleep(0.1)

        self.dx = dx
        self.dy = choice([-1,1])


lp = LeftPaddle()
rp = RightPaddle()
ball = Ball(lp, rp)


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0,0,0))

    # Score text
    text = font.render(f'{lp.score} - {rp.score}', True, white)
    rect = text.get_rect()
    rect.center = (width//2, 30)
    screen.blit(text, rect)

    # Countdown text
    if ball.countdown > 0:
        text = font.render(f'{1+ball.countdown//10}', True, white)
        rect = text.get_rect()
        rect.center = (width//2, 240)
        screen.blit(text, rect)

    # Draw ball
    pygame.draw.circle(screen, white, (ball.x, ball.y), ball_radius)

    # Draw left paddle
    rect = pygame.Rect(lp.x-paddle_width, lp.y, paddle_width, paddle_height)
    pygame.draw.rect(screen, white, rect)

    # Draw right paddles
    rect = pygame.Rect(rp.x, rp.y, paddle_width, paddle_height)
    pygame.draw.rect(screen, white, rect)

    pygame.display.update()


pygame.quit()