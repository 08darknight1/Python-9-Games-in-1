import random

import pygame
import os

class Entity:
    def __init__(self, name, width, height, speed, posX, posY):
        self.name = name
        self.width = width
        self.height = height
        self.posX = posX
        self.posY = posY
        self.speed = speed

    def CreatePyGameObject(self, debugRect: bool, posX: float, posY: float):
        if debugRect:
            self.pyGameObject = pygame.Rect(posX, posY, self.width, self.height)
        else:
            print("Waiting for code implementation of definitive object!")

    def ReturnPyGameObject(self):
        return self.pyGameObject

class Meteor(Entity):
    def __init__(self, name, width, height, speed, posX, posY, debug):
        super().__init__(name, width, height, speed, posX, posY)

        self.debug = debug

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.spriteSize = []

        self.currentSprite = random.randrange(0, 9)

        self.meteorSprites = pygame.image.load(script_dir + "/Resources/Meteor-Spinning-Sheet.png").convert_alpha()

        self.correctCollider = False

        self.CreatePyGameObject(self.debug, self.posX, self.posY)

    def CreatePyGameObject(self, debugRect: bool, posX: float, posY: float):
        self.pyGameObject = pygame.Rect(posX, posY, self.width, self.height)

    def ReturnPyGameObject(self):
        return self.pyGameObject

    def DrawCurrentSprite(self):
        #print("Hi, my name is ", self.name, " and my currentSprite is ", self.currentSprite)
        areaX = 50

        if self.currentSprite != 0:
            areaX = areaX * self.currentSprite

        surface = pygame.Surface((50, 50))

        surface.set_colorkey((255,255,255))

        surface.blit(self.meteorSprites, (0, 0), (areaX, 0, 50, 50))

        if not self.correctCollider:
            mask = pygame.mask.from_surface(surface)

            newRect = mask.get_bounding_rects()

            self.correctCollider = True
            self.pyGameObject.fit(newRect[0])

            self.pyGameObject.x = self.posX
            self.pyGameObject.y = self.posY

            #print("Set new rect for ", self.name, " - X{", self.pyGameObject.x, "}-Y{", self.pyGameObject.y, "}")
        return surface

    def SetNextFrame(self):
        if self.currentSprite < 8:
            self.currentSprite = self.currentSprite + 1
        else:
            self.currentSprite = 0

class Player(Entity):
    def __init__(self, name, width, height, speed, posX, posY, debug):
        super().__init__(name, width, height, speed, posX, posY)

        self.debug = debug

        self.dead = False

        self.playerSprites = []

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship.png").convert_alpha())
        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship Turning.png").convert_alpha())

        self.currentSprite = self.playerSprites[0]

        self.CreatePyGameObject(debug, self.posX, self.posY)

    def CreatePyGameObject(self, debugRect: bool, posX: float, posY: float):
        self.pyGameObject = pygame.Rect(posX, posY, self.width, self.height)

        if not debugRect:
            self.SetNewPlayerSprite(0,False)

    def SetNewPlayerSprite(self, index : int, flip: bool):
        self.currentSprite = self.playerSprites[index]

        self.currentSprite = pygame.transform.flip(self.currentSprite, flip, False)
        #print("Flipped equals: ", flip)

        self.currentSprite.set_colorkey((255,255,255))


