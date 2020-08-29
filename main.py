import pygame, cmath, threading, sys
from math import *


pygame.init()
w, h = int(181*1), int(181*0.8); cx, cy = w//2, h//2; run = True
print(w, h)
mouseHold = False; mouseInfo = [cx, cy]; prefMouse = []
tries = 100; defaultDist = 0.01; distance = defaultDist; offset = [0, 0]
# monitorInfo = (pygame.display.Info().current_w, pygame.display.Info().current_h); pref_size = [0, 0]
pygame.display.set_caption("The Mandelbrot set")
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
# fullscreen = False


def new_vector(x, y):
    value = 0
    vector = complex(0, 0)
    g = 255/tries
    # print(g)
    t = 0
    if distance != 0:
        t = distance/(defaultDist/distance)
    start = complex((x-cx)*distance-offset[0]-0.5, 
                    (y-cy)*distance-offset[1])
    while value < tries:
        if not run: return
        vector = vector * vector + start
        if vector.real + vector.imag > 4:
            break
        value += 1
    if value == ceil(tries):
        screen.set_at((x, y), (0, 0, 0))
    elif 0 < value < tries:
        # print(g)     
        color = int(255-value*g) 
        # print(color)
        if color < 0: color = 0
        screen.set_at((x, y), (color, color, color))    
    else:
        screen.set_at((x, y), (255, 255, 255))


def Arender():
    while run:
        clock.tick(60)
        # _w, _h, _cx, _cy = w, h, cx, cy
        screen.fill((0, 0, 0))
        for y in range(0, h):
            for x in range(0, w):
                new_vector(x, y)

        pygame.draw.circle(screen, (255, 0, 0), (int(mouseInfo[0]), int(mouseInfo[1])), 5)
        pygame.display.update()


def render():
    while run:
        clock.tick(60)
        screen.fill((250, 250, 250))
        inv = 1/distance
        startPos = 1
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy), int(inv))
        pygame.draw.circle(screen, (250, 250, 250), (cx, cy), int(inv)-5)
        pygame.draw.circle(screen, (0, 255, 0), mouseInfo, 6)
        vector = complex(0, 0)
        start = complex((mouseInfo[0]-cx)*distance, (mouseInfo[1]-cy)*distance)
        negX = 1; negY = 0

        dots = [vector]
        pref = None
        # for y in range(0, h):
        #     for x in range(0, w):
        #         pass
        for _ in range(0, 20):
            vector = vector * vector + start
            dots.append(vector)
        for i in range(1, 20):
            try:
                vR = dots[i].real; vI = dots[i].imag
                pR = dots[i-1].real; pI = dots[i-1].imag
                pygame.draw.circle(screen, (0, 0, 0), (int(vR*inv+cx), int(vI*inv+cy)), 6)
                pygame.draw.line(screen, (255, 0, 0), (int(vR*inv+cx), int(vI*inv+cy)), (int(pR*inv+cx), int(pI*inv+cy)), 3)
            except: pass
        pygame.display.update()


tick1 = pygame.time.get_ticks()
def move(key):
    global tries, tick1, distance

    # if key[pygame.K_w]:
    #     mouseInfo[1] += 0.01
    # if key[pygame.K_s]:
    #     mouseInfo[1] -= 0.01
    # if key[pygame.K_a]:
    #     mouseInfo[0] += 0.01
    # if key[pygame.K_d]:
    #     mouseInfo[0] -= 0.01
    if key[pygame.K_w]:
        offset[1] += distance
    if key[pygame.K_s]:
        offset[1] -= distance
    if key[pygame.K_a]:
        offset[0] += distance
    if key[pygame.K_d]:
        offset[0] -= distance
    if key[pygame.K_e]:
        distance = distance*0.9
    if key[pygame.K_q]:
        distance = distance*1.1

    if pygame.time.get_ticks() - tick1 > 100:
        if key[pygame.K_2]:
            tick1 = pygame.time.get_ticks()
            tries += 1
            print(tries)
        if key[pygame.K_1]:
            tick1 = pygame.time.get_ticks()
            tries -= 1
            print(tries)


ArenderT = threading.Thread(target=Arender)
ArenderT.start()

while run:
    clock.tick(60)
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event == pygame.QUIT:
            print("n")
            pygame.quit()
            sys.exit()

        # if event.type == pygame.VIDEORESIZE:
        #     if not fullscreen:
        #         w, h = event.w, event.h
        #         cx, cy = w//2, h//2
        #         screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mX, mY = pygame.mouse.get_pos()
            if mouseHold:
                mouseHold = False
            else:
                if mouseInfo[0] - 10 < mX < mouseInfo[0] + 10 and mouseInfo[1] - 10 < mY < mouseInfo[1] + 10:
                    mouseInfo = [mX, mY]
                    # i[2] = (255, 0, 0)
                    mouseHold = True

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_f:
        #         fullscreen = not fullscreen
        #         if fullscreen: 
        #             pygame.display.set_mode(monitorInfo, pygame.FULLSCREEN) 
        #             pref_size = (w, h)
        #             w, h = monitorInfo; cx, cy = w//2, h//2
        #         else:  
        #             w, h = pref_size; cx, cy = w//2, h//2
        #             pygame.display.set_mode((w, h), pygame.RESIZABLE)

    if key[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        sys.exit()

    move(key)
    if mouseHold and pygame.time.get_ticks() - tick1 > 50:
        tick1 = pygame.time.get_ticks()
        mX, mY = pygame.mouse.get_pos()
        mouseInfo = [mX, mY]