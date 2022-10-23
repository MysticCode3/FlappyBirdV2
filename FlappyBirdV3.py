import pygame
import random
import sys

from win32api import GetSystemMetrics

#screen_width = GetSystemMetrics(0)
#screen_height = GetSystemMetrics(1)

screen_width = 900
screen_height = 504
screen = pygame.display.set_mode((900, 604))
#screen = pygame.display.set_mode((1500, 1000))
clock = pygame.time.Clock()
pipes = []
floors = []
bird = None

green_color = 150, 200, 20
blue_color = 67, 84, 255
orange_color = 255, 165, 0
red_color = 250, 0, 0
purple_color = 172, 79, 198
gray_color = 128, 128, 128

background = pygame.image.load('flappybird_background.png')

total_points = 0
best_score = 0

reset_color = (255, 255, 255)

cx, cy = 0, 0
mx, my = 0, 0

def init_game():
    global bird
    global pipes
    global floors

    # BIRD
    bird = BIRD(screen_width / 2, screen_height / 2 + 25, 0.25)

    # PIPES
    pipes = []
    pipes.append(PIPE(1000, screen_height - 270))
    pipes.append(PIPE(1325, screen_height - 100))
    pipes.append(PIPE(1650, screen_height - 150))
    pipes.append(PIPE(1975, screen_height - 175))

    # FLOOR
    floors = []
    floors.append(FLOOR(0, screen_height - 10, 3.5))
    floors.append(FLOOR(310, screen_height - 10, 3.5))
    floors.append(FLOOR(620, screen_height - 10, 3.5))
    floors.append(FLOOR(930, screen_height - 10, 3.5))

def game_end():
    global reset_color
    global mx, my
    global cx, cy

    for pipe in pipes:
        pipe.change_vel(0)

    for floor in floors:
        floor.change_vel(0)

    reset_label = font.render("RESET", bool(1), reset_color)
    screen.blit(reset_label, (screen_width / 2 - 75, screen_height/2-100))

    best_score_label = font.render(f"BEST SCORE: {best_score}", bool(1), (255, 255, 255))
    screen.blit(best_score_label, (screen_width / 2 - 175, screen_height + 10))

    if 374 < mx < 540:
        if 165 < my < 209:
            reset_color = red_color
        else:
            reset_color = (255, 255, 255)
    else:
        reset_color = (255, 255, 255)

    if 374 < cx < 540:
        if 165 < cy < 209:
            cx, cy = 0, 0
            #reset_game(pipes, floors)
            init_game()


def collision_1(a, b):
    if a.bottom_rect != None and b.rect != None:
        if a.bottom_rect.colliderect(b.rect):
            return 'Y'
    if a.top_rect != None and b.rect != None:
        if a.top_rect.colliderect(b.rect):
            return 'Y'
    return 'N'

class BIRD():
    def __init__(self, x, y, gravity):
        self.x, self.y = x, y
        self.gravity = gravity
        self.bird_image = pygame.image.load('flappy_bird.png')
        self.new_x, self.new_y = 0, 0
        self.lost = False
        self.game_start = False
        self.flap_position = 1
        self.flap_time = 0.1
        self.points = 0
        self.bird_downflap = pygame.image.load('yellowbird-downflap.png').convert_alpha()
        self.bird_midflap = pygame.image.load('yellowbird-midflap.png').convert_alpha()
        self.bird_upflap = pygame.image.load('yellowbird-upflap.png').convert_alpha()

        self.bird_downflap_rotated = pygame.image.load('yellowbird-downflap.png')
        self.bird_midflap_rotated = pygame.image.load('yellowbird-midflap.png')
        self.bird_upflap_rotated = pygame.image.load('yellowbird-upflap.png')

        self.rect_width, self.rect_height = 65, 50
        self.rect = None
        self.bird_mv = 0
        self.down = False
        self.up = True
        self.start_grav = 0.25
        self.start_mv = 0

    def draw(self):
        self.new_x = self.x - 20
        self.new_y = self.y - 20
        self.bird_image = pygame.transform.scale(self.bird_image, (80, 80))
        self.bird_downflap = pygame.transform.scale(self.bird_downflap, (65, 50))
        self.bird_midflap = pygame.transform.scale(self.bird_midflap, (65, 50))
        self.bird_upflap = pygame.transform.scale(self.bird_upflap, (65, 50))
        self.rect = pygame.Rect((self.new_x, self.new_y), (self.rect_width, self.rect_height))
        #pygame.draw.rect(screen, (255, 0, 0), self.bird_rect)

        self.bird_downflap_rotated, self.bird_midflap_rotated, self.bird_upflap_rotated = self.change_rotation()

        if self.y == screen_height - 17 - 23:
            screen.blit(self.bird_downflap_rotated, (self.new_x, self.new_y))
        else:
            if self.flap_position < 2:
                screen.blit(self.bird_downflap_rotated, (self.new_x, self.new_y))
            if 2 < self.flap_position < 3:
                screen.blit(self.bird_midflap_rotated, (self.new_x, self.new_y))
            if 3 < self.flap_position < 4.2:
                screen.blit(self.bird_upflap_rotated, (self.new_x, self.new_y))

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.game_start = True
            self.bird_mv = 0
            self.bird_mv -= 6

        if self.y < screen_height - 17 - 35:
            if self.game_start:
                self.bird_mv += self.gravity
                self.y += self.bird_mv
        else:
            bird.change_lost(True)
            game_end()

        if self.y > screen_height - 17 - 35:
            self.y = screen_height - 17 - 23

        if self.game_start == False:
            if self.up:
                self.start_mv += self.start_grav
                self.y -= self.start_mv
            if self.down:
                self.start_mv += self.start_grav
                self.y += self.start_mv
            #LOGIC
            if self.y >= screen_height/2+10:
                self.start_mv = 0
                self.up = True
                self.down = False
            if self.y <= screen_height/2-10:
                self.start_mv = 0
                self.up = False
                self.down = True

    def update_flaps(self):
        if self.flap_position < 2:
            self.flap_position += self.flap_time
        elif self.flap_position < 3:
            self.flap_position += self.flap_time
        elif self.flap_position < 4:
            self.flap_position += self.flap_time
        elif self.flap_position >= 4:
            self.flap_position = 1

    def change_rotation(self):
        self.bird_downflap_rotated = pygame.transform.rotozoom(self.bird_downflap, -self.bird_mv*2, 1)
        self.bird_midflap_rotated = pygame.transform.rotozoom(self.bird_midflap, -self.bird_mv*2, 1)
        self.bird_upflap_rotated = pygame.transform.rotozoom(self.bird_upflap, -self.bird_mv*2, 1)
        return self.bird_downflap_rotated, self.bird_midflap_rotated, self.bird_upflap_rotated

    def return_x_y(self):
        return self.x, self.y

    def change_lost(self, new_val):
        self.lost = new_val

    def change_gravity(self, new_val):
        self.gravity = new_val

    def change_x_y(self, new_val_x, new_val_y):
        self.x, self.y = new_val_x, new_val_y

    def change_game_start(self, new_val):
        self.game_start = new_val

    def change_jump(self, new_val):
        self.jump = new_val

    def change_bird_mv(self, new_val):
        self.bird_mv = new_val

class PIPE():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.bird_x, self.bird_y = 0, 0
        self.pipe_image_bottom = pygame.image.load('pipe-green.png')
        self.pipe_image_top = pygame.image.load('pipe-green.png')
        self.bottom_rect_width, self.bottom_rect_height = 100, 400
        self.bottom_rect = None
        self.top_rect_width, self.top_rect_height = 100, 400
        self.top_rect = None
        #self.pipe_image_top = pygame.transform.rotate(self.pipe_image_top, 180)
        self.pipe_image_top = pygame.transform.flip(self.pipe_image_bottom, False, True)
        self.times = 1
        self.vel = 3.5

    def draw(self):
        self.bottom_rect = pygame.Rect((self.x, self.y), (self.bottom_rect_width, self.bottom_rect_height))
        #pygame.draw.rect(screen, (255, 0, 0), self.bottom_rect)
        self.pipe_image_bottom = pygame.transform.scale(self.pipe_image_bottom, (100, 400))
        screen.blit(self.pipe_image_bottom, (self.x, self.y))

        self.top_rect = pygame.Rect((self.x, self.y-600), (self.top_rect_width, self.top_rect_height))
        #pygame.draw.rect(screen, (255, 0, 0), self.top_rect)
        self.pipe_image_top = pygame.transform.scale(self.pipe_image_top, (100, 400))
        screen.blit(self.pipe_image_top, (self.x, self.y-600))

    def update(self):
        self.x -= self.vel
        if self.x < 0 - 200:
            self.x = screen_width + 200
            self.y = random.randint(screen_height-270, screen_height-50)
            self.times = 1

        if self.x + 100 > bird.x > self.x + 90:
            if self.times == 1:
                self.times -= 1
                bird.points += 1

    def change_vel(self, new_val):
        self.vel = new_val

    def change_x_y(self, new_x, new_y):
        self.x, self.y = new_x, new_y

class FLOOR():
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
        self.floor_image = pygame.image.load('flappyBirdFloor.png')
        #self.floor_image = pygame.image.load('Grass.png')

    def draw(self):
        self.floor_image = pygame.transform.scale(self.floor_image, (320, 112))
        screen.blit(self.floor_image, (self.x, self.y))

    def update(self):
        self.x -= self.vel
        if self.x+320 < 0:
            self.x = screen_width

    def change_vel(self, new_val):
        self.vel = new_val

pygame.init()
init_game()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            cx, cy = pygame.mouse.get_pos()
            print(cx, cy)

    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_1]:
        pygame.quit()
        sys.exit()

    screen.fill((30, 30, 30))
    font = pygame.font.SysFont("comicsansms", 50)

    #BACKGROUND
    screen.blit(background, (0, 0))

    #PIPES
    if bird.game_start:
        for pipe in pipes:
            pipe.draw()
            pipe.update()
            if collision_1(pipe, bird) == 'Y':
                bird.change_lost(True)
                bird.change_gravity(15)
                game_end()

    #FLOOR
    for floor in floors:
        floor.draw()
        floor.update()

    total_points_label = font.render(str(bird.points), bool(1), (255, 255, 255))
    screen.blit(total_points_label, (screen_width/2-10, 25))

    #BEST SCORE
    if bird.points > best_score:
        best_score = bird.points

    #BIRD
    bird.draw()
    bird.update()
    bird.update_flaps()

    current_color = pygame.Surface.get_at_mapped(screen, (screen_width - 10, screen_height - 10))
    #print(current_color)

    pygame.display.update()
    clock.tick(60)