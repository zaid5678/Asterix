from tkinter import *
import os

class Window(Frame):

    def __init__(self, master = None):

        Frame.__init__(self,master)

        self.master = master

        self.init_window()

    def init_window(self):

        self.master.title("Asterix")

        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Exit program", command=self.clientExit)

        quitButton.place(x=160, y=200)

        viewLeaderBoardButton = Button(self, text="View leaderboard", command=self.recieveScores)

        viewLeaderBoardButton.place(x=145, y=150)

        startButton = Button(self, text="Start game", command=self.startGame)

        startButton.place(x=160, y=100)
        
    def clientExit(self):
        exit()

    def startGame(self):
        import Main_project.py

    def recieveScores(self):
        from AllMatrixAndVectorOperations import SortAndSearch
        S = SortAndSearch()
        o = open("AllScores.txt", "r")
        print(S.msort(o))

root = Tk()
root.geometry("400x300")

app = Window(root)

root.mainloop()

import pygame
def imageLoader(image, scale, clip):
    asset = pygame.image.load(image)
    playerClipped = pygame.Surface( (clip[2],clip[3]) )
    playerClipped.blit(asset, (0,0), clip)
    scaledAsset = (clip[2] * scale, clip[3] * scale)
    scaledAsset = pygame.transform.scale(playerClipped, (clip[2] * scale, clip[3] *scale))

    return scaledAsset

import pygame
import random
import math
from imageloader import *
from Question_generation import *
from AllMatrixAndVectorOperations import *

playerRespawnDelay = 120 #Ticks (Frames until the event)

Q = Questions()
S = SortAndSearch()

class Background(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        self.originalAsset = pygame.image.load(image)
        self.image = pygame.transform.scale(self.originalAsset, (width,height) )
        self.rect = self.image.get_rect()

    def update(self):
        return

class Player(pygame.sprite.Sprite):
    def __init__(self, image,scale, clip):
        
        self.asset = imageLoader(image, scale, clip)
        self.image = self.asset
        self.imageColorKey = (0,0,0)
        self.explosionColorKey = 0x454e5b
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.velocityX = 0
        self.velocityY = 0
        self.accelerationX = 0
        self.accelerationY = 0
        self.thrust = 0.5
        self.angle = 0
        self.damping = 0.3
        self.maxVelocity = 8
        self.collision = False
        self.collisionGroup = []
        self.isWaitingToRespawn = False
        self.waitingToRespawn = 0
        self.loadExplosionAnimation()
        self.onSpawn()

    def inputInfo(self,score):
        items = []
        name = str(input("Input name : "))
        ID = S.hashFunction(name.upper())
        entry = (name,score,ID)
        return items

    def loadExplosionAnimation(self):
        self.explosionFrames = []
        self.explosionCurrentFrame = 0
        frameWidth = 24
        for i in range(0,6):
                self.explosionFrames.append( imageLoader("images/Explode4.bmp", 2, (frameWidth*i,0,frameWidth,25)))


    def onSpawn(self):
        self.reset()

    def onDeath(self):
        self.isWaitingToRespawn = True
        self.waitingToRespawn = playerRespawnDelay
        self.explosionCurrentFrame = 0

    def reset(self):
        self.rect.x = 400
        self.rect.y = 300
        self.velocityX = 0
        self.velocityY = 0
        self.accelerationX = 0
        self.accelerationY = 0
        self.collision = False

    def update(self):
        #Process Delayed Events
        if self.isWaitingToRespawn:
                #Update Explosion Animation (Player is Dead)
                if self.explosionCurrentFrame <= len(self.explosionFrames) - 1:
                        self.image = self.explosionFrames[self.explosionCurrentFrame]
                        self.image.set_colorkey(self.explosionColorKey)
                        self.explosionCurrentFrame += 1
                else:
                        self.image = pygame.Surface((0,0))

                self.waitingToRespawn -= 1
                if self.waitingToRespawn <= 0:
                        self.isWaitingToRespawn = False
                        self.reset()
        else:
                #Process Player Input
                controls = self.getPlayerInput()
                self.processControls(controls)
                self.image = pygame.transform.rotate(self.asset, self.angle)
                self.image.set_colorkey(self.imageColorKey)

                #Collision Detection
                self.checkForCollisions()

                #Update Physics
                self.updatePhysics()

    def checkForCollisions(self):
        for gameObject in self.collisionGroup:
                self.collision = self.rect.colliderect(gameObject.rect)
                if self.collision:
                    if not Q.determineWhichQuestionToCreate():
                        self.onDeath() 
                        for gameObject in self.collisionGroup:
                                gameObject.onDeath()
                        break
                    self.collisionGroup.remove(gameObject)

    def getPlayerInput(self):
        up = pygame.key.get_pressed()[pygame.K_UP]
        right = pygame.key.get_pressed()[pygame.K_RIGHT]
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        left = pygame.key.get_pressed()[pygame.K_LEFT]

        return (up, right, down, left)

    def processControls(self, control):
        self.angle = 0
        if control[0] == 1 and control[1] == 0 and control[2] == 0 and control[3] == 0:
                self.angle = 0
        elif control[0] == 1 and control[1] == 1 and control[2] == 0 and control[3] == 0:
                self.angle = 315
        elif control[0] == 0 and control[1] == 1 and control[2] == 0 and control[3] == 0:
                self.angle = 270
        elif control[0] == 0 and control[1] == 1 and control[2] == 1 and control[3] == 0:
                self.angle = 225
        elif control[0] == 0 and control[1] == 0 and control[2] == 1 and control[3] == 0:
                self.angle = 180
        elif control[0] == 0 and control[1] == 0 and control[2] == 1 and control[3] == 1:
                self.angle = 135
        elif control[0] == 0 and control[1] == 0 and control[2] == 0 and control[3] == 1:
                self.angle = 90
        elif control[0] == 1 and control[1] == 0 and control[2] == 0 and control[3] == 1:
                self.angle = 45

        self.accelerationX = self.thrust * (control[1] - control[3])
        self.accelerationY = self.thrust * (control[2] - control[0])

    def updatePhysics(self):
        self.velocityX += self.accelerationX
        self.velocityY += self.accelerationY

        #Apply Damping Horizontal
        if self.velocityX < 0 - self.damping:
                self.velocityX += self.damping
        elif self.velocityX > 0 + self.damping:
                self.velocityX -= self.damping
        else:
                self.velocityX = 0
        #Apply Damping Verticle
        if self.velocityY < 0 - self.damping:
                self.velocityY += self.damping
        elif self.velocityY > 0 + self.damping:
                self.velocityY -= self.damping
        else:
                self.velocityY = 0

        #Cap Velocity (Max Velocity)
        if self.velocityX > self.maxVelocity:
                self.velocityX = self.maxVelocity
        if self.velocityX < self.maxVelocity * -1:
                self. velocityX = self.maxVelocity * -1
        if self.velocityY > self.maxVelocity:
                self.velocityY = self.maxVelocity
        if self.velocityY < self.maxVelocity * -1:
                self. velocityY = self.maxVelocity * -1

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image,scale, clip, bounds, gameObjectTarget, waveManager):

        self.image = imageLoader(image, scale, clip)
        self.image.set_colorkey(0x454e5b)
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 500
        self.velocityX = 0
        self.velocityY = 0
        self.thrust = 0.4
        self.damping = 0.1
        self.maxVelocity = 6
        self.boundX = bounds[0]
        self.boundY = bounds[1]
        self.isWaitingToRespawn = False
        self.waitingToRespawn = 0
        self.target = gameObjectTarget
        self.waveManager = waveManager
        self.onSpawn()

    def onSpawn(self):
        self.reset()

    def onDeath(self):
        self.isWaitingToRespawn = True
        self.waitingToRespawn = playerRespawnDelay
        self.waveManager.enemyHasDied()

    def reset(self):
        if self.waveManager.allowSpawn():
                self.state = 1
                self.rect.x = random.randint(0,self.boundX) * -1
                self.rect.y = random.randint(0,self.boundY) * -1
                self.velocityX = 0
                self.velocityY = 0

                self.waveManager.enemyHasSpawned()
        else:
                self.resetOffScreen()
                self.waveManager.addWaitingSpawn(self)

    def resetOffScreen(self):
        self.rect.x = self.boundX
        self.rect.y = self.boundY

    def update(self):
        #Process Delayed Events
        if self.isWaitingToRespawn:
                self.waitingToRespawn -= 1
                if self.waitingToRespawn <= 0:
                        self.isWaitingToRespawn = False
                        self.reset()
        else:
                self.processState()

                #Apply Damping
                if self.velocityY < 0 - self.damping:
                        self.velocityY += self.damping
                elif self.velocityY > 0 + self.damping:
                        self.velocityY -= self.damping
                else:
                        self.velocityY = 0

                #Cap Velocity (Max Velocity)
                if self.velocityX > self.maxVelocity:
                        self.velocityX = self.maxVelocity
                if self.velocityX < self.maxVelocity * -1:
                        self. velocityX = self.maxVelocity * -1
                if self.velocityY > self.maxVelocity:
                        self.velocityY = self.maxVelocity
                if self.velocityY < self.maxVelocity * -1:
                        self. velocityY = self.maxVelocity * -1

                #Update Our Enemy Position
                self.rect.x += self.velocityX
                self.rect.y += self.velocityY

                #Check the Enemy Bound
                if self.rect.x > self.boundX or self.rect.y > self.boundY:
                        self.onDeath()

    def processState(self):
        #State 1 - Search
        if self.state == 1:
                if math.sqrt((self.rect.x - self.target.rect.x)**2 + (self.rect.y - self.target.rect.y)**2) <= 300:
                        self.state = 2
                else:
                        self.velocityX += self.thrust
                        self.velocityY += self.thrust
        #State 2 - Chase Player
        elif self.state == 2:
                if math.sqrt((self.rect.x - self.target.rect.x)**2 + (self.rect.y - self.target.rect.y)**2) > 300:
                        self.state = 3
                else:
                        #Get Target Vector
                        targetVectorX = self.target.rect.x - self.rect.x
                        targetVectorY = self.target.rect.y - self.rect.y
                        distance = math.sqrt((0 - targetVectorX)**2 + (0 - targetVectorY)**2)
                        targetVectorX /= distance
                        targetVectorY /= distance

                        #Apply Target Thrust
                        self.velocityX += targetVectorX * self.thrust
                        self.velocityY += targetVectorY * self.thrust

        #State 3 - Lost Chase
        elif self.state == 3:
                self.velocityX += self.thrust
                self.velocityY += self.thrust

        

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image,scale, clip, bounds):

        self.image = imageLoader(image, scale, clip)
        self.image.set_colorkey(0x454e5b)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400
        self.velocityX = 6
        self.velocityY = 6
        self.accelerationX = 0
        self.accelerationY = 0
        self.boundX = bounds[0]
        self.boundY = bounds[1]
        self.isWaitingToRespawn = False
        self.waitingToRespawn = 0
        self.reset()

    def onSpawn(self):
        self.reset()

    def onDeath(self):
        self.isWaitingToRespawn = True
        self.waitingToRespawn = playerRespawnDelay

    def reset(self):
        self.rect.x = random.randint(0,self.boundX) * -1
        self.rect.y = random.randint(0,self.boundY) * -1
        
    def update(self):
        #Process Delayed Events
        if self.isWaitingToRespawn:
                self.waitingToRespawn -= 1
                if self.waitingToRespawn <= 0:
                        self.isWaitingToRespawn = False
                        self.reset()
        else:
                self.velocityX += self.accelerationX
                self.velocityY += self.accelerationY
                self.rect.x += self.velocityX
                self.rect.y += self.velocityY

                if self.rect.x > self.boundX or self.rect.y > self.boundY:
                        self.onDeath()
class WaveManager():
    def __init__(self):
        self.currentWave = 1
        self.enemySpawnCount = 0
        self.enemyDeathCount = 0
        self.enemiesPerWave = 3
        self.waitingToSpawn = []
        self.score = 0


    def allowSpawn(self):
        if self.enemySpawnCount >= self.enemiesPerWave:
                return False
        else:
                return True

    def enemyHasSpawned(self):
        self.enemySpawnCount += 1
    
    def enemyHasDied(self):
        self.enemyDeathCount += 1
        self.score += 1

        if self.enemyDeathCount == self.enemiesPerWave:
                self.nextWave()

    def nextWave(self):
        self.enemySpawnCount = 0
        self.enemyDeathCount = 0
        self.enemiesPerWave += 3
        self.currentWave += 1
        #self.currentWaveWaitTime = 0
        #self.isBetweenWaves = True

    def addWaitingSpawn(self, gameObject):
        self.waitingToSpawn.append(gameObject)

    def update(self):
        if self.allowSpawn():
                for gameObject in self.waitingToSpawn:
                        gameObject.reset()


import pygame, sys
from gameobjects import *
from imageloader import *
from AllMatrixAndVectorOperations import *
from Stack import *

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))

gameObjects = []

background = Background("images/Nebula1.bmp", screen.get_width(),screen.get_height())

player = Player("images/Hunter1.bmp", 2, (25,1,23,23))
gameObjects.append(player)
playerRotated = pygame.transform.rotate(player.image, 30)

waveManager = WaveManager()

enemies = []
for i in range(3):
    enemy = Enemy("images/SpacStor.bmp", 1, (101,13,91,59), (screen.get_width() + 91,screen.get_height() + 59), player, waveManager)
    enemies.append(enemy)
    gameObjects.append(enemy)
    player.collisionGroup.append(enemy)

asteroids = []
for i in range(5):
    asteroid = Asteroid("images/Rock2a.bmp", 1, (6,3,80,67), (screen.get_width() + 80,screen.get_height() + 67))
    asteroids.append(asteroid)
    gameObjects.append(asteroid)
    player.collisionGroup.append(asteroid)

scoreBoardFrames = []
numbersWidth = 30
for i in range(0,10):
    scoreBoardFrames.append(imageLoader("images/numbers.bmp", 1, (numbersWidth * i,0,30,49)))
    scoreBoardFrames[i].set_colorkey((0,0,0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #Update Wave Manager
    waveManager.update()

    #Update Objects
    for gameObject in gameObjects:
        gameObject.update()

    
    #Render
    if player.collision:
        screen.fill( (30,0,0) )
    else:
        screen.blit(background.image, (0,0))
    for gameObject in gameObjects:
        screen.blit(gameObject.image, (gameObject.rect.x, gameObject.rect.y))

    #Render Out Score
    firstDigit = waveManager.score % 10
    secondDigit = waveManager.score % 100 - firstDigit
    thirdDigit = waveManager.score % 1000 - firstDigit - secondDigit
    screen.blit(scoreBoardFrames[firstDigit], (64,0))
    screen.blit(scoreBoardFrames[secondDigit // 10], (32,0))
    screen.blit(scoreBoardFrames[thirdDigit // 100], (0,0))

    #Render Out Current Wave
    firstDigit = waveManager.currentWave % 10
    secondDigit = waveManager.currentWave % 100 - firstDigit
    thirdDigit = waveManager.currentWave % 1000 - firstDigit - secondDigit
    screen.blit(scoreBoardFrames[firstDigit], ((800-30),0))
    screen.blit(scoreBoardFrames[secondDigit // 10], ((800-30) - 32,0))
    screen.blit(scoreBoardFrames[thirdDigit // 100], ((800-30) - 64,0))

    pygame.display.flip()

    #Waste Extra Work
    clock.tick(60)
    
class Stack():

    def reverseStack(self,x):
        return x.reverse()
    
    def push(self,x,item):
        return x.append(item)
    
    def pop(self,x):
        self.reverseStack(x)
        return x.remove(x[0])
        self.reverseStack(x)

    def peek(self,items):
        return items[0]

import numpy as np
import math
import random
from Stack import *
St = Stack()

class Matrix():
    
    def generateRandomNumber(self):
        return random.randint(2,3)

    def generateRandomMatrixNumber(self):
        return random.randint(-50,50)

    def add(self,A,B):
        if len(A) == 2:
            a = A[0][0] + B[0][0]
            b = A[0][1] + B[0][1]
            c = A[1][0] + B[1][0]
            d = A[1][1] + B[1][1]
            values = [[a, b],[c, d]]
        elif len(A) == 3:
            a = A[0][0] + B[0][0]
            b = A[0][1] + B[0][1]
            c = A[0][2] + B[0][2]
            d = A[1][0] + B[1][0]
            e = A[1][1] + B[1][1]
            f = A[1][2] + B[1][2]
            g = A[2][0] + B[2][0]
            h = A[2][1] + B[2][1]
            i = A[2][2] + B[2][2]
            values = [[a, b, c], [d, e, f], [g, h, i]]
        return np.mat(values)

    def subtract(self,A,B):
        if len(A) == 2:
            a = A[0][0] - B[0][0]
            b = A[0][1] - B[0][1]
            c = A[1][0] - B[1][0]
            d = A[1][1] - B[1][1]
            values = [[a, b],[c, d]]
        elif len(A) == 3:
            a = A[0][0] - B[0][0]
            b = A[0][1] - B[0][1]
            c = A[0][2] - B[0][2]
            d = A[1][0] - B[1][0]
            e = A[1][1] - B[1][1]
            f = A[1][2] - B[1][2]
            g = A[2][0] - B[2][0]
            h = A[2][1] - B[2][1]
            i = A[2][2] - B[2][2]
            values = [[a, b, c], [d, e, f], [g, h, i]]
        return np.mat(values)

    def create3x3Matrix(self):
        a = self.generateRandomMatrixNumber()
        b = self.generateRandomMatrixNumber()
        c = self.generateRandomMatrixNumber()
        d = self.generateRandomMatrixNumber()
        e = self.generateRandomMatrixNumber()
        f = self.generateRandomMatrixNumber()
        g = self.generateRandomMatrixNumber()
        h = self.generateRandomMatrixNumber()
        i = self.generateRandomMatrixNumber()
        values = [[a, b, c], [d, e, f], [g, h, i]]
        return values

    def create2x2Matrix(self):
        a = self.generateRandomMatrixNumber()
        b = self.generateRandomMatrixNumber()
        c = self.generateRandomMatrixNumber()
        d = self.generateRandomMatrixNumber()
        values = [[a, b],[c, d]]
        return values
    
    def createRandomMatrix(self):
        a = self.generateRandomMatrixNumber()
        b = self.generateRandomMatrixNumber()
        c = self.generateRandomMatrixNumber()
        d = self.generateRandomMatrixNumber()
        e = self.generateRandomMatrixNumber()
        f = self.generateRandomMatrixNumber()
        g = self.generateRandomMatrixNumber()
        h = self.generateRandomMatrixNumber()
        i = self.generateRandomMatrixNumber()
        s = self.generateRandomNumber()
        if s == 2:
            values = [[a, b],[c, d]]
        elif s == 3:
            values = [[a, b, c], [d, e, f], [g, h, i]]
        return values
        
    def createInverseMatrix(self):
        determinant = 0
        while determinant == 0:
            m = self.createRandomMatrix()
            print(np.mat(m))
            determinant = self.DetOfMatrix(m)
        #special case for 2x2 matrix:
        if len(m) == 2:
            return np.mat([[m[1][1]/determinant, -1*m[0][1]/determinant],
                    [-1*m[1][0]/determinant, m[0][0]/determinant]])
        #find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m,r,c)
                cofactorRow.append(((-1)**(r+c)) * self.DetOfMatrix(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        for r in range(len(m)):
            for c in range(len(m)):
                cofactors[r][c] = cofactors[r][c]/determinant
        return cofactors

    def transposeMatrix(self,m):
        return [[row[i] for row in m] for i in range(len(m[0]))]
            
    def getMatrixMinor(self,m,i,j):
        return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

    def DetOfMatrix(self,m):
        if len(m) == 2:
            return(m[0][0]*m[1][1])-(m[0][1]*m[1][0])
        determinant = 0
        for c in range(len(m)):
            determinant += ((-1)**c)*m[0][c]*self.DetOfMatrix(self.getMatrixMinor(m,0,c))
        return determinant

    def multiplyMatrix(self,a,b):
      result=[]
      result1=[]
      while len(a)>0:     
        d=0    
        a1=a[:1:]    
        c=True
        while d<len(a1):
          for x in b:
            for x1 in x:
              St.push(result,x1*a1[0][d])
            d=d+1
        a.pop(0)    
      result=[result[i:i+len(b[0])] for i in range(0, len(result), len(b[0]))]     
      total=0      
      while len(result)>0:
        for X in range(len(result[0])):
          for Y in range(len(b)):
            total=total+result[Y][X]
          St.push(result1,total)
          total=0 
        for s in range(len(b)):
          result.pop(0)  
      result1=[result1[i:i+len(b[0])] for i in range(0, len(result1), len(b[0]))] 
      return (np.mat(result1))

    def checkIfMatricesAreEqual(self,a,b):
        if np.array_equal(a, b):
            return True
        else:
            return False

    def checkIfAnswerIsCorrect(self,a,b):
        if a == b:
            return True
        else:
            return False

class Vector():
    def generateRandomNumber(self):
        return random.randint(2,3)

    def generateRandomVectorNumber(self):
        return random.randint(-50,50)
        
    def createVector2D(self):
        a = self.generateRandomVectorNumber()
        b = self.generateRandomVectorNumber()
        return np.array([a,b]).T

    def createVector3D(self):
        a = self.generateRandomVectorNumber()
        b = self.generateRandomVectorNumber()
        c = self.generateRandomVectorNumber()
        return np.array([a,b,c]).T

    def distanceBetween(self,a,b,c):
        return math.sqrt(a**2 + b**2 + c**2)

    def getShortestDistaceBetweenLines(self,a1,b1,a2,b2):
        c = self.crossProduct(b1,b2)
        numerator = self.dotProduct((a2-a1),c)
        d = self.distanceBetween(c[0],c[1],c[2])
        result = round((numerator/d),2)
        if result < 0:
            result = result * -1
        return result

    def getShortestDistaceBetweenPointAndPlane(self,A,n,d):
        denominator = self.distanceBetween(n[0],n[1],n[2])
        numerator = ((A[0]*n[0]) + (A[1]*n[1]) + (A[2]*n[2])) - d
        if numerator < 0:
            numerator = numerator * -1
        return round(numerator/denominator,2)

    def createVector3D(self):
        a = self.generateRandomVectorNumber()
        b = self.generateRandomVectorNumber()
        c = self.generateRandomVectorNumber()
        return np.array([a,b,c]).T
        
    def dotProduct(self,A,B):
        result = 0
        for i in range(0,len(A)):
            result += (A[i] * B[i])
        return result

    def crossProduct(self,A,B):
      dimension = len(A)
      c = []
      for i in range(dimension):
        c.append(0)
        for j in range(dimension):
          if j != i:
            for k in range(dimension):
              if k != i:
                if k > j:
                  c[i] += A[j]*B[k]
                elif k < j:
                  c[i] -= A[j]*B[k]
      c[1] *= -1
      return c

    def cosInverse(self,x):
        if x < 0:
            x = x * -1
        a = math.acos(x)
        return math.degrees(a)

    def sinInverse(self,x):
        if x < 0:
            x = x * -1
        a = math.asin(x)
        return math.degrees(a)
    
    def angleBetween2LinesOr2Planes(self,b1,b2):
        magA = self.distanceBetween(b1[0],b1[1],b1[2])
        magB = self.distanceBetween(b2[0],b2[1],b2[2])
        aDotb = self.dotProduct(b1,b2)
        angle = self.cosInverse(aDotb/(magA*magB))
        return round(angle,2)

    def angleBetween1LineAnd1Plane(self,b1,b2):
        magA = self.distanceBetween(b1[0],b1[1],b1[2])
        magB = self.distanceBetween(b2[0],b2[1],b2[2])
        aDotb = self.dotProduct(b1,b2)
        angle = self.sinInverse(aDotb/(magA*magB))
        return round(angle,2)

    def checkIfVectorsAreEqual(self,A,B):
        for i in range(0,len(A)-1):
            if A[i] != B[i]:
                return False
        return True
                      
class SortAndSearch():
    def msort(self, x):
        num_lines = sum(1 for line in open('AllScores.txt'))
        result = []
        if num_lines < 20:
            return sorted(x)
        mid = int(num_lines / 2)
        y = msort(x[:mid])
        z = msort(x[mid:])
        i = 0
        j = 0
        while i < len(y) and j < len(z):
            if y[i] > z[j]:
                result.append(z[j])
                j += 1
            else:
                result.append(y[i])
                i += 1
        result += y[i:]
        result += z[j:]
        return result

    def hashFunction(self,name):
        return hashlib.sha244(x).hexdigest()                           
        



from AllMatrixAndVectorOperations import *
import random
from numpy import *
import math
import time

M = Matrix()
V = Vector()

class Questions():

    def printMatricesOrVectors(self,A,B,s):
        print("A = ")
        print(np.mat(A))
        print("B = ")
        print(np.mat(B))
        w = "Find A{}B"
        print(w.format(s))
    
    def inputAnswer(self,name):
        while True:
            try:
                s = "Input {} : "
                answer = float(input((s.format(name))))
                break
            except ValueError:
                print("Invalid data type\nInput integer or float only\n")
        return answer
    
    def generateRandomNumForQuestion(self):
        return random.randint(1,12)

    def printCorrectWord(self):
        x = V.generateRandomNumber()
        if x == 2:
            return "perpendicular"
        elif x == 3:
            return "shortest"

    def determineWhichQuestionToCreate(self):
        print("===========================================")
        u = self.generateRandomNumForQuestion()
        if u == 1:
            return self.multiplyMatricesQuestion()
        elif u == 2:
            return self.addMatricesQuestion()
        elif u == 3:
            return self.subtractMatricesQuestion()
        elif u == 4:
            return self.DetQuestion()
        elif u == 5:
            return self.InverseQuestion()
        elif u == 6:
            return self.dotProductQuestion()
        elif u == 7:
            return self.crossProductQuestion()
        elif u == 8:
            return self.shortestDistanceBetweenSkewLinesQuestion()
        elif u == 9:
            return self.shortestDistanceBetweenLineAndPlaneQuestion()
        elif u == 10:
            return self.angleBetweenTwoLinesQuestion()
        elif u == 11:
            return self.angleBetweenLineAndPlaneQuestion()
        elif u == 12:
            return self.planeParametricToCartesianFormQuestion()

    #Matrix questions

    #1
    def multiplyMatricesQuestion(self):
        x = M.generateRandomNumber()
        if x == 2:
            A = M.create2x2Matrix()
            B = M.create2x2Matrix()
        elif x == 3:
            A = M.create3x3Matrix()
            B = M.create3x3Matrix()
        self.printMatricesOrVectors(A,B,"")
        result = M.multiplyMatrix(A,B)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answer = np.mat([[a,b],[c,d]])
        if x == 3:
            e = self.inputAnswer("e")
            f = self.inputAnswer("f")
            g = self.inputAnswer("g")
            h = self.inputAnswer("h")
            i = self.inputAnswer("i")
            answer = np.mat([[a,b,c],[d,e,f],[g,h,i]])
        if M.checkIfMatricesAreEqual(answer, result):
            print("Correct!")
            return True
        else:
            print("Incorrect!\nThe correct answer is : ")
            print(result)
    
    #2
    def addMatricesQuestion(self):
        x = M.generateRandomNumber()
        if x == 2:
            A = M.create2x2Matrix()
            B = M.create2x2Matrix()
        elif x == 3:
            A = M.create3x3Matrix()
            B = M.create3x3Matrix()
        self.printMatricesOrVectors(A,B,"+")
        result = M.add(A,B)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answer = np.mat([[a,b],[c,d]])
        if x == 3:
            e = self.inputAnswer("e")
            f = self.inputAnswer("f")
            g = self.inputAnswer("g")
            h = self.inputAnswer("h")
            i = self.inputAnswer("i")
            answer = np.mat([[a,b,c],[d,e,f],[g,h,i]])
        if M.checkIfMatricesAreEqual(answer, result):
            print("Correct!")
            return True
        else:
            print("Incorrect!\nThe correct answer is : ")
            print(result)
            return False

    #3
    def subtractMatricesQuestion(self):
        x = M.generateRandomNumber()
        if x == 2:
            A = M.create2x2Matrix()
            B = M.create2x2Matrix()
        elif x == 3:
            A = M.create3x3Matrix()
            B = M.create3x3Matrix()
        self.printMatricesOrVectors(A,B,"-")
        result = M.subtract(A,B)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answer = np.mat([[a,b],[c,d]])
        if x == 3:
            e = self.inputAnswer("e")
            f = self.inputAnswer("f")
            g = self.inputAnswer("g")
            h = self.inputAnswer("h")
            i = self.inputAnswer("i")
            answer = np.mat([[a,b,c],[d,e,f],[g,h,i]])
        if M.checkIfMatricesAreEqual(answer, result):
            print("Great!")
            return True
        else:
            print("Incorrect!\nThe correct answer is : ")
            print(result)
            return False
    #4  
    def DetQuestion(self):
        x = M.generateRandomNumber()
        if x == 2:
            m = M.create2x2Matrix()
        elif x == 3:
            m = M.create3x3Matrix()
        print(np.mat(m))
        det = M.DetOfMatrix(m)
        print("Calculate the determinant of the above matrix")
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer,det):
            print("Well done!")
            return True
        else:
            print("Incorrect!\nThe answer was :",det)
            return False
        
    #5
    def InverseQuestion(self):
        inverseMatrix = M.createInverseMatrix()
        inverseMatrix = np.around(inverseMatrix, decimals=2, out=None)
        v = len(inverseMatrix)
        print("Find the inverse matrix")
        print("Give the following values to",2,"decimal places where appropriate")
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answer = np.mat([[a,b],[c,d]])
        if v == 3:
            e = self.inputAnswer("e")
            f = self.inputAnswer("f")
            g = self.inputAnswer("g")
            h = self.inputAnswer("h")
            i = self.inputAnswer("i")
            answer = np.mat([[a,b,c],[d,e,f],[g,h,i]])
        if M.checkIfMatricesAreEqual(answer, inverseMatrix):
            print("Fantastic!")
            return True
        else:
            print("Incorrect!\nThe correct answer is : ")
            print(inverseMatrix)
            return False

    #Vector questions
    #6
    def dotProductQuestion(self):
        z = V.generateRandomNumber()
        if z == 2:
            A = V.createVector2D()
            B = V.createVector2D()
        elif z == 3:
            A = V.createVector3D()
            B = V.createVector3D()
        self.printMatricesOrVectors(A,B,"∙")
        result = V.dotProduct(A,B)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer, result):
            print("Good work!")
            return True
        else:
            print("Wrong answer!\nThe correct answer is : ",result)
            return False

    #7
    def crossProductQuestion(self):
        A = V.createVector3D()
        B = V.createVector3D()
        self.printMatricesOrVectors(A,B,"×")
        result = V.crossProduct(A,B)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        answer = np.mat([a,b,c]).T
        if V.checkIfVectorsAreEqual(answer,result):
            print("Great!")
            return True
        else:
            print("That's incorrect!\nThe correct answer is : ",result)
            return False

    #8
    def shortestDistanceBetweenSkewLinesQuestion(self):
        a1 = V.createVector3D()
        b1 = V.createVector3D()
        a2 = V.createVector3D()
        b2 = V.createVector3D()
        word = self.printCorrectWord()
        print("L1 :")
        print(a1, "+ λ",b1)
        print("L2 :")
        print(a2, "+ μ",b2)
        print("Find the",word,"distance between the skew lines L1 and L2\nGive your answers to",2,"decimal places")
        result = V.getShortestDistaceBetweenLines(a1,b1,a2,b2)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer,result):
            print("Fantastic!")
            return True
        else:
            print("That's wrong!\nThe correct answer is : ",result,"units")
            return False

    #9
    def shortestDistanceBetweenLineAndPlaneQuestion(self):
        A = V.createVector3D() #point
        n = V.createVector3D() #direction vector
        d = V.generateRandomNumber() #the non x coefficient
        print("The plane π has equation :")
        print("r ∙",n,"=",d)
        print("The point A has position vector :",A)
        word = self.printCorrectWord()
        print("Find the",word,"distance between A and the plane π\nGive your answer to",2,"decimal places")
        result = V.getShortestDistaceBetweenPointAndPlane(A,n,d)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer,result):
            print("Splendid!")
            return True
        else:
            print("That's the wrong answer!\nThe correct answer is : ",result,"units")
            return False

    #10
    def angleBetweenTwoLinesQuestion(self):
        a1 = V.createVector3D()
        b1 = V.createVector3D()
        a2 = V.createVector3D()
        b2 = V.createVector3D()
        print("L1 :")
        print(a1, "+ λ",b1)
        print("L2 :")
        print(a2, "+ μ",b2)
        print("Find the acute angle between the lines L1 and L2\nGive your answer in degrees to",2,"decimal places")
        result = V.angleBetween2LinesOr2Planes(b1,b2)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(result,answer):
            print("Good!")
            return True
        else:
            print("Not correct!\nThe correct answer is : ",result,"degrees")
            return False

    #11   
    def angleBetweenLineAndPlaneQuestion(self):
        a1 = V.createVector3D()
        b1 = V.createVector3D()
        a2 = V.createVector3D()
        b2 = V.createVector3D()
        n1 = V.createVector3D() #direction vector
        d1 = V.generateRandomNumber() #the non x coefficient
        print("The plane π has equation :")
        print("r ∙",n1,"=",d1)
        print("L :")
        print(a1, "+ λ",b1)
        print("Find the acute angle between the plane π and the line L\nGive your answer in degrees to",2,"decimal places")
        result = V.angleBetween1LineAnd1Plane(n1,b1)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer,result):
            print("Excellent!")
            return True
        else:
            print("Not right!\nThe correct answer is : ",result,"degrees")
            return False

    #12
    def planeParametricToCartesianFormQuestion(self):
        a = V.createVector3D()
        b = V.createVector3D()
        c = V.createVector3D()
        print("The plane π has equation :")
        print(a,"+ s",b,"+ t",c)
        print("Given that the cartesian form is ax + by + cz = d, where a, b, c, and d are constants\nConvert this plane in parametric form to cartesian form")
        n = V.crossProduct(b,c)
        answerD = V.dotProduct(n,a)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answerA = np.array([a,b,c]).T
        if M.checkIfMatricesAreEqual(answerA,n) and M.checkIfAnswerIsCorrect(d, answerD):
            print("Great job!")
            return True
        else:
            print("Not correct!\nThe correct answer is : ",end = "")
            print(n[0],"x +",n[1],"y +",n[2],"z =",answerD)
            return False


