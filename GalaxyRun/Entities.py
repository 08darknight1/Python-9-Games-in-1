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

        self.currentSpriteIndex = random.randrange(0, 9)

        self.currentSprite = 0

        self.meteorSprites = pygame.image.load(script_dir + "/Resources/Meteor-Spinning-Sheet.png").convert_alpha()

        self.CreatePyGameObject(self.debug, self.posX, self.posY)

        self.currentMask : pygame.mask

    def CreatePyGameObject(self, debugRect: bool, posX: float, posY: float):
        if not debugRect:
            surface = self.DrawCurrentSprite()

            self.currentSprite = surface

            self.pyGameObject = pygame.Rect(posX, posY, self.width, self.height)

            self.currentMask = pygame.mask.from_surface(surface)

            #self.pyGameObject = spriteRect
        else:
            self.pyGameObject = pygame.Rect(posX, posY, self.width, self.height)

    def ReturnPyGameObject(self):
        return self.pyGameObject

    def DrawCurrentSprite(self):
        areaX = 50

        if self.currentSprite != 0:
            areaX = areaX * self.currentSpriteIndex

        surface = pygame.Surface((50, 50))

        surface.set_colorkey((255,255,255))

        self.currentSprite = surface.blit(self.meteorSprites, (0, 0), (areaX, 0, 50, 50))

        self.currentMask = pygame.mask.from_surface(surface)

        #Enable this next part to test the mask collision and comment the return surface
        #surfaceFromMask = self.currentMask.to_surface()

        #surfaceFromMask.set_colorkey((0, 0, 0))

        #return surfaceFromMask

        return surface


    def SetNextFrame(self):
        if self.currentSpriteIndex < 9:
            self.currentSpriteIndex = self.currentSpriteIndex + 1
        else:
            self.currentSpriteIndex = 0

class Player(Entity):
    def __init__(self, name, width, height, speed, posX, posY, debug):
        super().__init__(name, width, height, speed, posX, posY)

        self.debug = debug

        self.dead = False

        self.playerSprites = []

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship.png").convert_alpha())
        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship Turning.png").convert_alpha())

        self.thrusterSprites = pygame.image.load(script_dir + "/Resources/ShipThruster-Sheet.png").convert_alpha()

        self.currentThrusterFrame = 0

        self.currentSprite = self.playerSprites[0]

        self.CreatePyGameObject(debug, self.posX, self.posY)

        self.currentMask = pygame.mask.from_surface(self.currentSprite)

    def CreatePyGameObject(self, debugRect: bool, posX: float, posY: float):
        self.pyGameObject = pygame.Rect(posX, posY, self.width, self.height)

        if not debugRect:
            self.SetNewPlayerSprite(0,False)


    def SetNewPlayerSprite(self, index : int, flip: bool):
        self.currentSprite = self.playerSprites[index]

        self.currentSprite = pygame.transform.flip(self.currentSprite, flip, False)

        self.currentSprite.set_colorkey((255,255,255))

        self.currentMask = pygame.mask.from_surface(self.currentSprite)

        #This right here needs to be enabled to show the masks to test collision
        #maskToSurface = self.currentMask.to_surface()

        #maskToSurface.set_colorkey((0, 0, 0))

        #self.currentSprite = maskToSurface

    def DrawThruster(self):
        areaX = 50

        if self.currentThrusterFrame != 0:
            areaX = areaX * self.currentThrusterFrame

        surface = pygame.Surface((50, 50))

        surface.set_colorkey((255,255,255))

        surface.blit(self.thrusterSprites, (0, 0), (areaX, 38, 50, 50))

        self.currentMask = pygame.mask.from_surface(surface)

        return surface

    def SetNewThrusterFrame(self):
        if self.currentThrusterFrame < 3:
            self.currentThrusterFrame = self.currentThrusterFrame + 1
        else:
            self.currentThrusterFrame = 0