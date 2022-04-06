import pygame,random
import sys
import os

# настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
icon = pygame.image.load(os.path.join(img_folder, 'Tree.png'))
player_img = pygame.image.load(os.path.join(img_folder, 'player_down.png'))
enemy_img = pygame.image.load(os.path.join(img_folder, 'angry_cat.png'))

# 1280x800
# 1920x1080
WIDTH = 1280  # ширина игрового окна
HEIGHT = 800 # высота игрового окна
FPS = 60 # частота кадров в секунду

#просто цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RPURPLE = (185,0,105)

map_color = (65,66,1)


P_SPEED = 5
P_Dash_co = 3
enemy_view = 250
enemy_speed = P_SPEED/3

# создать родительский класс!

def sign(x):
    if x>0:
        return 1
    if x == 0:
        return 0
    if x<0:
        return -1

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        # image - отображение
        self.image = player_img
        # rect - такого же размера, что и спрайт
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        dash_co = 1
        #перемещение
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_p]:
            dash_co = P_Dash_co
            print(self.rect.right - self.rect.left,'\t', self.rect.bottom - self.rect.top)
        else:
            dash_co = 1
        if keystate[pygame.K_a]:
            self.speedx = -P_SPEED * dash_co
        if keystate[pygame.K_d]:
            self.speedx = P_SPEED * dash_co
        if keystate[pygame.K_w]:
            self.speedy = -P_SPEED * dash_co
        if keystate[pygame.K_s]:
            self.speedy = P_SPEED * dash_co
        self.rect.x += self.speedx
        self.rect.y += self.speedy


        # условия стен

        # левая стена
        #if self.rect.right < 0:
        #    self.rect.left = WIDTH
        # правая стена
        #if self.rect.left > WIDTH:
        #    self.rect.right = 0
        # верх
        #if self.rect.bottom < 0:
        #    self.rect.top = HEIGHT
        # низ
        #if self.rect.top > HEIGHT:
        #    self.rect.bottom = 0

    def get_cord(self):
        return [self.rect.x,self.rect.y]

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        # image - отображение
        self.image = enemy_img
        # rect - такого же размера, что и спрайт
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        #перемещение
        cord_dif_x = player_1.rect.x - self.rect.x
        cord_dif_y = player_1.rect.y - self.rect.y
        if (abs(cord_dif_x) + abs(cord_dif_y) < enemy_view): #and abs(cord_dif_x) + abs(cord_dif_y) > 70 ):
            self.rect.x += enemy_speed*sign(cord_dif_x)
            self.rect.y += enemy_speed*sign(cord_dif_y)
        # условия стен
        # левая стена
        #if self.rect.right < 0:
        #    self.rect.left = WIDTH
        # правая стена
        #if self.rect.left > WIDTH:
        #    self.rect.right = 0
        # верх
        #if self.rect.bottom < 0:
        #    self.rect.top = HEIGHT
        # низ
        #if self.rect.top > HEIGHT:
        #    self.rect.bottom = 0

    def get_cord(self):
        return [self.rect.x,self.rect.y]


pygame.init() #инициаллизация всех игровых объедков
pygame.mixer.init()  # инициализация звука
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаём экран)
pygame.display.set_caption("Cobolt") # экран
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

player_1 = Player(WIDTH/2,HEIGHT/2) # создаём спрайт класса "игрок"
enemy_1 = Enemy(WIDTH/2 + 100,HEIGHT/2 - 100)
enemy_2 = Enemy(WIDTH/2 + 200,HEIGHT/2 - 200)

all_sprites.add(player_1,enemy_1,enemy_2) # добавляем объект в спрайты

screen.fill(map_color)



run = True
while run:
    clock.tick(FPS)
    #print(clock)
    print(player_1.get_cord())


    # Ввод процесса (события)


    # Обновление
    all_sprites.update()
    #обработка событий
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT: # работа "крестика"
            run = False

    #Рендеринг
    screen.fill(map_color)
    all_sprites.draw(screen)
    
    # Визуализация (сборка)
    pygame.display.flip() # отрисовка