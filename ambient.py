#import numpy as np
from random import *
import time
import sys, pygame
import csv
from pygame.locals import * 
from scipy.spatial import distance

class Ant:
    def __init__(self, size, prob, radius):
        self.dead = self.lottery(prob)
        self.x = self.randPosition(size)
        self.y = self.randPosition(size)
        self.carried = False
        self.carrying = None
        self.lastMove = None
        self.label = 1
        self.data1 = 0.0
        self.data2 = 0.0

    def randPosition(self,size):
        return randint(0, size)

    def lottery(self, prob):
        return False if randint(0, 100) > prob else True

    def setPosition(self):
        if not self.dead:
            self.x = self.randPosition(size)
            self.y = self.randPosition(size)
            return;
        samePosition = True
        while samePosition:
            samePosition = False
            self.x = self.randPosition(size)
            self.y = self.randPosition(size)
            for i in range(len(ants)):
                if ants[i].dead and ants[i].x == self.x and ants[i].y == self.y:
                    samePosition = True

    def moveUp(self):
        if self.lastMove == DOWN:
            self.moveDown()
            return;
        if self.x - 1 < 0:
            self.x = size
        else:
            self.x = self.x - 1
        if not self.carrying is None:
            self.carrying.x = self.x   
        self.lastMove = UP           

    def moveDown(self):
        if self.lastMove == UP:
            self.moveUp()
            return;
        if self.x + 1 >= size:
            self.x = 0
        else:
            self.x = self.x + 1
        if not self.carrying is None:
            self.carrying.x = self.x 
        self.lastMove = DOWN

    def moveLeft(self):
        if self.lastMove == RIGHT:
            self.moveRight()
            return;
        if self.y - 1 < 0:
            self.y = size
        else:
            self.y = self.y - 1
        if not self.carrying is None:
            self.carrying.y = self.y 
        self.lastMove = LEFT

    def moveRight(self):
        if self.lastMove == LEFT:
            self.moveLeft()
            return;
        if self.y + 1 >= size:
            self.y = 0
        else:
            self.y = self.y + 1
        if not self.carrying is None:
            self.carrying.y = self.y 
        self.lastMove = RIGHT

    def randMove(self):
        if self.dead:
    	    return;
        rand = randrange(0,4)
        if rand == 0: self.moveUp() 
        if rand == 1: self.moveDown()
        if rand == 2: self.moveRight()
        if rand == 3: self.moveLeft()



    def leaveProb(self): #Only works with radius 1 by now || Returns the prob of leave an ant
        if self.dead:
            return 0
        sizeRadius = ( ( (radius*2) + 1 )**2 ) - 1
        nDead = 0
        if self.x - 1 < 0:
            upX = size
        else:
            upX = self.x - 1
        if self.x + 1 > size:
            downX = 0
        else:
            downX = self.x + 1
        if self.y - 1 < 0:
            leftY = size
        else:
            leftY = self.y - 1
        if self.y + 1 > size:
            rightY = 0
        else:
            rightY = self.y + 1
        if isDead(upX,leftY,self.carrying.label): nDead = nDead + 1
        if isDead(upX,self.y,self.carrying.label): nDead = nDead + 1
        if isDead(upX,rightY,self.carrying.label): nDead = nDead + 1
        if isDead(self.x,leftY,self.carrying.label): nDead = nDead + 1
        # if self.isDead(self.x,self.y): nDead = nDead + 1
        if isDead(self.x,rightY,self.carrying.label): nDead = nDead + 1
        if isDead(downX,leftY,self.carrying.label): nDead = nDead + 1
        if isDead(downX,self.y,self.carrying.label): nDead = nDead + 1
        if isDead(downX,rightY,self.carrying.label): nDead = nDead + 1
        return nDead/sizeRadius

    def carryProb(self):
        if self.dead:
            return 0
        sizeRadius = ( ( (radius*2) + 1 )**2 ) - 1
        nDead = 0
        if self.x - 1 < 0:
            upX = size
        else:
            upX = self.x - 1
        if self.x + 1 > size:
            downX = 0
        else:
            downX = self.x + 1
        if self.y - 1 < 0:
            leftY = size
        else:
            leftY = self.y - 1
        if self.y + 1 > size:
            rightY = 0
        else:
            rightY = self.y + 1
        if self.isDead(upX,leftY): nDead = nDead + 1
        if self.isDead(upX,self.y): nDead = nDead + 1
        if self.isDead(upX,rightY): nDead = nDead + 1
        if self.isDead(self.x,leftY): nDead = nDead + 1
        # if self.isDead(self.x,self.y): nDead = nDead + 1
        if self.isDead(self.x,rightY): nDead = nDead + 1
        if self.isDead(downX,leftY): nDead = nDead + 1
        if self.isDead(downX,self.y): nDead = nDead + 1
        if self.isDead(downX,rightY): nDead = nDead + 1
        return 1 - nDead/sizeRadius

    def decision(self):
        # print(( self.leaveProb() + noise )*100)
        if self.dead:
            return;
        if self.carrying is None and self.isDead(self.x, self.y): #Can carry one
            if self.lottery(( self.carryProb() + noise )*100):
                self.carry()
                return;
        if not self.carrying is None and not self.isDead(self.x, self.y):
            if self.lottery(( self.leaveProb() + noise )*100):
                self.leave()
                return;

    def carry(self):
        ambientDead[self.y - 1][self.x - 1].carried = True
        self.carrying = ambientDead[self.y - 1][self.x - 1]
        # for i in range(len(ants)):
        #     if(ants[i].x == self.x and ants[i].y == self.y):
        #         ants[i].carried = True
        #         self.carrying = ants[i]
        #         return;

    def leave(self):
        self.carrying.carried = False
        self.carrying = None  

    def isDead(self,x,y):
        if(not ambientDead[y-1][x-1] is None and ambientDead[y-1][x-1] != self.carrying):
            return True
        return False
        # for i in range(len(ants)):
        #     if ants[i].x == x and ants[i].y == y and ants[i].dead and ants[i] != self.carrying:
        #         return True
        # return False




size = 40
allAnts = []
ants = []
aliveAnts = []
nAnts = size*5
probDead = 90
radius = 1
ambient = []
ambientDead = []
noise = -0.01
maxIteractions = 500000
minDead = 200

#Colors
darkGreen = (0,30,0)
white = (200,200,200)
darkBlue = (0,0,128)
grey = (100,100,100)
lightGrey = (150,150,150)
yellow = (212,175,55)
red = (255, 0, 0)
green = (0,255,0)

#Moves
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

screen = pygame.display.set_mode((1000,1000))

#--------------------READ FILE----------------------
def readFile():
    cont = 0;
    with open('data.csv', newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ' ', quotechar=',')
        for row in spamreader:
            linha = row[0].split(",")
            ants[cont].data1 = float(linha[0])
            ants[cont].data2 = float(linha[1])
            ants[cont].label = int(linha[2])
            cont = cont + 1

#---------------------------------------------------

def isDead(x,y,label):
    if not ambientDead[y-1][x-1] is None: 
        if ambientDead[y-1][x-1].label == label:
            return True
    return False
    # for i in range(len(ants)):
    #     if ants[i].x == x and ants[i].y == y and ants[i].dead:
    #         return True
    # return False

def euclidean(x1,x2,y1,y2):
    return distance.euclidean([x1,y1],[x2,y2])

def initAmbient():
    for i in range(size):
        line = []
        lineDead = []
        for j in range(size):
            line.append(0)
            lineDead.append(None)
        ambient.append(line)
        ambientDead.append(lineDead)
    for j in range(nAnts):
        ant = Ant(size, probDead, radius)
        if not ant.dead:
        	aliveAnts.append(ant)
        else:
            ants.append(ant)
        allAnts.append(ant)
    while len(ants) < minDead:
        ant = Ant(size, probDead, radius)
        ant.dead = True
        ant.setPosition()
        ants.append(ant)
        allAnts.append(ant)

    readFile()



def resetAmbient():
    for i in range(size):
        for j in range (size):
            ambient[i][j] = 0
            ambientDead[i][j] = None

def resetDead():
    for i in range(size):
        for j in range (size):
            ambientDead[i][j] = None

def printAmbient():
    for i in range(size): #i = y
        for j in range(size): #j = x
            if(j == size - 1):
                print("%d\n" %ambient[i][j], end = "")
            else:
                print("%d " %ambient[i][j], end = "")
    print()

def updateDead():
    resetDead()
    for i in range(len(ants)):
        if( ants[i].carried == False):
            ambientDead[ ants[i].y - 1][ ants[i].x - 1] = ants[i]

def updateAmbient():
    resetAmbient()
    for i in range(len(ants)):
        if( ants[i].carried == False):
            ambient[ ants[i].y - 1][ ants[i].x - 1 ] = ants[i].label
            ambientDead[ ants[i].y - 1][ ants[i].x - 1] = ants[i]
    for i in range(len(aliveAnts)):
        if not aliveAnts[i].carrying is None:
            ambient[ aliveAnts[i].y-1 ][ aliveAnts[i].x-1 ] = 6
        else:
            ambient[ aliveAnts[i].y-1 ][ aliveAnts[i].x-1 ] = 5


    # for k in range(nAnts):
    #     if allAnts[k].dead:
    #         if ambient[ allAnts[k].y-1 ][ allAnts[k].x-1 ] != 2 and ambient[ allAnts[k].y-1 ][ allAnts[k].x-1 ] != 3:
    #             ambient[ allAnts[k].y-1][ allAnts[k].x-1 ] = 1
    #     else:
    #         if not allAnts[k].carrying is None:
    #             ambient[ allAnts[k].y-1 ][ allAnts[k].x-1 ] = 3
    #         else:
    #             ambient[ allAnts[k].y-1 ][ allAnts[k].x-1 ] = 2

def drawAmbient():
    # Draw lines
	# for i in range(size):
	# 	pygame.draw.line(screen, white, [0, i*1000/size], [size*100, i*1000/size], (1))
	# 	pygame.draw.line(screen, white, [i*1000/size, 0], [i*1000/size, size*100], (1))
    screen.fill( darkGreen )
    for i in range(size):
        for j in range(size):
            if ambient[i][j] == 5:
                pygame.draw.rect(screen, darkBlue, (i*1000/size,j*1000/size,1000/size,1000/size), 0)
            if ambient[i][j] == 1:
                pygame.draw.rect(screen, grey, (i*1000/size,j*1000/size,1000/size,1000/size), 0)
            if ambient[i][j] == 2:
                pygame.draw.rect(screen, yellow, (i*1000/size,j*1000/size,1000/size,1000/size), 0)
            if ambient[i][j] == 3:  
                pygame.draw.rect(screen, red, (i*1000/size,j*1000/size,1000/size,1000/size), 0)  
            if ambient[i][j] == 4:
                pygame.draw.rect(screen, green, (i*1000/size,j*1000/size,1000/size,1000/size), 0)
            if ambient[i][j] == 6:
                pygame.draw.rect(screen, darkBlue, (i*1000/size,j*1000/size,1000/size,1000/size), 0)
                pygame.draw.rect(screen, lightGrey, (i*1000/size + 200/size,j*1000/size + 200/size,600/size,600/size), 0)



def main():
    initAmbient()
    print(len(ants))
    print(len(aliveAnts))
    updateAmbient()
    pygame.display.update()
    drawAmbient() 
    pygame.image.save(screen,"deadAnts-init.png")
    for k in range(maxIteractions):
        for i in range(len(aliveAnts)):
            aliveAnts[i].randMove()
            aliveAnts[i].decision()
            updateDead()
        if k%100000 == 0:
            updateAmbient()
            pygame.display.update()
            drawAmbient() 
            pygame.image.save(screen,"deadAnts-" + str(k) + ".png")
            # print(k)
    while(len(aliveAnts)>0): 
        for j in range(len(aliveAnts)-1, -1, -1):
            print(j)
            if(aliveAnts[j].carrying is None):
                aliveAnts.pop(j)
        for i in range(len(aliveAnts)):
            aliveAnts[i].randMove()
            aliveAnts[i].decision()
        updateAmbient()
        pygame.display.update()
        drawAmbient() 
        
        # else : print(iterations)
        # time.sleep(1)
    while(1):
        updateAmbient()
        pygame.display.update()
        drawAmbient() 
        pygame.image.save(screen,"deadAnts-final.png")
        print(len(aliveAnts))
        time.sleep(100)

main()
