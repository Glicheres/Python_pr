import pygame,random,math
import sys
import os


# настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

def select_img(x):
    return  pygame.image.load(os.path.join(img_folder, x))

icon = select_img('Tree.png')
player_img = [select_img('P_down.png'),select_img('P_up.png'),select_img('P_right.png'),select_img('P_left.png')]
tree_img = select_img('Tree.png')
enemy_img = select_img('angry_cat.png')

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


player_SPEED = 4
player_Dash_co = 3
player_Hp = 30
player_dmg = 10

enemy_view = 150
enemy_speed = player_SPEED/2
enemy_hp = 20
enemy_dmg = 10

def sign(x):
    if x>0:
        return 1
    if x == 0:
        return 0
    if x<0:
        return -1

class Obj(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        # image - отображение
        self.image = img
        self.border_color = BLUE
        # rect - такого же размера, что и спрайт
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # рамка выделяющая спрайт
        self.border = (0, 0, self.rect.width, self.rect.height)
        pygame.draw.rect(self.image, self.border_color, self.border, 3)

    def get_cord(self):
        return [self.rect.x,self.rect.y]

class NPC(Obj):
    def __init__(self,x,y,img,hp,dmg):
        self.hp = hp
        self.dmg = dmg
        super().__init__(x,y,img)

class Player(NPC):
    def update(self):
        #перемещение
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_p]:
            dash_co = player_Dash_co
        else:
            dash_co = 1
        if keystate[pygame.K_a]:
            self.speedx = -player_SPEED * dash_co
            self.image = player_img[3]
        if keystate[pygame.K_d]:
            self.speedx = player_SPEED * dash_co
            self.image = player_img[2]
        if keystate[pygame.K_w]:
            self.speedy = -player_SPEED * dash_co
            self.image = player_img[1]
        if keystate[pygame.K_s]:
            self.speedy = player_SPEED * dash_co
            self.image = player_img[0]
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # рамка выделяющая спрайт
        self.border = (0, 0, self.rect.width, self.rect.height)
        pygame.draw.rect(self.image, self.border_color, self.border, 2)

class Enemy(NPC):
    def update(self):
        #перемещение
        cord_dif_x = player_1.rect.x - self.rect.x
        cord_dif_y = player_1.rect.y - self.rect.y


        #фокус с -  )
        if ( math.sqrt(cord_dif_x**2 + cord_dif_y**2) <= enemy_view):
            self.rect.x += enemy_speed*sign(cord_dif_x)
            self.rect.y += enemy_speed*sign(cord_dif_y)


pygame.init() #инициаллизация всех игровых объедков
pygame.mixer.init()  # инициализация звука
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаём экран)
pygame.display.set_caption("Cobolt") # экран
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

player_1 = Player(WIDTH/2,HEIGHT/2,player_img[0],player_Hp,player_dmg) # создаём спрайт класса "игрок"
enemy_1 = Enemy(WIDTH/2 + 100,HEIGHT/2 - 100,enemy_img,enemy_hp,enemy_dmg)
tree_1 = Obj(WIDTH/2 - 300,HEIGHT/2,tree_img)

enemy_sprites.add(enemy_1)
all_sprites.add(player_1,enemy_1,tree_1) # добавляем объект в спрайты


screen.fill(map_color)


run = True
while run:
    clock.tick(FPS)
    #print(clock)
    #print(player_1.get_cord())

    # Ввод процесса (события)

    # Обновление всех спрайтов
    all_sprites.update()
    #pygame.sprite.spritecollideany(player_1,enemy_sprites)
    #обработка событий
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT: # работа "крестика"
            run = False

    #Рендеринг
    screen.fill(map_color)
    all_sprites.draw(screen)

    #
    pygame.draw.circle(screen, BLACK,enemy_1.rect.center, enemy_view,5)
    # Визуализация (сборка)
    pygame.display.flip() # отрисовка