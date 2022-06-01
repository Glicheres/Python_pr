import pygame
import random
# 1280x800
WIDTH = 1280  # ширина игрового окна
HEIGHT = 800 # высота игрового окна
FPS = 60 # частота кадров в секунду


pygame.init() #инициаллизация всех игровых объедков
pygame.mixer.init()  # инициализация звука
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаём экран)
pygame.display.set_caption("Cobolt") # экран mygame
clock = pygame.time.Clock() #убежаемся в заданной частоте кадров


# просто цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RPURPLE = (185,0,105)
screen.fill(RPURPLE)

run = True
while run:
    clock.tick(FPS)
    print(clock)
    # Ввод процесса (события)


    # Обновление

    #обработка событий
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT: # работа "крестика"
            run = False

    #Рендеринг


    # Визуализация (сборка)
    pygame.display.flip() # отрисовка