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
# выбрать фото по имени
def select_img(x):
    return  pygame.image.load(os.path.join(img_folder, x))
#выбрать звук по имени
def select_sound(x):
    return  pygame.mixer.Sound(os.path.join(sound_floder,x))
#создание Хэш - таблицы
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
#отслеживание пересечения 2х прямоугольных областей
def intersection(rect_1,rect_2):
    if rect_1.right > rect_2.left and \
   rect_1.left < rect_2.right and \
   rect_1.bottom > rect_2.top and \
   rect_1.top < rect_2.bottom:
        return 1
    else:
        return 0

# создаём хеш таблицы для боле удобного использования png файлами, после создания кадой таблицы
# массивы удалятся, код написан в таком порядке чтобы экономить память насколько это возможно
player_img_name = ['down','up','right','left','down_hit','up_hit','right_hit','left_hit']
player_img = [select_img('P_down.png'),select_img('P_up.png'),select_img('P_right.png'),select_img('P_left.png'),
              select_img('P_down_hit.png'),select_img('P_up_hit.png'),select_img('P_right_hit.png'),select_img('P_left_hit.png')]
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

map_color = BLUE
map_border = pygame.math.Vector2(4000,2000)

#  главные параметры "настройки" - от них зависит сложность
player_SPEED = 5
player_Dash_co = 3
player_Hp = 50
player_dmg = 10

#требует срочной доработки для удобной настройки
player_hit_range = 32
player_hit_rad = 128


enemy_view = 200
enemy_speed = player_SPEED/2
enemy_hp = 30
enemy_dmg = 10


# создаём группы спрайтов - надо над ними будет поработать :)
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
static_sprites = pygame.sprite.Group()

# классы с функциями и наследованиями, если их можно так назвать
class Obj(pygame.sprite.Sprite):
    def __init__(self,pos,img):
        pygame.sprite.Sprite.__init__(self)
        # image - отображение
        self.image = img
        self.border_color = BLUE
        # rect - такого же размера, что и спрайт
        self.rect = self.image.get_rect(center = pos)
        # рамка выделяющая спрайт
    def paint_border(self):
        self.border = (0, 0, self.rect.width, self.rect.height)
        pygame.draw.rect(self.image, self.border_color, self.border, 3)
    def get_cord(self):
        return [self.rect.x + 32,self.rect.y+32]

#не хочу создавать кучу классов для каждого статичного объекта, они почти идентичны, только функции и картинка отличаются
# а структура переменных та же, пытаюсь придумать хитрость

# на данном этапе просто придерживаюсь парадигмы наследования от абстрактного класса, возможно перепишу все структуры к чертям чтоь позже
class Static_obj(Obj):
    def __init__(self,pos,type):
        self.type = type
        super().__init__(pos,img = Obj_img_map[type])

class Tree(Static_obj):
    def __init__(self,pos,type):
        super().__init__(pos,type='tree')
        # твёрдый объект
        self.solid_x = self.rect.x+120
        self.solid_y = self.rect.y+265
        self.solid = pygame.rect.Rect(self.solid_x, self.solid_y, 30, 120)
        self.solid_border = (120,265,30,120)
    def update(self):
        self.paint_border()
        pygame.draw.rect(self.image,RPURPLE,self.solid_border,3)

class NPC(Obj):
    def __init__(self,pos,hp,dmg,img):
        self.hp = hp
        self.dmg = dmg
        super().__init__(pos,img)

class Player(NPC):
    def __init__(self,pos):
        super().__init__(pos,hp = player_Hp,dmg = player_dmg,img = player_img_map['down'])
        self.side = 'down'
        self.hit_time_dist = 500
        self.hit_time = 0
        self.hit_time_anim = 200
        self.direction = pygame.math.Vector2()
        self.speed = player_SPEED
    def input(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.direction.x = -1
            self.side = 'left'
        elif keystate[pygame.K_d]:
            self.direction.x = 1
            self.side = 'right'
        else:
            self.direction.x = 0
            self.side = 'down'

        if keystate[pygame.K_w]:
            self.direction.y = -1
            self.side = 'up'
        elif keystate[pygame.K_s]:
            self.direction.y = 1
            self.side = 'down'
        else:
            self.direction.y = 0

    def update(self):
        self.input()
        if self.hit_time+self.hit_time_anim <= pygame.time.get_ticks():
            self.image = player_img_map[self.side]
            self.rect.center += self.direction * self.speed
            if self.rect.x + 32 < 0:
                self.rect.x +=self.speed
            if self.rect.x + 32 > map_border.x:
                self.rect.x -=self.speed
            if self.rect.y + 32 < 0:
                self.rect.y +=self.speed
            if self.rect.y + 32 > map_border.y:
                self.rect.y -=self.speed
        self.paint_border()

    def hit(self):
        self.hit_time = pygame.time.get_ticks()
        hit_x = self.rect.centerx
        hit_y = self.rect.centery
        if (self.direction.y!=0 or self.direction == (0,0)):
            hit_w = player_hit_rad
            hit_h = player_hit_range
            hit_x+= -32 + 32*(self.direction.x-1)
            hit_y+=-15 + 45*self.direction.y
            if self.direction == (0,0):
                hit_y+=45
        elif self.direction.y==0:
            hit_x+=-15 + 45*self.direction.x
            hit_y+=-32 + 32*(self.direction.y-1)
            hit_w = player_hit_range
            hit_h = player_hit_rad
        self.side+='_hit'
        self.image = player_img_map[self.side]
        hit_rect = pygame.rect.Rect(hit_x, hit_y,hit_w,hit_h)
        self.paint_border()
        return hit_rect

class Enemy(NPC):
    def __init__(self,pos,hp,dmg):
        self.catch = False
        self.catch_timer = 0
        self.stop = False
        super().__init__(pos,hp,dmg,img = enemy_img_map['normal'])
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
                self.image = enemy_img_map['angry']
                self.rect.x += enemy_speed*sign(cord_dif_x)
                self.rect.y += enemy_speed*sign(cord_dif_y)
        else:
            self.catch = False
            self.image = enemy_img_map['normal']
        self.paint_border()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0]// 2
        self.half_h = self.display_surface.get_size()[1]// 2
        # ground
        self.ground_surf = select_img('map.png')
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self,player):

        self.center_target_camera(player)

        #ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf,ground_offset)

        #active elements
        for sprite in sorted(self.sprites(),key=lambda  sprite:sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

def Create_Arr_SO(count,x,y,distace,type):
    Result_Arr = [0]*count
    m = 0
    real_type = Static_obj
    if type == 'tree':
        real_type = Tree
    for i in range(0,count):
        Result_Arr[i]  = real_type((x+m,y),type)
        m+=distace
    return Result_Arr

pygame.init() #инициаллизация всех игровых объедков
pygame.mixer.init()  # инициализация звука
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаём экран)
pygame.display.set_caption("Cobolt") # экран
pygame.display.set_icon(icon) # иконка дерева - если вы помните (icon) была объявлена еще до структур
clock = pygame.time.Clock()

player_1 = Player((100,100)) # создаём спрайт класса "игрок"
enemy_1 = Enemy((600,700),enemy_hp,enemy_dmg) # спрайт класса вражина

#Some_OBJ_Arr = Create_Arr_SO(2,WIDTH/2-500,HEIGHT/2+100,400,'bush')
Tree_Arr = Create_Arr_SO(7,900,500,800,'tree')

camera_group = CameraGroup()

static_sprites.add(Tree_Arr)
enemy_sprites.add(enemy_1)
all_sprites.add(player_1,enemy_sprites,static_sprites) # добавляем объекты в группы
camera_group.add(all_sprites)

hit_s = pygame.rect.Rect(0,0,0,0)

# заполняем экран цветастостью
screen.fill(map_color)

run = True
while run:

    clock.tick(FPS)
    #print(pygame.time.get_ticks())
    timer = pygame.time.get_ticks()
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
    # удар через определённое время
    if pygame.key.get_pressed()[pygame.K_o] and player_1.hit_time + player_1.hit_time_dist <= timer:
        hit_s = player_1.hit()
    #elif (player_1.hit_time + player_1.hit_time_anim <= timer):
    else:
        hit_s = pygame.rect.Rect(0,0,0,0)
     #сырой алгоритм, но ничего не поделаешь - чем больше деревьев, тем медленнее работает при пересечении
    if pygame.sprite.spritecollideany(player_1,Tree_Arr):
        for i in range(len(Tree_Arr)):
            if (intersection(Tree_Arr[i].solid,player_1.rect)):
                where_x = sign(Tree_Arr[i].solid.centerx - player_1.rect.centerx)
                where_y = sign(Tree_Arr[i].solid.centery - player_1.rect.centery)
                player_1.rect.x-=where_x*player_SPEED
                player_1.rect.y-=where_y*player_SPEED



    if intersection(hit_s,enemy_1.rect):
        enemy_1.hp-=player_1.dmg
    if enemy_1.hp<1:
        enemy_1.kill()

    #Рендеринг
    screen.fill(map_color)
    camera_group.custom_draw(player_1)

    pygame.draw.rect(camera_group.ground_surf,RED,hit_s,4)
    pygame.draw.circle(camera_group.ground_surf, BLACK,enemy_1.rect.center, enemy_view,5)
    # Визуализация (сборка)
    pygame.display.flip() # отрисовка
