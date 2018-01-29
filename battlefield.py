# -*- coding: utf-8 -*-
from visual import *
from math import *
import tank1
import tank2

### scene setup
hp_pos = [-300, 300]
hp_dx = [-1, 1]

scene = display(width=900, height=600, center=(0, 285, 0), background=(0.3, 0.3, 0.0))
scene.forward = vector(0, 0, -1)
scene.range = (450, 600, 1)
table = box(length=900, width=1, height=10, color=(0.4, 0.9, 0.2), pos=vector(0, -5, 0))
barrier = [box(length=10, width=1, height=60, pos=vector(-145, 30, 0), color=(1, 1, 1)),
           box(length=10, width=1, height=60, pos=vector(145, 30, 0), color=(1, 1, 1))]
hp = [box(length=250, width=1, height=20.0, pos=vector(hp_pos[0], 520, 0), color=(1, 0, 0)),
      box(length=250, width=1, height=20.0, pos=vector(hp_pos[1], 520, 0), color=(1, 0, 0))]

ready = False
player = 0
dt = 0.1
eps = 1

pw_max = 140
dpw = 4
power = 1
###

### tank construction
tank = [tank1.construction(), tank2.construction()]
for i in range(2):
    if tank[i][2].radius<tank[i][3].radius:
        tank[i][3].radius=tank[i][2].radius
        
f = [frame(), frame()]

for i in range(2):
    for j in tank[i]:
        j.frame = f[i]

tank[0].append(250)
tank[1].append(250)
tank[1][2].rotate(angle=-pi/2, axis=vector(scene.forward), origin=tank[player][2].pos)
tank[0][2].rotate(angle=-pi/2, axis=vector(scene.forward), origin=tank[player][2].pos)
tank[0].append(tank[0][3].radius)
tank[1].append(tank[1][3].radius)
###

def reset():
    tank[0][0].pos = vector(-300, tank[0][0].height / 2, 0)
    tank[0][1].pos = vector(-300, tank[0][0].height+tank[0][1].height / 2, 0)
    tank[0][2].pos = tank[0][1].pos
    tank[0][3].pos = tank[0][1].pos
    tank[0][4] = 250
    tank[1][0].pos = vector(300, tank[1][0].height / 2, 0)
    tank[1][1].pos = vector(300, tank[1][0].height+tank[1][1].height / 2, 0)
    tank[1][2].pos = tank[1][1].pos
    tank[1][3].pos = tank[1][1].pos
    tank[1][4] = 250
    
def reset_bomb():
    tank[player][3].radius = tank[player][5] #we need to save the original radius of shiao dui yuan's bomb radius
    tank[player][3].color = (1, 1, 1)
    tank[player][3].pos = tank[player][1].pos
    tank[player][3].visible = True
    
def explosion():
    global player
    k = 0
    tank[player][3].v = (0, 0, 0)
    tank[player][3].color = (1, 0, 0)
    while True:
        rate(100)
        if k == 0:
            tank[player][3].radius += tank[player][5] / 10
            if tank[player][3].radius >= 10 * tank[player][5]:
                k = 1
        elif k == 1:
            tank[player][3].radius -= tank[player][5] / 10
            if tank[player][3].radius <= 0:
                break

def fire():
    global player
    global power
    tank[player][3].v = power * norm(tank[player][2].axis)
    while not (hitOpponent() or hitField()):
        rate(100)
        tank[player][3].pos += tank[player][3].v * dt
        tank[player][3].v += vector(0, -9.8, 0) * dt
    explosion()
    if hitOpponent():
        tank[player ^ 1][4] -= 50
        while hp[player ^ 1].length > tank[player ^ 1][4]:
            rate(100)
            if hp[player^1].length <= 2:
                GG()
                break
            else:
                hp[player^1].length -= 2
            hp_pos[player^1] += hp_dx[player^1]
            hp[player^1].pos = vector(hp_pos[player^1], 520, 0)
    reset_bomb()
    player ^= 1
    battle_phase1()
    
def GG():
    hp[player^1].length = 0
    t = 0
    mag = [random.uniform(100, 200), random.uniform(100, 200), random.uniform(100, 200)]
    theta = [random.uniform(0, pi), random.uniform(0, pi), random.uniform(0, pi)]
    ro = [random.uniform(-pi/20, pi/20), random.uniform(-pi/20, pi/20), random.uniform(-pi/20, pi/20)]
    v = [vector(mag[0] * cos(theta[0]), mag[0] * sin(theta[0]), 0),
         vector(mag[1] * cos(theta[1]), mag[1] * sin(theta[1]), 0),
         vector(mag[2] * cos(theta[2]), mag[2] * sin(theta[2]), 0)]
    while t < 1:        
        rate(100)
        for i in range(3):
            tank[player ^ 1][i].pos += v[i] * dt
            v[i] += vector(0, -9.8, 0) * dt
            tank[player ^ 1][i].rotate(angle=ro[i], axis=vector(scene.forward), origin=tank[player ^ 1][i].pos)
        t += dt
    explo = [sphere(radius=1), sphere(radius=1), sphere(radius=1)]
    for i in range(3):
        explo[i].pos = tank[player ^ 1][i].pos
        explo[i].color = (1, 0, 0)
    while explo[0].radius < tank[player ^ 1][0].length or explo[0].radius < tank[player ^ 1][0].height or explo[0].radius < tank[player ^ 1][1].length or explo[0].radius < tank[player ^ 1][0].height:
        rate(100)
        for i in range(3):
            explo[i].radius += 1
    for i in range(2):
        tank[player ^ 1][i].length = 0.2
        tank[player ^ 1][i].height = 0.2
    tank[player ^ 1][2].axis = vector(0.1, 0, 0)
    tank[player ^ 1][2].radius = 0.1
    tank[player ^ 1][3].radius = 0.1
    while explo[0].radius > 0:
        rate(100)
        for i in range(3):
            explo[i].radius -= 1
    text(text='GAME OVER', align='center', depth=0.3, color=color.red, height=100,width=[1000],pos=(0,285,0))
    while t<10:
        rate(100)
        t+=dt
    exit()
    
def hitOpponent():
    #tank[player][0][1]->body; [2]->Barrel; [3]->bomb
    #print tank[player ^ 1][0].pos.x - tank[player ^ 1][0].length / 2, tank[player][3].pos.x, tank[player ^ 1][0].pos.x + tank[player ^ 1][0].length / 2, '=', tank[player][3].pos.y
    for i in range(2):
        if tank[player ^ 1][i].pos.x - tank[player ^ 1][i].length / 2 <= tank[player][3].pos.x + tank[player][5] and\
           tank[player][3].pos.x - tank[player][5] <= tank[player ^ 1][i].pos.x + tank[player ^ 1][i].length / 2 and\
           tank[player ^ 1][i].pos.y - tank[player ^ 1][i].height / 2 <= tank[player][3].pos.y + tank[player][5] and\
           tank[player][3].pos.y - tank[player][5] <= tank[player ^ 1][i].pos.y + tank[player ^ 1][i].height / 2:
            return True
    if mag(tank[player ^ 1][2].pos - tank[player][3].pos) + mag(tank[player ^ 1][2].pos + tank[player ^ 1][2].axis - tank[player][3].pos) - mag(tank[player ^ 1][2].axis) < eps * (tank[player][5] + tank[player ^ 1][2].radius):
        return True
    return False



def hitField():
    if (tank[player][3].pos.y - 3) <= 0:
        return True
    if abs(tank[player][3].pos.x)>450:
        return True
    for i in range(2):
        if barrier[i].pos.x - barrier[i].length / 2 <= tank[player][3].pos.x and\
           tank[player][3].pos.x <= barrier[i].pos.x + barrier[i].length / 2 and\
           barrier[i].pos.y - barrier[i].height / 2 <= tank[player][3].pos.y and\
           tank[player][3].pos.y <= barrier[i].pos.y + barrier[i].height/2:
            return True
    return False

    
def outrange(lr, ud):
    global player
    if player==0:
        if lr<0:
            if tank[player][0].pos.x-tank[player][0].length/2<-450 or tank[player][1].pos.x-tank[player][1].length/2<-450 or tank[player][2].pos.x+tank[player][2].axis.x<-450:
                return True
        elif lr>0 :
            if tank[player][0].pos.x+tank[player][0].length/2>-150 or tank[player][1].pos.x+tank[player][1].length/2>-150 or tank[player][2].pos.x+tank[player][2].axis.x>-150:
                return True
        if (ud>0 and tank[player][2].axis.y<0) or (ud<0 and tank[player][2].axis.y>0):
            if tank[player][2].pos.x+tank[player][2].axis.x>-150:
                return True
        elif (ud>0 and tank[player][2].axis.y>0) or (ud<0 and tank[player][2].axis.y<0):
            if tank[player][2].pos.x+tank[player][2].axis.x<-450:
                return True
    else:
        if lr<0:
            if tank[player][0].pos.x-tank[player][0].length/2<150 or tank[player][1].pos.x-tank[player][1].length/2<150 or tank[player][2].pos.x+tank[player][2].axis.x<150:
                return True
        elif lr>0:
            if tank[player][0].pos.x+tank[player][0].length/2>450 or tank[player][1].pos.x+tank[player][1].length/2>450 or tank[player][2].pos.x+tank[player][2].axis.x>450:
                return True
        if (ud>0 and tank[player][2].axis.y<0) or (ud<0 and tank[player][2].axis.y>0):
            if tank[player][2].pos.x+tank[player][2].axis.x<150:
                return True
        elif (ud>0 and tank[player][2].axis.y>0) or (ud<0 and tank[player][2].axis.y<0):
            if tank[player][2].pos.x+tank[player][2].axis.x>450:
                return True
    return False
    
def battle_phase1():
    ready = False
    global player
    dtheta = [-1, 1]
    if player==1:
        while not ready:
            rate(100)
            move_instruction = scene.waitfor('keydown')
            if move_instruction.key == "j" and not outrange(-2, 0):
                tank[player][0].pos += (-5, 0, 0)
                tank[player][1].pos += (-5, 0, 0)
                tank[player][2].pos += (-5, 0, 0)
                tank[player][3].pos += (-5, 0, 0)
            elif move_instruction.key == "l" and not outrange(2, 0):   
                tank[player][0].pos += (5, 0, 0)
                tank[player][1].pos += (5, 0, 0)
                tank[player][2].pos += (5, 0, 0)
                tank[player][3].pos += (5, 0, 0)
            elif move_instruction.key == "i" and not outrange(0, 2):    
                tank[player][2].rotate(angle=dtheta[player]*pi/180, axis=vector(scene.forward), origin=tank[player][2].pos)
            elif move_instruction.key == "k" and not outrange(0, -2):
                tank[player][2].rotate(angle=-dtheta[player]*pi/180, axis=vector(scene.forward), origin=tank[player][2].pos)
            elif move_instruction.key == "u":
                ready = True
    elif player==0:
        while not ready:
            rate(100)
            move_instruction = scene.waitfor('keydown')
            if move_instruction.key == "a" and not outrange(-2, 0):
                tank[player][0].pos += (-5, 0, 0)
                tank[player][1].pos += (-5, 0, 0)
                tank[player][2].pos += (-5, 0, 0)
                tank[player][3].pos += (-5, 0, 0)
            elif move_instruction.key == "d" and not outrange(2, 0):   
                tank[player][0].pos += (5, 0, 0)
                tank[player][1].pos += (5, 0, 0)
                tank[player][2].pos += (5, 0, 0)
                tank[player][3].pos += (5, 0, 0)
            elif move_instruction.key == "w" and not outrange(0, 2):    
                tank[player][2].rotate(angle=dtheta[player]*pi/180, axis=vector(scene.forward), origin=tank[player][2].pos)
            elif move_instruction.key == "s" and not outrange(0, -2):
                tank[player][2].rotate(angle=-dtheta[player]*pi/180, axis=vector(scene.forward), origin=tank[player][2].pos)
            elif move_instruction.key == "q":
                ready = True
    battle_phase2()
    tank[player][3].pos = tank[player][2].pos + tank[player][2].axis
    fire()

def battle_phase2():
    global power
    power = 1
    pw_block = box(length=power, width=1, height=5.0, pos=vector(tank[player][1].pos.x-(pw_max/2),tank[player][1].pos.y+tank[player][1].height / 2+20, 0), color=(0,1,0))
    pw_contour_r = box(length=0.6, width=1, height=5.0, pos=vector(tank[player][1].pos.x-(pw_max/2)-1,tank[player][1].pos.y+tank[player][1].height / 2+20, 0), color=(0,0,0))
    pw_contour_l = box(length=0.6, width=1, height=5.0, pos=vector(tank[player][1].pos.x+(pw_max/2)+1,tank[player][1].pos.y+tank[player][1].height / 2+20, 0), color=(0,0,0))
    pw_contour_t = box(length=pw_max, width=1, height=0.6, pos=vector(tank[player][1].pos.x,tank[player][1].pos.y+tank[player][1].height / 2+20+3, 0), color=(0,0,0))
    pw_contour_b = box(length=pw_max, width=1, height=0.6, pos=vector(tank[player][1].pos.x,tank[player][1].pos.y+tank[player][1].height / 2+20-3, 0), color=(0,0,0))
    ready_fire = False
    if player==1:
        while not ready_fire :
            rate(100)
            move_instruction = scene.waitfor('keydown')
            if(move_instruction.key == "i"):
                ready_fire = True
            if(move_instruction.key == "k"): #remember ".key"
                if(power <= pw_max): 
                    power += dpw
                    pw_block.length = power
                    pw_block.pos.x += dpw / 2  
                else:
                    ready_fire = True
    elif player==0:
        while not ready_fire :
            rate(100)
            move_instruction = scene.waitfor('keydown')
            if(move_instruction.key == "w"):
                ready_fire = True
            if(move_instruction.key == "s"): #remember ".key"
                if(power <= pw_max): 
                    power += dpw
                    pw_block.length = power
                    pw_block.pos.x += dpw / 2  
                else:
                    ready_fire = True
    pw_block.length = pw_contour_r.length = pw_contour_l.length = pw_contour_t.length = pw_contour_b.length = 0

### main
reset()    
while not ready:
    battle_phase1()
###
