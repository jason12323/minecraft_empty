# import pygame
import time
import os
# from pygame.locals import *

import main
from mods import modlist

ver = os.listdir(os.getcwd()+"/minecraft")

"""pygame.init()

sc = pygame.display.set_mode((500, 281), 0, 30)
pygame.display.set_caption("minecraft launcher")
fp = pygame.image.load("fp.jpeg")
p2 = pygame.image.load("t2.jpeg")
p3 = pygame.image.load("t3.png")
p4 = pygame.image.load("t4.png")

def text(tex):
    my_font = pygame.font.SysFont("arial", 16)
    return my_font.render(tex, True, pygame.color.Color(0, 0, 0))

def startpage():
    global sc
    b = True
    sc.blit(fp, (0, 0))
    pygame.display.update()
    time.sleep(5)
    while b:  # main loop
        for event in pygame.event.get():  # 获取事件
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                b = False
        sc.blit(p2, (0, 0))
        pygame.display.update()


def inarea(areard, arealu):
    mouse = pygame.mouse.get_pos()
    return areard[0] < mouse[0] < arealu[0] and areard[1] < mouse[1] < arealu[1]
"""

# startpage()
while True:
    """
    sc.blit(p3, (0, 0))
    pygame.display.update()
    inp = 0
    for event in pygame.event.get():  # 获取事件
        if event.type == MOUSEBUTTONDOWN:
            if inarea((135, 201), (363, 268)):
                sc.blit(p4, (0, 0))
                yy = 0
                for y in ver:
                    yy += 30
                    sc.blit(text(str(yy//30)+y), (250, yy))
                pygame.display.update()
                while True:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[pygame.K_1]:
                        a = ver[0]
                        break
                    if keys_pressed[pygame.K_2]:
                        a = ver[1]
                        break
                    if keys_pressed[pygame.K_3]:
                        a = ver[2]
                        break
                    if keys_pressed[pygame.K_4]:
                        a = ver[3]
                        break
                    if keys_pressed[pygame.K_5]:
                        a = ver[4]
                        break
                    if keys_pressed[pygame.K_6]:
                        a = ver[5]
                        break
                    if keys_pressed[pygame.K_7]:
                        a = ver[6]
                        break
                    if keys_pressed[pygame.K_8]:
                        a = ver[7]
                        break
                    if keys_pressed[pygame.K_9]:
                        a = ver[8]
                        break
                try:
                    b = open(r"minecraft/" + a + ".py", "r")
                except IOError:
                    print("can't open minecraft " + a)
                    continue
                c = open(r"main.py", "w+")
                c.write(b.read())
                c.close()
                b.close()
                import main
            elif inarea((135, 106), (363, 183)):
                print("------------minecraft-------------\n\n\n")
                main.maii()
            elif inp == "3":
                print(modlist.mod)
                inp = input("1:add mod\n2:back\n?")
                if inp == "1":
                    a = input("mod name?")
                    b = open(r"mods/modlist.py", "r")
                    c = b.read().split("]")[0]
                    b.close()
                    b = open(r"mods/modlist.py", "w+")
                    b.write(c + ", " + a + ".main]")
                    b.close()
                    from mods import modlist
    """
    inp = input("1:install minecraft version\n2:play\n3:[mods]\n?")
    if inp == "1":
        a = input("version?")
        try:
            b = open(r"minecraft/minecraft "+a+".py", "r")
        except IOError:
            print("can't open minecraft "+a)
            continue
        c = open(r"main.py", "w+")
        c.write(b.read())
        c.close()
        b.close()
        import main
    elif inp == "2":
        print("------------minecraft-------------\n\n\n")
        main.maii()
    elif inp == "3":
        print(modlist.mod)
        inp = input("1:add mod\n2:delete mod\n3:back\n?")
        if inp == "1":
            a = input("mod name?")
            b = open(r"mods/modlist.py", "r")
            c = b.read().split("]")[0]
            b.close()
            b = open(r"mods/modlist.py", "w+")
            b.write(c+", "+a+".main]")
            b.close()
            from mods import modlist
        elif inp == "2":
            b = open(r"mods/modlist.py", "r")
            d = b.read()
            c = d.split("[")[0]
            d = ",".join(d.split("[")[1].split("]")[0].split(",")[:-1])
            b.close()
            b = open(r"mods/modlist.py", "w+")
            b.write(c+"["+d+"]")
            b.close()
            from mods import modlist
    else:
        print("??????????")

# pygame.quit()
