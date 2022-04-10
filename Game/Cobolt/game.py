import pygame,random,math
import sys
import os

# настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

#звук
sound_floder = os.path.join(game_folder,'sound')
pygame.mixer.init()
Chanel_1 = pygame.mixer.Channel(0)

#удобные, помогающие функции
def select_img(x):
    return  pygame.image.load(os.path.join(img_folder, x))
def select_sound(x):
    return  pygame.mixer.Sound(os.path.join(sound_floder,x))
def create_hash(name,png):
    Hash = {}
    for i in range(len(png)):
        Hash[name[i]] = png[i]
    return Hash
# функция определяет знак и выводит 1 0 -1 - используется в основном для передвижения врага
def sign(x):
    if x>0:
        return 1
    if x == 0:
        return 0
    if x<0:
        return -1

# создаём хеш таблицы для боле удобного использования png файлами, после создания кадой таблицы
# массивы удалятся, код написан в таком порядке чтобы экономить память насколько это возможно
player_img_name = ['down','up','right','left']
player_img = [select_img('P_down.png'),select_img('P_up.png'),select_img('P_right.png'),select_img('P_left.png')]
player_img_map = create_hash(player_img_name,player_img)
del player_img_name,player_img

enemy_img_name = ['normal','alert','angry']
enemy_img = [select_img('enemy.png'),select_img('enemy_alert.png'),select_img('enemy_angry.png')]
enemy_img_map = create_hash(enemy_img_name,enemy_img)
del enemy_img_name,enemy_img

Obj_img_name = ['Obj','tree','xp','apple','bush']
Obj_img = [select_img('Obj_img.png'),select_img('Tree.png'),select_img('xp.png'),select_img('apple.png'),select_img('bush_1_mid.png')]
Obj_img_map = create_hash(Obj_img_name,Obj_img)
del Obj_img_name,Obj_img

#иконка окна "деревце"
icon = Obj_img_map['tree']
# пока что единственный созданный звук - звук врага
alert_sound = select_sound('alert.mp3')

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

#  главные параметры "настройки" - от них зависит сложность
player_SPEED = 4
player_Dash_co = 3
player_Hp = 30
player_dmg = 10

enemy_view = 200
enemy_speed = player_SPEED/2
enemy_hp = 20
enemy_dmg = 10

# классы с функциями и наследованиями, если их можно так назвать
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

#не хочу создавать кучу классов для каждого статичного объекта, они почти идентичны, только функции и картинка отличаются
# а структура переменных ты же, пытаюсь придумать хитрость


class NPC(Obj):
    def __init__(self,x,y,hp,dmg,img):
        self.hp = hp
        self.dmg = dmg
        super().__init__(x,y,img)
# управление персонажем реализовано в функции udate
class Player(NPC):
    def __init__(self,x,y,hp,dmg):
        self.catch = False
        self.catch_timer = 0
        super().__init__(x,y,hp,dmg,img = player_img_map['down'])
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
            self.image = player_img_map['left']
        if keystate[pygame.K_d]:
            self.speedx = player_SPEED * dash_co
            self.image = player_img_map['right']
        if keystate[pygame.K_w]:
            self.speedy = -player_SPEED * dash_co
            self.image = player_img_map['up']
        if keystate[pygame.K_s]:
            self.speedy = player_SPEED * dash_co
            self.image = player_img_map['down']
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # рамка выделяющая спрайт
        self.border = (0, 0, self.rect.width, self.rect.height)
        pygame.draw.rect(self.image, self.border_color, self.border, 2)

class Enemy(NPC):
    def __init__(self,x,y,hp,dmg):
        self.catch = False
        self.catch_timer = 0
        super().__init__(x,y,hp,dmg,img = enemy_img_map['normal'])
    def update(self):
        #перемещение
        cord_dif_x = player_1.rect.x - self.rect.x
        cord_dif_y = player_1.rect.y - self.rect.y


        if ( math.sqrt(cord_dif_x**2 + cord_dif_y**2) <= enemy_view):
            if (self.catch==False):
                self.catch_timer = pygame.time.get_ticks()
                self.image = enemy_img_map['alert']
                self.catch = True
                Chanel_1.play(alert_sound)
            if pygame.time.get_ticks() > self.catch_timer + 300:
                self.rect.x += enemy_speed*sign(cord_dif_x)
                self.rect.y += enemy_speed*sign(cord_dif_y)
                self.image = enemy_img_map['angry']
        else:
            self.catch = False
            self.image = enemy_img_map['normal']

pygame.init() #инициаллизация всех игровых объедков
pygame.mixer.init()  # инициализация звука
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаём экран)
pygame.display.set_caption("Cobolt") # экран
pygame.display.set_icon(icon) # иконка дерева - если вы помните (icon) была объявлена еще до структур
clock = pygame.time.Clock()


player_1 = Player(WIDTH/2,HEIGHT/2,player_Hp,player_dmg) # создаём спрайт класса "игрок"
enemy_1 = Enemy(WIDTH/2 + 400,HEIGHT/2 ,enemy_hp,enemy_dmg) # спрайт класса вражина

# распределяем спрайты на группы - так надо, это важно
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
static_sprites = pygame.sprite.Group()

enemy_sprites.add(enemy_1)
all_sprites.add(player_1,enemy_sprites,static_sprites) # добавляем объект в спрайты

# заполняем экран цветастостью
screen.fill(map_color)


run = True
while run:
    clock.tick(FPS)
    #print(clock)
    #print(player_1.get_cord())

    # Ввод процесса (события)

    # тут могла быть ваша реклама, но даже её нет
    # всё потому что ввод клавиш(как таковых событий) - осущетвляется в update игрока

    # Обновление всех спрайтов
    # не забываем что внути udate прописаны event для управления
    all_sprites.update()

    #обработка событий
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT: # работа "крестика"
            run = False # завершает цикл

    #Рендеринг
    screen.fill(map_color)
    all_sprites.draw(screen)


    pygame.draw.circle(screen, BLACK,enemy_1.rect.center, enemy_view,5)
    # Визуализация (сборка)
    pygame.display.flip() # отрисовка