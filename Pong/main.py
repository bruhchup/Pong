'''pong game'''
import sys
import random as rand
import pygame as pg

pg.font.init()

WIDTH, HEIGHT = 950, 520
PLAYER_WIDTH, PLAYER_HEIGHT = 25, 100
BALL_CENTER = 412.5
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("pong")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255,255,0)
VEL = 10
POINT_FONT = pg.font.SysFont('CASCADIACODE', 40)
MENU_FONT = pg.font.SysFont('CASCADIACODE', 135)
WELCOME_MENU_FONT = pg.font.SysFont('CASCADIACODE', 110)
AGAIN_MENU_FONT = pg.font.SysFont('CASCADIACODE', 80)

print(POINT_FONT.size('0'))
print(WELCOME_MENU_FONT.size('PLAYER 2 WINS!'))
print(MENU_FONT.size('YES'))
print(MENU_FONT.size('NO'))

def draw_window(player1, player2, ball, score1, score2):
    '''renders the visuals of the game'''

    player1_point_text = POINT_FONT.render(str(score1), 1, WHITE)
    player2_point_text = POINT_FONT.render(str(score2), 1, WHITE)

    SCREEN.fill(BLACK)

    pg.draw.rect(SCREEN, WHITE, player1)
    pg.draw.rect(SCREEN, WHITE, player2)
    pg.draw.rect(SCREEN, WHITE, ball)
    SCREEN.blit(player1_point_text, (230, 480))
    SCREEN.blit(player2_point_text, (705, 480))

    pg.display.update()

def movement(keys_press, player1, player2):
    # pylint: disable=no-member
    '''Defines what keys to press for which player movement'''
    if keys_press[pg.K_w] and player1.y - VEL >= 0:
        player1.y -= VEL
    if keys_press[pg.K_s] and player1.y + VEL <= HEIGHT - 100:
        player1.y += VEL

    if keys_press[pg.K_UP] and player2.y - VEL >= 0:
        player2.y -= VEL
    if keys_press[pg.K_DOWN] and player2.y + VEL <= HEIGHT - 100:
        player2.y += VEL


def ball_start(ball):
    '''starts the ball off in the center at a random y coordinate'''
    ball.x = BALL_CENTER
    ball.y = rand.randint(25,495)

def ball_ball_direction(ball, ball_direction, y_vel):
    '''what decides if the ball will move left or right. 1 = right, 2 = left'''
    match ball_direction:
        case 1:
            ball.x += VEL
        case 2:
            ball.x -= VEL
    ball.y += y_vel

def hit_ceil_floor(ball, y_vel):
    '''returns true if the ball hits the floor or ceiling'''
    ceil = 494.5
    floor = 0
    if ball.y > ceil or ball.y < floor:
        return -(y_vel)
    return y_vel

def trajectory(ball, player, y_vel):
    '''determines the trajectory of the ball after hit with paddle'''
    ball_midpoint = ball.y + 12.5
    player_midpoint = player.y + 50
    if ball_midpoint > player_midpoint:
        y_vel = rand.randint(1,5)
    if ball_midpoint  < player_midpoint:
        y_vel = rand.randint(-5,-1)
    if ball_midpoint == player_midpoint:
        y_vel = 0
    return y_vel

def draw_menu(menu_select):
    '''renders the main'''
    SCREEN.fill(YELLOW)

    welcome_text = WELCOME_MENU_FONT.render('WELCOME TO PONG', 1, WHITE)
    play_text = MENU_FONT.render('PLAY', 1, WHITE)
    exit_text = MENU_FONT.render('QUIT', 1, WHITE)

    menu_play_blackbox = (350, 171, 250, 107)
    menu_quit_blackbox = (350, 315, 250, 107)

    if menu_select == 0:
        menu_play_blackbox = (350, 171, 250, 107)
        pg.draw.rect(SCREEN, BLACK, menu_play_blackbox)
    if menu_select == 1:
        menu_quit_blackbox = (350, 315, 250, 107)
        pg.draw.rect(SCREEN, BLACK, menu_quit_blackbox)

    SCREEN.blit(welcome_text, (92.5, 60.5))
    SCREEN.blit(play_text, (357.5, 186))
    SCREEN.blit(exit_text, (361, 330))

    pg.display.update()

def draw_again(score1, score2, menu_select):
    '''menu presented after a game is played'''

    SCREEN.fill(YELLOW)

    if score1 == 10:
        winner = 'PLAYER 1 WINS! PLAY AGAIN?'
    if score2 == 10:
        winner = 'PLAYER 2 WINS! PLAY AGAIN?'

    winner_text = AGAIN_MENU_FONT.render(winner, 1, WHITE)
    yes_text = MENU_FONT.render('YES', 1, WHITE)
    no_text = MENU_FONT.render('NO', 1, WHITE)

    if menu_select == 0:
        menu_play_blackbox = (376, 171, 198, 107)
        pg.draw.rect(SCREEN, BLACK, menu_play_blackbox)
    if menu_select == 1:
        menu_quit_blackbox = (376, 315, 198, 107)
        pg.draw.rect(SCREEN, BLACK, menu_quit_blackbox)

    SCREEN.blit(winner_text, (55.5, 60.5))
    SCREEN.blit(yes_text, (383.5, 186))
    SCREEN.blit(no_text, (406, 330))

    pg.display.update()


def main():
    # pylint: disable=no-member
    '''main method. initializes variables and handles in-game events'''
    while True:

        menu_select = 0
        player1 = pg.Rect(50, 210, PLAYER_WIDTH, PLAYER_HEIGHT)
        player2 = pg.Rect(875, 210, PLAYER_WIDTH, PLAYER_HEIGHT)
        ball = pg.Rect(412.5, 247.5, 25, 25)
        score1 = 0
        score2 = 0
        goal_line_1 = 875
        goal_line_2 = 72
        reset_point_2 = -500
        reset_point_1 = WIDTH + 500
        ball_direction = rand.randint(1,2)
        clock = pg.time.Clock()
        running = True
        menu = 0
        again = True
        y_vel = 0
        pg.draw.rect(SCREEN, WHITE, player1)
        ball_start(ball)

        while menu == 0:
            clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

            keys_press = pg.key.get_pressed()

            if keys_press[pg.K_RETURN]:
                if menu_select == 0:
                    menu += 1
                if menu_select == 1:
                    sys.exit()
            if keys_press[pg.K_s]:
                if keys_press[pg.K_w] is False:
                    menu_select = 1
            if keys_press[pg.K_w]:
                menu_select = 0

            draw_menu(menu_select)

        while running and score1 < 10 and score2 < 10:
            clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    sys.exit()

            keys_press = pg.key.get_pressed()

            movement(keys_press, player1, player2)

            y_vel = hit_ceil_floor(ball, y_vel)

            if ball.x > goal_line_1:
                if ball.x > reset_point_1:
                    ball_direction = 2
                    score1 += 1
                    y_vel = rand.randint(-5,5)
                    ball_start(ball)
            if ball.x < goal_line_2:
                if ball.x < reset_point_2:
                    ball_direction = 1
                    score2 += 1
                    y_vel = rand.randint(-5,5)
                    ball_start(ball)

            if pg.Rect.colliderect(player1, ball) and ball.x > goal_line_2:
                ball_direction = 1
                y_vel = trajectory(ball, player1, y_vel)
            if pg.Rect.colliderect(player2, ball) and ball.x < goal_line_1:
                ball_direction = 2
                y_vel = trajectory(ball, player2, y_vel)

            ball_ball_direction(ball, ball_direction, y_vel)
            draw_window(player1, player2, ball, score1, score2)

        while again:
            clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    menu = False
                    sys.exit()

            keys_press = pg.key.get_pressed()

            if keys_press[pg.K_RETURN]:
                if menu_select == 0:
                    again = False
                if menu_select == 1:
                    sys.exit()
            if keys_press[pg.K_s]:
                if keys_press[pg.K_w] is False:
                    menu_select = 1
            if keys_press[pg.K_w]:
                menu_select = 0

            draw_again(score1, score2, menu_select)

if __name__ == "__main__":
    main()
