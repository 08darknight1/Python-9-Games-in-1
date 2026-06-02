import pygame
import os
import time
import random

from GalaxyRaiders import Entities
from GalaxyRaiders import GameDrawer


class RunGame:
    def __init__(self, Width: int, Height: int) -> None:
        pygame.font.init()

        self.defaultFont = pygame.font.SysFont("Arial", 20)

        self.window = pygame.display.set_mode((Width, Height))

        self.level = 1

        self.drawer = GameDrawer.Drawer(self.window)

        pygame.display.set_caption("Galaxy Raiders")

        self.running = True

        self.gameOver = False

        self.FPS = 60

        self.clock = pygame.time.Clock()

        self.animationTimerLimit = 30

        self.animationTimer = 0

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.background = pygame.transform.scale(pygame.image.load(script_dir + "/Resources/spaceBackground.jpeg"),
                                                 (Width, Height))

        level_label = self.defaultFont.render(f"Level: {self.level}", True, (255, 255, 255))

        self.player = Entities.Ship("Player", 50, 50, (Width/2)-25, Height-50, 0, 10)

        self.drawer.AddObject("Background", "Static", None, self.background, 0, 0, 0)
        self.drawer.AddObject("Level Text", "Static", None, level_label, 0, 0, 1)

        playerObj = self.player.pyGameObject

        self.drawer.AddObject("Player Ship", "Dynamic", playerObj, self.player.ReturnShipSprite(), playerObj.x, playerObj.y, 2)
        self.drawer.AddObject("Player Ship Thruster", "Static", None, self.player.ReturnThrusterToDraw(), playerObj.x, playerObj.y + 40, 3)

        while self.running:
            self.PlayGame()

        pygame.quit()

    def PlayGame(self):
        self.clock.tick(self.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        self.Animator()

        self.drawer.Draw()

        self.GetUserInput()

    def Animator(self):
        self.animationTimer += self.clock.tick(60)

        if self.animationTimer >= self.animationTimerLimit :
            #Put changes in animator here
            self.player.SetNewThrusterFrame()
            self.drawer.ChangeObject("Player Ship Thruster", 2, self.player.ReturnThrusterToDraw())

            self.animationTimer = 0

    def GetUserInput(self):
        userInput = pygame.key.get_pressed()

        p1_Obj = self.player.pyGameObject

        #Player 1 input Y moving
        if userInput[pygame.K_a] and p1_Obj.x > 0:
            p1_Obj.x -= self.player.speed
            self.player.ChangeShipMainSprite(True, False)
        elif userInput[pygame.K_d] and p1_Obj.x < self.window.get_width() - self.player.SizeW:
            p1_Obj.x += self.player.speed
            self.player.ChangeShipMainSprite(True, True)
        else:
            self.player.ChangeShipMainSprite(False, False)

        if userInput[pygame.K_w] and p1_Obj.y > 0:
            p1_Obj.y -= self.player.speed
        elif userInput[pygame.K_s] and p1_Obj.y < self.window.get_height() - self.player.SizeH:
            p1_Obj.y += self.player.speed

        self.drawer.ChangeObject("Player Ship", 2, self.player.ReturnShipSprite())
        self.drawer.ChangeObject("Player Ship Thruster", 3, self.player.pyGameObject.x)
        self.drawer.ChangeObject("Player Ship Thruster", 4, self.player.pyGameObject.y + 40)










