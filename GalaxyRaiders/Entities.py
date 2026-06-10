import random
import pygame
import os

class Entity:
    def __init__(self, Name: str, SizeW, SizeH) -> None:
        self.Name = Name
        self.SizeW = SizeW
        self.SizeH = SizeH

    def CreatePyGameObject(self, debug, posX: float, posY: float):
        if debug:
            self.pyGameObject = pygame.Rect(posX, posY, self.SizeW, self.SizeH)
        else:
            print("Waiting for code implementation of definitive object!")

class Ship(Entity):
    def __init__(self, Name: str, SizeW, SizeH, PosX, PosY, rotation, speed) -> None:
        super().__init__(Name, SizeW, SizeH)

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.ammo = 10

        self.ammoMax = 10

        self.reloadTimerMax = 5

        self.shipTurning = False

        self.flip = False

        self.rotation = rotation

        self.speed = speed

        self.playerSprites = []

        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship.png").convert_alpha())
        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship Turning.png").convert_alpha())

        self.currentSprite = self.playerSprites[0]

        self.thrusterSprites = pygame.image.load(script_dir + "/Resources/ShipThruster-Sheet.png").convert_alpha()

        self.currentThrusterFrame = 0

        color_R_Value = random.randrange(0, 256)

        color_G_Value = random.randrange(0, 256)

        color_B_Value = random.randrange(0, 256)

        self.Color = pygame.Color(color_R_Value, color_G_Value, color_B_Value)

        self.currentMask = pygame.mask.from_surface(self.currentSprite)

        self.CreatePyGameObject(True, PosX, PosY)

    def ReturnShipSprite(self):
        self.currentSprite = pygame.transform.flip(self.currentSprite, self.flip, False)

        imgToReturn = pygame.transform.rotate(self.currentSprite, self.rotation)

        #imgToReturn = self.currentSprite

        coloredImage = pygame.Surface(imgToReturn.get_size()).convert_alpha()

        coloredImage.fill(self.Color)

        imgToReturn.blit(coloredImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.currentMask = pygame.mask.from_surface(imgToReturn)

        return imgToReturn

    def CreatePyGameObject(self, debug, posX: float, posY: float):
        super().CreatePyGameObject(debug, posX, posY)

    def ChangeShipMainSprite(self, newValue: bool, flip):
        self.flip = flip

        self.shipTurning = newValue

        if self.shipTurning:
            self.currentSprite = self.playerSprites[1]
        else:
            self.currentSprite = self.playerSprites[0]

        self.currentMask = pygame.mask.from_surface(self.currentSprite)

    def ReturnThrusterToDraw(self):
        areaX = 50

        if self.currentThrusterFrame != 0:
            areaX = areaX * self.currentThrusterFrame

        surface = pygame.Surface((50, 15))

        self.thrusterSprites.set_colorkey((255, 255, 255))

        surface.blit(self.thrusterSprites, (0, 0), (areaX, 38, 50, 50))

        surface.set_colorkey((0,0,0))

        if self.rotation > 0:
            surface = pygame.transform.flip(surface, self.flip, True)

        return surface

    def SetNewThrusterFrame(self):
        if self.currentThrusterFrame < 3:
            self.currentThrusterFrame = self.currentThrusterFrame + 1
        else:
            self.currentThrusterFrame = 0

class Bullet(Entity):
    def __init__(self, Name: str, SizeW, SizeH, posX, posY, owner: Ship, color: pygame.Color) -> None:
        super().__init__(Name, SizeW, SizeH)

        self.speed = 6

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.owner = owner

        self.flip = True

        self.missileColor = color

        self.missileSprites = pygame.image.load(script_dir + "/Resources/MissileSpinning-Sheet.png").convert_alpha()

        self.currentSpriteIndex = 0

        self.currentMissileFrame = 0

        self.CreatePyGameObject(True, posX, posY)

        self.currentMask = pygame.mask.from_surface(self.ReturnCurrentMissileSprite())

    def CreatePyGameObject(self, debug, posX: float, posY: float):
        super().CreatePyGameObject(debug, posX, posY)

    def ReturnCurrentMissileSprite(self):
        areaX = 50

        if self.currentMissileFrame != 0:
            areaX = areaX * self.currentMissileFrame

        surface = pygame.Surface((50, 50))

        surface.blit(self.missileSprites, (0, 0), (areaX, 0, 50, 50))

        if self.flip:
            surface = pygame.transform.rotate(surface, 90)

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