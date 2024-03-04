from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt

HEIGHT = 500
WIDTH = 800

#СОЗДАЕМ ОКНО
window = Tk()
window.title('Buble Blaster')
c = Canvas(window, width=WIDTH , height=HEIGHT, bg='darkblue')
c.pack()
SHIP_R = 30

#ПОДЛОДКА
ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ship_id2 = c.create_oval(0, 0, 30, 30, outline='red')

# SHIP_R = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
c.move(ship_id, MID_X, MID_Y)
c.move(ship_id2, MID_X, MID_Y)

def change_ship(first, second):
    c.move(ship_id, first, second)
    c.move(ship_id2, first, second)


def move_ship(event):
    if event.keysym == 'Up':
        change_ship(0,-10)
    elif event.keysym == 'Down':
        change_ship(0,10)
    elif event.keysym == 'Left':
        change_ship(-10,0)
    elif event.keysym == 'Right':
        change_ship(10,0)


c.bind_all('<Key>', move_ship)

#Создаем шарики
bub_id = list()
bub_r = list()
bub_speed = list()
bub_perk = list()

MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPEED = 10
GAP = 100


def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    rand = randint(1,10)
    if rand == 1 or rand == 4:
        id1 = c.create_oval(x-r, y-r, x+r, y+r, fill='red')
        bub_perk.append('end')
    elif rand == 2:
        id1 = c.create_oval(x-r, y-r, x+r, y+r, fill='green')
        bub_perk.append('norm')
    elif rand == 3:
        id1 = c.create_oval(x-r, y-r, x+r, y+r, fill='yellow')
        bub_perk.append('norm')
    else:
        id1 = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
        bub_perk.append('norm')
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPEED))

def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)

BUB_CHANCE = 10

def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y

def del_bubble(i):
    del bub_r[i]
    c.delete(bub_id[i])
    del bub_speed[i]
    del bub_id[i]

def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x, y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)

def distace(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2-x1)**2+(y2-y1)**2)

GAME = True

def collision():
    global GAME
    poits = 0
    for bub in range(len(bub_id)-1, -1, -1):
        if distace(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]):
            poits += (bub_r[bub] + bub_speed[bub])
            del_bubble(bub)
            if bub_perk[bub] == 'end':
                GAME = False
    return poits

score = 0


###TODO реализовать ограничение передвижения подлодки (уходит за края экрана)
while GAME:
    if randint(1, BUB_CHANCE) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    score += collision()
    print(score)
    window.update()
    sleep(0.01)