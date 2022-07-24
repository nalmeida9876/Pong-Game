from tkinter import Widget
import pygame 
import random

pygame.font.init()
# shows score for both players
SCORE_FONT = pygame.font.SysFont('impact',40)
# sets the window size of game
WIDTH, HEIGHT = 720,460

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG") # sets name of the window

PLAYER_WIDTH = 10
PLAYER_LENGTH = 50
BORDER_SPACE = 75
BORDER_WIDTH = 10
FPS = 60 # defines how quickly game updates screen
WHITE = (255,255,255)

# ball speed
INITIAL_SPEED  = 4
HIT_XSPEED = 8
HIT_YSPEED = 6
ball_xspeed = INITIAL_SPEED
ball_yspeed = INITIAL_SPEED

PLAYER_SPEED = 8

# events that updates players score
LEFT_SCORE = pygame.USEREVENT + 1
RIGHT_SCORE = pygame.USEREVENT + 2

#collision tolerance 
COLLIDE = 10

# X,Y,width,length

def draw_window(left,right,ball,left_points,right_points):
    WINDOW.fill((0,0,0)) # maintains background of game

    pygame.draw.rect(WINDOW, WHITE, (0, left.y, PLAYER_WIDTH, PLAYER_LENGTH)) #left side
    pygame.draw.rect(WINDOW, WHITE, (WIDTH - 10, right.y, PLAYER_WIDTH, PLAYER_LENGTH)) # right side

    # display scores
    left_score_text = SCORE_FONT.render(str(left_points),1,WHITE)
    right_score_text = SCORE_FONT.render(str(right_points),1,WHITE)
    WINDOW.blit(left_score_text,(WIDTH/4,10))
    WINDOW.blit(right_score_text,(WIDTH/2 + WIDTH/4,10))

    # takes care of displaying moving ball
    ball_movement(ball,left,right)

    # draws dashed line down the middle of window
    pygame.draw.rect(WINDOW, WHITE, (WIDTH/2, 0, BORDER_WIDTH, 50))
    pygame.draw.rect(WINDOW, WHITE, (WIDTH/2, 75, BORDER_WIDTH, 50))
    pygame.draw.rect(WINDOW, WHITE, (WIDTH/2, 150, BORDER_WIDTH, 50))
    pygame.draw.rect(WINDOW, WHITE, (WIDTH/2, 225, BORDER_WIDTH, 50))
    pygame.draw.rect(WINDOW, WHITE, (WIDTH/2, 300, BORDER_WIDTH, 50))
    pygame.draw.rect(WINDOW, WHITE, (WIDTH/2, 375, BORDER_WIDTH, 50))
    pygame.draw.rect(WINDOW, WHITE, (WIDTH/2, 450, BORDER_WIDTH, 50))

    pygame.display.update()


def ball_movement(ball,left,right):
    global ball_xspeed, ball_yspeed
    # responsible for moving the ball on the screen
    ball.x += ball_xspeed
    ball.y += ball_yspeed

    # ball hits left or right border
    if ball.right >= WIDTH+50:
        # initial speed gives player chance to hit ball after game resets
        ball_xspeed = INITIAL_SPEED
        ball_yspeed = INITIAL_SPEED
        # ball starts at center and at any point on the dashed line
        ball.x = WIDTH/2
        ball.y = random.randint(20,HEIGHT-20)

        pygame.event.post(pygame.event.Event(LEFT_SCORE))
        
    if ball.left <= -50:
        ball_xspeed = INITIAL_SPEED * -1
        ball_yspeed = INITIAL_SPEED
        ball.x = WIDTH/2
        ball.y = random.randint(20,HEIGHT-20)
        pygame.event.post(pygame.event.Event(RIGHT_SCORE))

    #ball hits top or bottom border
    if ball.bottom >= HEIGHT or ball.top <= 0:
        ball_yspeed *= -1
    
    #hits players
    # checks each possible encounter with player and ball
    if ball.colliderect(left):
        # directions randomizes where the ball should go after being hit by player
        direction = random.randint(0,1)
        # if absolute value of player.side - ball.side is close to zero that means there is a collision 
        # ball speed in x and y  directions is modified depending on type of collision
        if abs(left.top - ball.bottom)< COLLIDE:
            if direction:
                ball_yspeed = HIT_YSPEED
            else:
                ball_yspeed = HIT_YSPEED * -1
            ball_xspeed = HIT_XSPEED * -1
            ball_yspeed *= -1
        if abs(left.bottom - ball.top)< COLLIDE:
            if direction:
                ball_yspeed = HIT_YSPEED
            else:
                ball_yspeed = HIT_YSPEED * -1
            ball_xspeed = HIT_XSPEED * -1
            ball_yspeed *= -1
        if abs(left.left - ball.right)< COLLIDE:
            ball_xspeed = HIT_XSPEED * -1
            if direction:
                ball_yspeed = HIT_YSPEED
            else:
                ball_yspeed = HIT_YSPEED * -1
            ball_xspeed *= -1
        if abs(left.right - ball.left)< COLLIDE:
            ball_xspeed = HIT_XSPEED * -1
            if direction:
                ball_yspeed = HIT_YSPEED
            else:
                ball_yspeed = HIT_YSPEED * -1
            ball_xspeed *= -1

    if ball.colliderect(right):
        direction = random.randint(0,1)
        if abs(right.top - ball.bottom)< COLLIDE:
            if direction:
                ball_yspeed = HIT_YSPEED
            else:
                ball_yspeed = HIT_YSPEED * -1
            ball_xspeed = HIT_XSPEED
            ball_yspeed *= -1
        if abs(right.bottom - ball.top)< COLLIDE:
            if direction:
                ball_yspeed = HIT_YSPEED
            else:
                ball_yspeed = HIT_YSPEED * -1
            ball_xspeed = HIT_XSPEED
            ball_yspeed *= -1
        if abs(right.left - ball.right)< COLLIDE:
            ball_xspeed = HIT_XSPEED
            if direction:
                ball_yspeed = HIT_YSPEED
            else:
                ball_yspeed = HIT_YSPEED * -1
            ball_xspeed *= -1
        if abs(right.right - ball.left)< COLLIDE:
            ball_xspeed = HIT_XSPEED
            if direction:
                ball_yspeed = HIT_YSPEED
            else:
                ball_yspeed = HIT_YSPEED * -1
            ball_xspeed *= -1

    pygame.draw.rect(WINDOW, WHITE, ball) # ball

def player_movement(left,right):
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w] and left.y >= 0: # left up
        left.y -= PLAYER_SPEED
    if pressed[pygame.K_s] and left.y <= HEIGHT-55: # left down
        left.y += PLAYER_SPEED
    if pressed[pygame.K_UP] and right.y >=0: # right up
        right.y -= PLAYER_SPEED
    if pressed[pygame.K_DOWN] and right.y <= HEIGHT-55: # right down
        right.y += PLAYER_SPEED

def main():
    # creates the structures of the ball, left player, and right player
    left = pygame.Rect(5,200,10,50)
    right = pygame.Rect(705,200,10,50)
    ball = pygame.Rect(WIDTH/2,75,10,10)

    # keeps track of score
    left_points = 0
    right_points = 0

    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(FPS) # ensures to not go over set FPS
        for event in pygame.event.get():
            # press red button on corner of screen
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == LEFT_SCORE:
                left_points += 1
            if event.type == RIGHT_SCORE:
                right_points += 1
        if left_points == 11 or right_points == 11:
            pygame.time.delay(2000)
            break
        player_movement(left,right)
        draw_window(left,right,ball,left_points,right_points)  
    main()

if __name__ == "__main__":
    main()