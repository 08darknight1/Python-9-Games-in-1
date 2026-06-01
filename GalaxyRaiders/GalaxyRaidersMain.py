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

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.background = pygame.transform.scale(pygame.image.load(script_dir + "/Resources/spaceBackground.jpeg"),
                                                 (Width, Height))

        level_label = self.defaultFont.render(f"Level: {self.level}", True, (255, 255, 255))

        self.player = Entities.Ship("Player", 50, 50, (Width/2)-25, Height-50, 0, 10)

        self.drawer.AddObject(self.background, None, 0)
        self.drawer.AddObject(level_label, None, 1)
        self.drawer.AddObject(self.player.ReturnShipSprite(), self.player.pyGameObject, 2)

        while self.running:
            self.PlayGame()

        pygame.quit()

    def PlayGame(self):
        self.clock.tick(self.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        self.drawer.Draw()

        self.GetUserInput()

    def GetUserInput(self):
        userInput = pygame.key.get_pressed()

        p1_Obj = self.player.pyGameObject

        #Player 1 input Y moving
        if userInput[pygame.K_a] and p1_Obj.x > 0:
            p1_Obj.x = p1_Obj.x - self.player.speed
            #self.player.ChangeShipMainSprite(True, False)
        elif userInput[pygame.K_d] and p1_Obj.x < self.window.get_width() - self.player.SizeW:
            p1_Obj.x = p1_Obj.x + self.player.speed
            #self.player.ChangeShipMainSprite(True, True)
        #else:
            #self.player.ChangeShipMainSprite(False, False)










