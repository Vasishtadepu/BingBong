import pygame
import os
import random
pygame.init()
pygame.font.init()
pygame.mixer.init()

# defining window constants
width = 900
height = 500
holder_x = 60

score_font = pygame.font.SysFont('comicsans', 50)
final_font = pygame.font.SysFont('comicsans', 100)

grenade = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
silencer = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# defining random positions for numbers
X = [72, 356, 493, 0, 180, 780, 922, 566, 278, 228, 131, 180, 390, 670, 990,
     1200, 1650, 1523, 1350, 2000, 1976, 1460, 2397, 2212, 1150, 3157, 3330]


# defining colors
cblack = (0, 0, 0)
cwhite = (255, 255, 255)
cred = (240, 0, 0)

# defining user events
hit_holder = pygame.USEREVENT+1
player_hit = pygame.USEREVENT + 2

# definig up and bottom holders
top = pygame.Rect(holder_x, 0, 10, 25)
bottom = pygame.Rect(holder_x, height-25, 10, 25)

# defining obstacles array
obstacles = []

# defining obstacles formation


def generate_obs(obstacles, score):
    obstacles_num = (score//7)+2
    if len(obstacles) < obstacles_num:
        if len(obstacles) > 0:
            object = pygame.Rect(random.randint(
                50, 1000)+obstacles[len(obstacles)-1].x+200, random.randint(1, 11)*35, 50, 50)
            obstacles.append(object)
        else:
            object = pygame.Rect(900, random.randint(1, 11)*35, 50, 50)
            obstacles.append(object)


def obs_movement(obstacles, player):
    for obs in obstacles:
        obs.x -= 7
        if player.colliderect(obs):
            pygame.event.post(pygame.event.Event(player_hit))
            obstacles.clear()
        if obs.x <= 0:
            if len(obstacles) > 0:
                obstacles.remove(obs)

# defining user events


win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bing Bong!")
fps = 60

# defining main display window


def display_window(player, score, obstacles, color):
    win.fill(cblack)
    score_text = score_font.render("Score:" + str(score), 1, cwhite)
    win.blit(score_text, (width-score_text.get_width() -
             10, height-score_text.get_height()-10))
    for obs in obstacles:
        pygame.draw.rect(win, cwhite, obs)
    pygame.draw.rect(win, cwhite, top)
    pygame.draw.rect(win, cwhite, bottom)
    pygame.draw.rect(win, color, player)
    pygame.display.update()

# defining what happens when player hits holder


def player_moving(player, top, bottom):
    if player.y<=25 or player.y+player.height>=height-25:
        pygame.event.post(pygame.event.Event(hit_holder))


def draw_score(text):
    score = final_font.render("Final Score:" + str(text), 1, cwhite)
    win.blit(score, (width//2-score.get_width() //
             2, height//2-score.get_height()//2))
    pygame.display.update()
    pygame.time.delay(1000)
# writing the main game loop


def main():
    run = True
    clock = pygame.time.Clock()
    while(run):
        clock.tick(fps)
        win.fill(cblack)
        main_menu_text = final_font.render("Hit Space bar to Play", 1, cwhite)
        win.blit(main_menu_text, (width//2-main_menu_text.get_width() //
                 2-10//2, height//2-main_menu_text.get_height()//2-50))
        exit_text = final_font.render("Q to exit", 1, cwhite)
        win.blit(exit_text, (width//2-exit_text.get_width()//2 -
                 10//2, height//2-exit_text.get_height()//2+30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
        pygame.display.update()


def game():
    # making the player blob
    player = pygame.Rect(holder_x+5-20, height//2-50, 40, 40)
    score = 0
    player_vel = 5
    player_out = ""
    player_vel_slow = 2
    clock = pygame.time.Clock()
    run = True
    while(run):
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == hit_holder:
                player_vel = -player_vel
                player_vel_slow = -player_vel_slow
                score += 1

                silencer.play()
            if event.type == player_hit:
                player_out = "!"
                grenade.play()

        if player_out != "":
            draw_score(score)
            break

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            player.y += player_vel_slow
            color = cred
            if player.width < 60 and player.y+player.height+10 < 500-30 and player.y > player.width+10:
                player.width += 1
                player.height = player.width
        else:
            player.y += player_vel
            color = cwhite
            if player.width > 40 and player.y+player.height+10 < 500-30 and player.y > player.width+10:
                player.width -= 1
                player.height = player.width

        generate_obs(obstacles, score)
        obs_movement(obstacles, player)
        player_moving(player, top, bottom)
        display_window(player, score, obstacles, color)

    main()


if __name__ == "__main__":
    main()
