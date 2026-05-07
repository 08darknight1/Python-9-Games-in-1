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
        Entity.__init__(self, name, width, height, speed)

        self.rotation = rotation

        self.playerSprites = []

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship.png").convert_alpha())
        self.playerSprites.append(pygame.image.load(script_dir + "/Resources/Ship Turning.png").convert_alpha())

        self.thrusterSprites = pygame.image.load(script_dir + "/Resources/ShipThruster-Sheet.png").convert_alpha()

        self.currentThrusterFrame = 0

        self.currentSprite = self.playerSprites[0]

        self.CreatePyGameObject(debug, posX, posY)

        value1 = random.randrange(0, 256)

        value2 = random.randrange(0, 256)

        value3 = random.randrange(0, 256)

        self.Color = pygame.Color(value1, value2, value3)

    def CreatePyGameObject(self, debug, posX: float, posY: float):
        super().CreatePyGameObject(debug, posX, posY)

    def ReturnShipSprite(self):
        imgToReturn = pygame.transform.rotate(self.currentSprite, self.rotation)

        coloredImage = pygame.Surface(imgToReturn.get_size()).convert_alpha()

        coloredImage.fill(self.Color)

        imgToReturn.blit(coloredImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        return imgToReturn

