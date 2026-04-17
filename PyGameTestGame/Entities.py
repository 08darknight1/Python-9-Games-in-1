import pygame

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

        self.CreatePyGameObject(debug, self.posX, self.posY)

class Player(Entity):
    def __init__(self, name, width, height, speed, posX, posY, debug):
        super().__init__(name, width, height, speed, posX, posY)

        self.debug = debug

        self.dead = False

        self.playerSprites = []

        self.playerSprites.append(pygame.image.load("PyGameTestGame/Resources/Ship.png"))
        self.playerSprites.append(pygame.image.load("PyGameTestGame/Resources/Ship Turning.png"))

        self.CreatePyGameObject(debug, self.posX, self.posY)

    def CreatePyGameObject(self, debugRect: bool, posX: float, posY: float):
        self.pyGameObject = pygame.Rect(posX, posY, self.width, self.height)

        if not debugRect:
            self.currentSprite = self.playerSprites[0]
            self.SetNewPlayerSprite(0,0)

    def SetNewPlayerSprite(self, index : int, direction: int):
        self.currentSprite = self.playerSprites[index]
        self.spriteDirection = direction