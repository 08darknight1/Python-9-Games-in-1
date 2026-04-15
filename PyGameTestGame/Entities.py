import pygame

class Entity:
    def __init__(self, name):
        self.name = name

class Player(Entity):
    def __init__(self, name, width, height, speed, debug):
        super().__init__(name)
        self.width = width
        self.height = height
        self.debug = debug
        self.speed = speed

        self.CreatePyGamePlayer(debug)

    def CreatePyGamePlayer(self, debugRect: bool):
        if debugRect:
            self.playerObject = pygame.Rect(0, 0, self.width, self.height)
        else:
            print("Waiting for code implementation of definitive player!")

    def ReturnPlayerObject(self):
        return self.playerObject