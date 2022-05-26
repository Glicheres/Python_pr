import time,pygame,random,math,os


# настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

#звук
sound_floder = os.path.join(game_folder,'sound')
pygame.mixer.init()
Chanel_1 = pygame.mixer.Channel(0)

front_floder = os.path.join(game_folder,'front')
pygame.font.init() # инициаллизация шрифтов
#удобные, помогающие функции
# выбрать фото по имени
def select_img(x):
    return  pygame.image.load(os.path.join(img_folder, x))
#выбрать звук по имени
def select_sound(x):
    return  pygame.mixer.Sound(os.path.join(sound_floder,x))
def select_front(x):
    return  pygame.font.Font(os.path.join(front_floder,'GangSmallYuxian.ttf'),x)

def check_button(x):
    return pygame.key.get_pressed()[x]
#создание Хэш - таблицы
def create_hash(name,png):
    Hash = {}
    for i in range(len(png)):
        Hash[name[i]] = png[i]
    return Hash

# пишу генератор/редактор
def read_text_file(name):
    f = open(name,'r')
    try:
        m = f.read()
    finally:
        f.close()
    return m
def write_text_file(name, Arr):
    s = str()
    for i in range(len(Arr)):
        for j in range(len(Arr[i])):
            s+=str(Arr[i][j])
        s+='\n'
    f = open(name,'w')
    try:
        m = f.write(s)
    finally:
        f.close()
    return name
# вернёт имя файла с рандомой "картой"(не png)
def save_random_map(x,y,tile_count,name):
    map_1 = str()
    for i in range(y):
        for j in range(x):
            map_1 += str(random.randint(1,tile_count))
        map_1 += '\n'
    map_1 +='.'
    print(map_1)
    write_text_file(name, map_1)
    return name

def text_to_map(text):
    #перезапись текста
    text_map = []
    map_line = []
    for i in range(len(text)):
        if text[i] =='\n':
            text_map.append(map_line)
            map_line = []
            #print('n: ',i)
        else:
            map_line.append(text[i])
    del map_line
    return text_map
# создаёт массив равномерно распределённых квадратов - сетку
def create_grid(map_ogc,power):
    rect_arr = [0]* int(map_ogc.y)
    for i in range(0,int(map_ogc.y)):
        col_1 = [0]* int(map_ogc.x)
        for j in range(0,int(map_ogc.x)):
            col_1[j] = pygame.rect.Rect(j*power,i*power,power,power)
            rect_arr[i] = col_1
    return rect_arr

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

# отрисовывает нашу карту на поверзность, которую возвращает, redactor(T/F)
# в file указываем изначальную пустую поверхность
def draw_map(redactor,map_file,text_file):
    change_camera_group = CameraGroup(map_file)
    tail_group = pygame.sprite.Group()
    text_map_obj = text_to_map(read_text_file(text_file))
    power = 200
    map_ogc = pygame.math.Vector2(int(map_border.x) // power,int(map_border.y) // power)
    grid_obj = create_grid(map_ogc,power)
    for i in range(0,int(map_ogc.y)):
        for j in range(0,int(map_ogc.x)):
            if (text_map_obj[i][j]!='.'):
                tail1 = Obj(grid_obj[i][j].center,tail_map[text_map_obj[i][j]])
                tail_group.add(tail1)
                tail_group.draw(change_camera_group.ground_surf)
                if redactor:
                    analog = pygame.transform.scale(change_camera_group.ground_surf,(1280,640))
                    screen.blit(analog,(0,0))
                    pygame.display.flip()
                #screen.blit(change_camera_group.ground_surf,(0,0))
                #pygame.display.flip()
                del tail1
    if redactor:
        result = analog
    else:
        result = change_camera_group.ground_surf
    del change_camera_group,tail_group
    return result


# создаём хеш таблицы для боле удобного использования png файлами, после создания кадой таблицы
# массивы удалятся, код написан в таком порядке чтобы экономить память насколько это возможно
tail = ['1','2','3','4','5','6','7']
tail_img = [select_img('tile1.png'),select_img('tile2.png'),select_img('tile3.png'),select_img('tile4.png'),select_img('tile5.png'),select_img('tile6.png'),select_img('tile7.png')]
tail_map = create_hash(tail,tail_img)
del tail_img,tail

player_img_name = ['down','up','right','left','down_hit','up_hit','right_hit','left_hit']
player_img = [select_img('P_down.png'),select_img('P_up.png'),select_img('P_right.png'),select_img('P_left.png'),
              select_img('P_down_hit.png'),select_img('P_up_hit.png'),select_img('P_right_hit.png'),select_img('P_left_hit.png')]
player_img_map = create_hash(player_img_name,player_img)
del player_img_name,player_img

enemy_img_name = ['normal','alert','angry']
enemy_img = [select_img('enemy.png'),select_img('enemy_alert.png'),select_img('enemy_angry.png')]
enemy_img_map = create_hash(enemy_img_name,enemy_img)
del enemy_img_name,enemy_img

egg_img_name = ['egg_n','egg_r','spawn']
egg_img = [select_img('egg_n.png'),select_img('egg_r.png'),select_img('midge.png')]
egg_img_map = create_hash(egg_img_name,egg_img)
del egg_img_name,egg_img

Obj_img_name = ['icon','tree','xp','apple','bush1','bush2','bush3','bush4','d_close','key','enemy_spawner','rod']
Obj_img = [select_img('icon.png'),select_img('Tree.png'),select_img('xp.png'),select_img('apple.png'),
           select_img('bush1.png'),select_img('bush2.png'),select_img('bush3.png'),select_img('bush4.png'),
           select_img('dungeon_close.png'),select_img('key.png'),select_img('enemy_spawner.png'),select_img('rod_off.png')]
Obj_img_map = create_hash(Obj_img_name,Obj_img)

dung_img_name = ['close','open']
dung_img = [select_img('dungeon_close.png'),select_img('dungeon_open.png')]
dung_img_map = create_hash(dung_img_name,dung_img)
del dung_img_name, dung_img


Obj_img = [select_img('Tree.png'),
           select_img('bush1.png'),select_img('bush2.png'),select_img('bush3.png'),select_img('bush4.png'),
           select_img('P_down.png'),select_img('enemy.png'),select_img('dungeon_close.png'),select_img('key.png'),
           select_img('enemy_spawner.png'),select_img('rod_off.png'),select_img('None.png')]
Obj_img_name = ['T','b','b','b','b','P','e','D','k','S','r','.']

#иконка окна "деревце"
icon = Obj_img_map['icon']
# пока что единственный созданный звук - звук врага
alert_sound = select_sound('alert.mp3')
frontir = select_front(60)



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
class Static_obj(Obj):
    def __init__(self,pos,type):
        self.type = type
        super().__init__(pos,img = Obj_img_map[type])

class Apple(Static_obj):
    def __init__(self,pos):
        super().__init__(pos,type ='apple')
    def update(self):
        if intersection(player_1.rect,self.rect):
            player_1.counter_apple+=1
            player_1.hp+=10
            self.kill()
    def interfase_update(self):
        self.rect.center = (player_1.rect.x + 590,player_1.rect.y - 300)
class Xp(Static_obj):
    def __init__(self,pos):
        super().__init__(pos,type ='xp')
    def update(self):
        self.paint_border()
        if intersection(player_1.rect,self.rect):
            player_1.counter_xp+=1
            player_1.hp+=2
            self.kill()
class Key(Static_obj):
    def __init__(self,pos):
        super().__init__(pos,type ='key')
    def update(self):
        self.paint_border()
        if intersection(player_1.rect,self.rect):
            player_1.counter_key+=1
            self.kill()
class Tree(Static_obj):

    def __init__(self,pos,type):
        super().__init__(pos,type)
        # твёрдый объект
        self.solid_x = self.rect.x+120
        self.solid_y = self.rect.y+265
        self.solid = pygame.rect.Rect(self.solid_x, self.solid_y, 30, 120)
        self.solid_border = (120,265,30,120)

    def update(self):
        self.paint_border()
        pygame.draw.rect(self.image,RPURPLE,self.solid_border,3)
        if intersection(player_1.rect,self.solid):
            where_x = sign(self.solid.centerx - player_1.rect.centerx)
            where_y = sign(self.solid.centery - player_1.rect.centery)
            player_1.rect.x-=where_x*player_SPEED
            player_1.rect.y-=where_y*player_SPEED

    def spawn_apple(self):
        m = random.randint(0,1)
        x = 0
        y = 0
        if self.rect.x<65:
            m = 0
        elif self.rect.x>(map_border.x - 100):
            m = 1
        if self.rect.y<65:
            y = random.randint(self.rect.centery+150,self.rect.centery + 192)
        else:
            y = random.randint(self.rect.centery+80,self.rect.centery + 192)
        if m == 1:
            x = random.randint(self.rect.x+20,self.solid.x - 10)
        else:
            x = random.randint(self.solid.x + 60,self.rect.x + 245)
        apple = Apple((x,y))
        return apple
class Rod(Static_obj):
    def __init__(self,pos):
        super().__init__(pos,type ='rod')
        self.state = False
    def rod_off(self):
        self.state = False
        self.image = select_img('rod_off.png')
        boss.rod_counter_t-=1
    def update(self):
        if intersection(player_1.hit_s,self.rect):
            if self.state:
                self.state = False
                self.image = select_img('rod_off.png')
                boss.rod_counter_t-=1
            else:
                self.image = select_img('rod_on.png')
                self.state = True
                boss.rod_counter_t+=1
class Rod_group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    def rod_off(self):
        for sprite in self.sprites():
            sprite.rod_off()
class heart(Obj):
    def __init__(self,numb):
        self.numb = numb
        super().__init__(pos = (player_1.rect.x+640,player_1.rect.y-340),img = select_img('heart.png'))
        self.rect.center = (player_1.rect.x+640 - self.numb * 50 ,player_1.rect.y-340)
    def update(self):
        self.rect.center = (player_1.rect.x+640 - self.numb * 50 ,player_1.rect.y-340)
        if (self.numb+1)* 10>player_1.hp:
            self.kill()
class Dungeon(Tree):
    def __init__(self,pos):
        super().__init__(pos,type='d_close')
        self.solid_x = self.rect.x + 128
        self.solid_y = self.rect.y + 120
        self.solid = pygame.rect.Rect(self.solid_x, self.solid_y, 128, 136)
        self.solid_border = (128,120,128,136)
        self.Gate_is_open = False
        self.solid_1 = pygame.rect.Rect(self.solid_x, self.solid_y, 128, 100)
        self.solid_border_1 = (128,120,128,100)

        # доп грани
        #self.solid_1 = pygame.rect.Rect(self.solid_x-128, self.solid_y, 128, 136)
        #self.solid_border_1 = (0,120,128,136)
        #self.solid_2 = pygame.rect.Rect(self.solid_x+128, self.solid_y, 128, 136)
        #self.solid_border_2 = (256,120,128,136)
    def update(self):
        super().update()
        # всё те же доп.грани
        #pygame.draw.rect(self.image,WHITE,self.solid_border_1,4)
        #pygame.draw.rect(self.image,WHITE,self.solid_border_2,4)
        #if intersection(player_1.rect,self.solid_1):
         #   where_x = sign(self.solid_1.centerx - player_1.rect.centerx)
          #  where_y = sign(self.solid_1.centery - player_1.rect.centery)
           # player_1.rect.x-=where_x*player_SPEED
            #player_1.rect.y-=where_y*player_SPEED
        #if intersection(player_1.rect,self.solid_2):
         #   where_x = sign(self.solid_2.centerx - player_1.rect.centerx)
          #  where_y = sign(self.solid_2.centery - player_1.rect.centery)
           # player_1.rect.x-=where_x*player_SPEED
            #player_1.rect.y-=where_y*player_SPEED
        if (self.Gate_is_open == False) and (player_1.counter_key >= 2):
            # пересечение - переход
            self.image = dung_img_map['open']
            self.solid_border = (128,120,128,68)
            self.solid = pygame.rect.Rect(self.solid_x, self.solid_y, 128, 68)
            self.Gate_is_open = True
#enemy spawner
class En_sp(Tree):
    def __init__(self,pos):
        super().__init__(pos,type='enemy_spawner')
        self.solid_x = self.rect.x
        self.solid_y = self.rect.y + 50
        self.solid = pygame.rect.Rect(self.solid_x, self.solid_y, 200, 90)
        self.solid_border = (0,50,200,90)
    def update(self):
        super().update()

class NPC(Obj):
    def __init__(self,pos,hp,dmg,img):
        self.hp = hp
        self.dmg = dmg
        super().__init__(pos,img)
        self.DDTP = 0
        self.cord_dif = pygame.Vector2()
        self.attack_timer = 0
        self.stop_timer = 0

    def check_kill(self):
        if intersection(player_1.hit_s,self.rect):
            self.hp-=player_1.dmg
            self.stop_timer = pygame.time.get_ticks()
            if self.hp<1:
                xp = Xp(self.rect.center)
                all_sprites.add(xp)
                camera_group.add(xp)
                player_1.counter_kill+=1
                print(player_1.counter_kill)
                self.kill()
    def update(self):
        self.check_kill()
        self.cord_dif.x = player_1.rect.centerx - self.rect.centerx
        self.cord_dif.y = player_1.rect.centery - self.rect.centery
        self.DDTP = math.sqrt(self.cord_dif.x**2 + self.cord_dif.y**2)
    def move_to_player(self,speed):
        if self.stop_timer + 400 < pygame.time.get_ticks():
            self.rect.centerx += speed*sign(self.cord_dif.x)
            self.rect.centery += speed*sign(self.cord_dif.y)
class Player(Obj):
    def __init__(self,pos):
        self.hp = player_Hp
        self.dmg = player_dmg
        super().__init__(pos,img = player_img_map['down'])
        self.side = 'down'
        self.hit_time_dist = player_hit_time_dist
        self.hit_time = 0
        self.hit_time_anim = player_hit_time_anim
        self.direction = pygame.math.Vector2()
        self.speed = player_SPEED
        self.counter_apple = 0
        self.counter_xp = 0
        self.counter_kill = 0
        self.counter_key = 0
        self.hit_s = pygame.rect.Rect(0,0,0,0)

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
        if pygame.key.get_pressed()[pygame.K_o] and self.hit_time + self.hit_time_dist <= timer:
            self.hit_s = player_1.hit()
        else:
            self.hit_s = pygame.rect.Rect(0,0,0,0)

        self.paint_border()

    def hit(self):
        self.hit_time = pygame.time.get_ticks()
        hit_x = self.rect.centerx
        hit_y = self.rect.centery
        if (self.direction.y!=0 or self.direction == (0,0)):
            hit_w = player_hit_rad
            hit_h = player_hit_range
            hit_x+= -32 + 32*(self.direction.x-1)
            hit_y+= -32 + 45*self.direction.y
            if self.direction == (0,0):
                hit_y+=45
        elif self.direction.y==0:
            hit_x+= -32 + 45*self.direction.x
            hit_y+= -32 + 32*(self.direction.y-1)
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
        self.attack_timer = 0
        self.do_attack = False

        self.pmv_timer = pygame.time.get_ticks()
        self.pmv_x = 0
        self.pmv_y = 0
        super().__init__(pos,hp,dmg,img = enemy_img_map['normal'])
    def update(self):
        #перемещение
        super().update()
        if (self.DDTP <= enemy_view):
            if (self.catch==False):
                self.catch_timer = pygame.time.get_ticks()
                self.image = enemy_img_map['alert']
                self.catch = True
                #Chanel_1.play(alert_sound)
            if pygame.time.get_ticks() > self.catch_timer + 300 and self.DDTP >= enemy_attack_range:
                self.image = enemy_img_map['angry']
                self.move_to_player(enemy_speed)
                self.pmv_timer = pygame.time.get_ticks()
                self.pmv_x = 0
                self.pmv_y = 0
            if self.DDTP <= enemy_attack_range and pygame.time.get_ticks() > self.attack_timer + 700:
                player_1.hp-=enemy_dmg
                self.attack_timer = pygame.time.get_ticks()
        else:
            self.catch = False
            self.image = enemy_img_map['normal']
            # пассивное хождение
            if self.pmv_timer + 1000 < pygame.time.get_ticks():
                self.pmv_x = random.choice([-1,0,0,0,1])
                self.pmv_y = random.choice([-1,0,0,0,1])
                self.pmv_timer = pygame.time.get_ticks()
            self.rect.centerx+=enemy_speed/2 * self.pmv_x
            self.rect.centery+=enemy_speed/2 * self.pmv_y
        self.paint_border()
class Midge(NPC):
    def __init__(self,pos,hp,dmg):
        super().__init__(pos,hp,dmg,img = egg_img_map['egg_n'])
        self.timer = pygame.time.get_ticks()
        self.stadia = None
    def update(self):
        self.check_kill()
        if self.stadia == None and self.timer + 4200 <= pygame.time.get_ticks():
            self.stadia = False
            self.image = egg_img_map['egg_r']
            self.timer = pygame.time.get_ticks()
        if self.stadia == False and self.timer + 4200 <= pygame.time.get_ticks():
            self.stadia = True
            self.image = egg_img_map['spawn']
        if self.stadia:
            super().update()
            self.move_to_player(3)
            if self.DDTP <= enemy_attack_range and pygame.time.get_ticks() > self.attack_timer + 700:
                player_1.hp-=enemy_dmg
                self.attack_timer = pygame.time.get_ticks()
class Boss(NPC):
    def __init__(self, pos):
        super().__init__(pos,hp = 1000,dmg = 1000,img = select_img('Boss.png'))
        self.rod_counter = 0
        self.rod_counter_t = 0
        self.rod_is_real = False
        self.stan = False
        self.stan_timer = 0
        self.stan_timer_dist = 8000
    def update(self):
        super().update()
        if not self.stan:
            self.move_to_player(boss_speed)
            if self.rod_is_real and self.rod_counter == self.rod_counter_t:
                self.stan = True
                self.stan_timer = pygame.time.get_ticks()
            player_1.dmg = 10
        if self.stan:
            player_1.dmg = 500
        self.paint_border()
        pygame.draw.circle(self.image, BLACK,(256,256), 220,5)
        if self.DDTP < 220:
            player_1.hp = 0
        if self.stan and self.stan_timer + self.stan_timer_dist <= pygame.time.get_ticks():
            self.stan = False
            rod_gr.rod_off()


class CameraGroup(pygame.sprite.Group):
    def __init__(self,image):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0]// 2
        self.half_h = self.display_surface.get_size()[1]// 2
        # ground
        self.ground_surf = select_img(image)
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
    def change_img(self,image):
        self.ground_surf = select_img(image)
    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self,player):

        self.center_target_camera(player)

        #ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.fill(map_color)
        self.display_surface.blit(self.ground_surf,ground_offset)

        #active elements
        for sprite in self.sprites(): #sorted(self.sprites(),key=lambda  sprite:sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

def redactor(power,map_to_change,tile_arr,tile_case,button_freeze_timer):
    screen.fill(map_color)
    screen.blit(select_img('help.png'),(0,639))
    pygame.display.flip()
    changer_text_map = text_to_map(read_text_file(map_to_change))
    red_surf = draw_map(True,'none_map.png','cache/map_redacted.txt')
    if tile_case == 0:
        unlimited = 0
        type = True
        limited = 11
        for i in range(0,20):
            for j in range(0,40):
                if changer_text_map[i][j] !='.':
                    if changer_text_map[i][j] == 'P':
                        red_surf.blit(pygame.transform.scale(tile_arr[5],(power,power)),(j*32,i*32))
                    if changer_text_map[i][j] == 'T':
                        red_surf.blit(pygame.transform.scale(tile_arr[0],(power,power)),(j*32,i*32))
                    if changer_text_map[i][j] == 'b':
                        red_surf.blit(pygame.transform.scale(tile_arr[1],(power,power)),(j*32,i*32))
                    if changer_text_map[i][j] == 'e':
                        red_surf.blit(pygame.transform.scale(tile_arr[6],(power,power)),(j*32,i*32))
                    if changer_text_map[i][j] == 'k':
                        red_surf.blit(pygame.transform.scale(tile_arr[8],(power,power)),(j*32,i*32))
                    if changer_text_map[i][j] == 'S':
                        red_surf.blit(pygame.transform.scale(tile_arr[9],(power,power)),(j*32,i*32))
                    if changer_text_map[i][j] == 'r':
                        red_surf.blit(pygame.transform.scale(tile_arr[10],(power,power)),(j*32,i*32))
                    if changer_text_map[i][j] == 'D':
                        red_surf.blit(pygame.transform.scale(tile_arr[7],(power,power)),(j*32,i*32))
    else:
        unlimited = 1
        type = False
        limited = 7
    #сетка
    red_cursor = pygame.rect.Rect(0,0,power,power)
    run_redactor = True
    while run_redactor:
        if type ==0:
            analog = pygame.transform.scale(tile_arr[str(tile_case)],(power,power))
            point = str(tile_case)
        else:
            analog = pygame.transform.scale(tile_arr[tile_case],(power,power))
            point = Obj_img_name[tile_case]
        timer = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_redactor = False
        if button_freeze_timer + 90<=timer:
            button_freeze_timer = timer
            if check_button(pygame.K_q) and tile_case>unlimited:
                tile_case-=1
            if check_button(pygame.K_e) and tile_case<limited:
                tile_case+=1
            if (check_button(pygame.K_d) or check_button(pygame.K_RIGHT)) and red_cursor.x<1280 - power:
                red_cursor.x+=power
            if (check_button(pygame.K_a) or check_button(pygame.K_LEFT)) and red_cursor.x>0:
                red_cursor.x-=power
            if (check_button(pygame.K_w) or check_button(pygame.K_UP)) and red_cursor.y>0:
                red_cursor.y-=power
            if (check_button(pygame.K_s)or check_button(pygame.K_DOWN)) and red_cursor.y<640 - power:
                red_cursor.y+=power
            if check_button(pygame.K_RETURN):
                changer_text_map[red_cursor.y//power][red_cursor.x//power] = point
                red_surf.blit(analog,red_cursor)
            if check_button(pygame.K_ESCAPE):
                write_text_file(map_to_change,changer_text_map)
                run_redactor = False
        screen.blit(red_surf,(0,0))
        screen.blit(analog,red_cursor)
        pygame.draw.rect(screen,RPURPLE,red_cursor,3)
        pygame.display.flip()
    del red_surf

#просто цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RPURPLE = (185,0,105)


map_color = (63,72,204)
map_border = pygame.math.Vector2(4000,2000)
# 1280x800
# 1920x1080
WIDTH = 1280  # ширина игрового окна
HEIGHT = 800 # высота игрового окна
FPS = 60 # частота кадров в секунду

pygame.init() #инициаллизация всех игровых объедков

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаём экран)
pygame.display.set_caption("CoboLt, 0.15") # экран
pygame.display.set_icon(icon) # иконка дерева - если вы помните (icon) была объявлена еще до структур
clock = pygame.time.Clock()


#  главные параметры "настройки" - от них зависит сложность
player_SPEED = 7
player_Dash_co = 3
player_Hp = 40
player_dmg = 10

player_hit_range = 64
player_hit_rad = 128
player_hit_time_dist = 500
player_hit_time_anim = 200
player_counter_kill = 0

enemy_view = 400
enemy_speed = player_SPEED/2
boss_speed = 1
enemy_hp = 30
enemy_dmg = 10
enemy_attack_range = 64


# для изменения размера экрана
# WIDTH = 1280  # ширина игрового окна
# HEIGHT = 800 # высота игрового окна
# screen = pygame.display.set_mode((WIDTH, HEIGHT)) переназначаем экран с внесёнными изменениями
run_all = True
run_game = True
run_menu = True

map_file = '1_tail_map.txt'
obj_file = '1_object_map.txt'

next_map_flag = False

while run_all == True :
    pygame.display.set_icon(icon)
    if next_map_flag:
        run_game = True
        map_file = '2_tail_map.txt'
        obj_file = '2_object_map.txt'
        map_border.x=2000
    clock.tick(10)
    screen.fill(map_color)
    # отвечает за индексацию(отслеживание выбора)
    text_index = 0
    #отвечает за тип селектора
    text_select = 0
    #отвечает за количество отображаемого текста селектора
    text_index_lim = 2
    button_freeze_timer = 0

    while run_menu:
        timer = pygame.time.get_ticks()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
                run_game = False
                run_all = False
        screen.blit(select_img('menu.png'),(0,0))
        screen.blit(frontir.render('V 0.15',True,GREEN),(1100,740))
        # нашъ прекрасный шрифт размера 60)
        frontir = select_front(60)
        if button_freeze_timer + 100<=timer:
            button_freeze_timer = timer
            if  (check_button(pygame.K_s) or check_button(pygame.K_DOWN)):
                if text_index == text_index_lim:
                    text_index = 0
                else:
                    text_index+=1
            if (check_button(pygame.K_w) or check_button(pygame.K_UP)):
                button_freeze_timer = timer
                if text_index == 0:
                    text_index = text_index_lim
                else:
                    text_index-=1
            # я зуб даю перепишу этот ужас ибо мне стыдно смотреть на подобную реализацию, но пока так, живите с этим(
            if check_button(pygame.K_KP_ENTER) or check_button(pygame.K_RETURN):
                if text_index==0:
                    if text_select==0:
                        text_select = 1
                    elif text_select==1:
                        run_menu=False
                        run_game = True
                    # запуск игры на изменённой карте
                    elif text_select==2:
                        map_file = 'cache/map_redacted.txt'
                        obj_file = 'cache/object_redacted.txt'
                        run_menu=False
                        run_game = True
                if text_index == 1:
                    # настройки
                    #if text_select = 0:
                    # переход к меню редактора
                    if text_select == 1:
                        text_index_lim+=1
                        text_select+=1
                    # реальный выход к реальному редактору !
                    elif text_select == 2:
                        redactor(64,'cache/map_redacted.txt',tail_map,1,button_freeze_timer)

                if text_index == 2:
                    if text_select == 0:
                        run_menu = False
                        run_game = False
                        run_all = False
                    elif text_select == 1:
                        text_select=0
                    #переход к редактору ОБЪЕДКОВ
                    elif text_select == 2:
                        redactor(32,'cache/object_redacted.txt',Obj_img,0,button_freeze_timer)
                # третй пункт достигается только в настройках редактора
                if text_index == 3:
                    text_select=1
                    text_index-=1
                    text_index_lim-=1

        #отрисовка нашей менюшки)
        text_arr = ['Play','Settings(in progress)','Quit',
                    'Play story','Map editor','Back',
                    'Play on created map','Map redactor','Object redactor','Back'] # нормально

        for i in range(0,text_index_lim+1):
            screen.blit(frontir.render(text_arr[i+3*text_select],True,BLUE),(70,250+i*100))
        screen.blit(frontir.render(text_arr[text_index+3*text_select],True,RPURPLE),(73,253+text_index*100))
        pygame.display.flip()
    if run_game:
        if not next_map_flag:
            player_Hp = 40
        #exist
        Dung_ex = False
        Spawner_ex = False
        # обнуляем группы спрайтов
        all_sprites = pygame.sprite.Group()
        enemy_sprites = pygame.sprite.Group()
        static_sprites = pygame.sprite.Group()
        rod_gr = Rod_group()
        # создаём карточку
        text_map_obj = text_to_map(read_text_file(obj_file))
        #map_obj_grid_count
        power = 100
        map_ogc = pygame.math.Vector2(int(map_border.x) // power,int(map_border.y) // power)
        grid_obj = create_grid(map_ogc,power)
        pygame.image.save(draw_map(False,'none_map.png',map_file),'img/screen.png')
        #это точно надо изменить, но пока не придумал другой реализации
        camera_group = CameraGroup('screen.png')
        #анализ и создание объектов
        spawner_cord_arr = []
        rod_counter = 0
        rod_is_real = False
        for i in range(0,int(map_ogc.y)):
            for j in range(0,int(map_ogc.x)):
                pygame.draw.rect(camera_group.ground_surf,WHITE,grid_obj[i][j],1)
                if text_map_obj[i][j] == 'P':
                    player_1 = Player(grid_obj[i][j].center) # создаём спрайт класса "игрок"
                    for p in range(0,player_Hp//10):
                        heart_1 = heart(p)
                        static_sprites.add(heart_1)
                if text_map_obj[i][j] == 'T':
                    some_tree = Tree((grid_obj[i][j].centerx,grid_obj[i][j].centery-200),'tree')
                    for k in range(random.randint(0,2)):
                        some_apple = some_tree.spawn_apple()
                        static_sprites.add(some_apple)
                    static_sprites.add(some_tree)
                if text_map_obj[i][j] == 'b':
                    some_bush = Static_obj(grid_obj[i][j].center,'bush'+str(random.randint(1,4)))
                    static_sprites.add(some_bush)
                if text_map_obj[i][j] == 'e':
                    some_enemy = Enemy(grid_obj[i][j].center,enemy_hp,enemy_dmg)
                    enemy_sprites.add(some_enemy)
                if text_map_obj[i][j] == 'm':
                    some_midge = Midge(grid_obj[i][j].center,10,enemy_dmg)
                    enemy_sprites.add(some_midge)
                if text_map_obj[i][j] == 'B':
                    boss = Boss(grid_obj[i][j].center)
                    enemy_sprites.add(boss)
                if text_map_obj[i][j] == 'D':
                    Dung_ex = True
                    Dung = Dungeon(grid_obj[i][j].center)
                    static_sprites.add(Dung)
                if text_map_obj[i][j] == 'S':
                    spawner = En_sp(grid_obj[i][j].center)
                    spawner_cord_arr.append(spawner.rect.center)
                    Spawner_ex = True
                    static_sprites.add(spawner)
                if text_map_obj[i][j] == 'k':
                    key = Key(grid_obj[i][j].center)
                    static_sprites.add(key)
                if text_map_obj[i][j] == 'r':
                    some_rod = Rod(grid_obj[i][j].center)
                    rod_gr.add(some_rod)
                    static_sprites.add(some_rod)
                    rod_is_real = True
                    rod_counter+=1


        all_sprites.add(player_1,enemy_sprites,static_sprites) # добавляем объекты в группы
        camera_group.add(all_sprites)

        # прямоугольничек атаки)))
        hit_s = pygame.rect.Rect(0,0,0,0)
        time_to_sp = 1000
        # заполняем экран цветастостью
        screen.fill(map_color)
    while run_game:
        clock.tick(FPS)
        #print(pygame.time.get_ticks())
        timer = pygame.time.get_ticks()
        #print(clock)
        #print('a = ',player_1.counter_apple, '\tk = ',player_1.counter_kill,'\txp = ',player_1.counter_xp)
        #print(player_1.get_cord())
        #print(len(all_sprites))

        # Ввод процесса (события)

        # Обновление всех спрайтов
        # не забываем что внути udate прописаны event для управления

        #обработка событий
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT: # работа "крестика"
                run_all = False # завершает цикл
                run_game = False
        if Spawner_ex:
            if time_to_sp + 4000 < timer:
                m = random.randint(0,len(spawner_cord_arr)-1)
                some_enemy = Enemy(spawner_cord_arr[m],enemy_hp,enemy_dmg)
                enemy_sprites.add(some_enemy)
                all_sprites.add(some_enemy)
                camera_group.add(some_enemy)
                time_to_sp = timer
        print(player_1.hp,'\t',player_Hp)
        if player_1.hp+9 < player_Hp:
            player_Hp = (player_1.hp//10)*10
        if player_1.hp > player_Hp+9:
            player_Hp = (player_1.hp//10)*10
            print(player_1.hp,'\t',player_Hp)
            some_heart = heart((player_1.hp//10)-1)
            print(some_heart.rect.center)
            static_sprites.add(some_heart)
            camera_group.add(some_heart)
            all_sprites.add(some_heart)

        if next_map_flag:
            if rod_is_real:
                boss.rod_is_real = True
                boss.rod_counter = rod_counter
            if time_to_sp + 2000 < timer and boss.stan == False:
                sp_x = random.randint(boss.rect.centerx - 200,boss.rect.centerx + 200)
                sp_y = random.randint(boss.rect.centery - 200,boss.rect.centery + 200)
                some_egg = Midge((sp_x,sp_y),10,enemy_dmg)
                enemy_sprites.add(some_egg)
                all_sprites.add(some_egg)
                camera_group.add(some_egg)
                time_to_sp = timer
            if boss.hp<1:
                screen.blit(select_img('win.jpg'),(0,0))
                screen.blit(frontir.render('You won, thanks for playing',True,RPURPLE),(10,253))
                screen.blit(frontir.render('Score: ',True,RPURPLE),(10,353))
                player_counter_kill += player_1.counter_kill
                screen.blit(frontir.render(str(player_counter_kill),True,RPURPLE),(250,353))
                pygame.display.flip()
                time.sleep(5)
                run_game = False
                run_menu = True

        if Dung_ex:
            if Dung.Gate_is_open:
                pygame.draw.rect(Dung.image,GREEN,Dung.solid_border_1,4)
                if intersection(Dung.solid_1,player_1.rect):
                    run_game = False
                    run_menu = False
                    next_map_flag = True
                    Dung.Gate_is_open = False
                    player_Hp = player_1.hp
                    player_counter_kill = player_1.counter_kill

        if player_1.hp<=0:
            player_1.kill()
            camera_group.custom_draw(player_1)
            run_game = False
            run_menu = True
            screen.blit(select_img('dead.png'),(0,0))
            pygame.display.flip()
            time.sleep(5)
        #Рендеринг
        all_sprites.update()
        # Визуализация (сборка)
        camera_group.custom_draw(player_1)
        pygame.draw.rect(camera_group.ground_surf,RED,player_1.hit_s,4)
        pygame.display.flip() # отрисовка
    #pygame.image.save(screen,'cache/screen.png')
    #pygame.image.save(camera_group.ground_surf,'cache/camera.png')