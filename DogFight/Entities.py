import random
import pygame
import os

class Entity:
    def __init__(self, name, width, height, speed):
        self.name = name
        self.width = width
        self.height = height
        self.speed = speed

    def CreatePyGameObject(self, debug, posX: float, posY: float):
        if debug:
            self.pyGameObject = pygame.Rect(posX, posY, self.width, self.height)
        else:
            print("Waiting for code implementation of definitive object!")

    def ReturnPyGameObject(self):
        return self.pyGameObject

class SpaceShip(Entity):
    def __init__(self, name, width, height, posX, posY, speed, debug, rotation):
        super().__init__(name, width, height, speed)

        self.ammo = 10

        self.life = 2

        self.ammoMax = 10

        self.reloadTimerMax = 5

        self.rotation = rotation

        self.playerSprites = []

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship.png").convert_alpha())
        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship Turning.png").convert_alpha())

        self.thrusterSprites = pygame.image.load(script_dir + "/Resources/ShipThruster-Sheet.png").convert_alpha()

        self.currentThrusterFrame = 0

        self.shipTurning = False

        self.currentSprite = self.playerSprites[0]

        self.CreatePyGameObject(debug, posX, posY)

        value1 = random.randrange(0, 256)

        value2 = random.randrange(0, 256)

        value3 = random.randrange(0, 256)

        self.Color = pygame.Color(value1, value2, value3)

        self.currentMask = pygame.mask.from_surface(self.currentSprite)

    def CreatePyGameObject(self, debug, posX: float, posY: float):
        super().CreatePyGameObject(debug, posX, posY)

    def ReturnShipSprite(self):
        self.currentSprite = pygame.transform.flip(self.currentSprite, self.flip, False)

        imgToReturn = pygame.transform.rotate(self.currentSprite, self.rotation)

        coloredImage = pygame.Surface(imgToReturn.get_size()).convert_alpha()

        coloredImage.fill(self.Color)

        imgToReturn.blit(coloredImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.currentMask = pygame.mask.from_surface(imgToReturn)

        return imgToReturn

    def ChangeShipMainSprite(self, newValue: bool, flip: bool):
        self.shipTurning = newValue

        self.flip = flip

        if self.shipTurning:
            self.currentSprite = self.playerSprites[1]
        else:
            self.currentSprite = self.playerSprites[0]

        self.currentMask = pygame.mask.from_surface(self.currentSprite)

    def ReturnThrusterToDraw(self, flipDirection):
        areaX = 50

        if self.currentThrusterFrame != 0:
            areaX = areaX * self.currentThrusterFrame

        surface = pygame.Surface((50, 15))

        self.thrusterSprites.set_colorkey((255, 255, 255))

        surface.blit(self.thrusterSprites, (0, 0), (areaX, 38, 50, 50))

        if flipDirection == 1:
            surface = pygame.transform.rotate(surface, 90)
        else:
            surface = pygame.transform.rotate(surface, -90)

        surface.set_colorkey((0,0,0))

        return surface

    def SetNewThrusterFrame(self):
        if self.currentThrusterFrame < 3:
            self.currentThrusterFrame = self.currentThrusterFrame + 1
        else:
            self.currentThrusterFrame = 0

class Bullet(Entity):
    def __init__(self, name, width, height, speed, posX, posY, flip:bool, owner: SpaceShip, color: pygame.Color):
        super().__init__(name, width, height, speed)

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.owner = owner

        self.missileColor = color

        self.missileSprites = pygame.image.load(script_dir + "/Resources/MissileSpinning-Sheet.png").convert_alpha()

        self.currentSpriteIndex = 0

        self.currentMissileFrame = 0

        self.flip = flip

        self.CreatePyGameObject(False, posX, posY)

        self.currentMask = pygame.mask.from_surface(self.ReturnCurrentMissileSprite())

    def CreatePyGameObject(self, debug, posX: float, posY: float):
        self.pyGameObject = pygame.Rect(posX, posY, self.width, self.height)

    def ReturnCurrentMissileSprite(self):
        areaX = 50

        if self.currentMissileFrame != 0:
            areaX = areaX * self.currentMissileFrame

        surface = pygame.Surface((50, 50))

        surface.blit(self.missileSprites, (0, 0), (areaX, 0, 50, 50))

        if self.flip:
            surface = pygame.transform.rotate(surface, -180)

        surface.set_colorkey((0, 0, 0))

        coloredImage = pygame.Surface(surface.get_size()).convert_alpha()

        coloredImage.fill(self.missileColor)

        surface.blit(coloredImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.currentMask = pygame.mask.from_surface(surface)

        return surface

    def SetNewMissileFrame(self):
        if self.currentMissileFrame < 5:
            self.currentMissileFrame = self.currentMissileFrame + 1
        else:
            self.currentMissileFrame = 0