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


