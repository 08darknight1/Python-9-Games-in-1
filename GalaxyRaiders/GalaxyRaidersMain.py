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

        self.enemiesList = []

        self.startedNewLevel = False

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.background = pygame.transform.scale(pygame.image.load(script_dir + "/Resources/spaceBackground.jpeg"),
                                                 (Width, Height))

        level_label = self.defaultFont.render(f"Level: {self.level}", True, (255, 255, 255))

        self.player = Entities.Ship("Player", 50, 50, (Width/2)-25, Height-50, 0, 10)

        self.drawer.AddObject("Background", "Static", None, self.background, 0, 0, 0)
        self.drawer.AddObject("Level Text", "Static", None, level_label, 0, 0, 1)

        playerObj = self.player.pyGameObject

        self.drawer.AddObject("Player Ship", "Dynamic", playerObj, self.player.ReturnShipSprite(), 0, 0, 2)
        self.drawer.AddObject("Player Ship Thruster", "Static", None, self.player.ReturnThrusterToDraw(), playerObj.x, playerObj.y + 40, 3)

        #self.SpawnNewEnemy()

        while self.running:
            self.PlayGame()

        pygame.quit()

    def PlayGame(self):
        self.clock.tick(self.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        self.LevelHandler()

        self.Animator()

        self.drawer.Draw()

        self.GetUserInput()

        self.MoveEnemies()

    def SpawnNewEnemy(self, posXforEnemy):
        posYforEnemy = (self.window.get_height()/2) * -1
        newEnemy = Entities.Ship("NewEnemy", 50, 50, posXforEnemy, posYforEnemy, 180, 5)
        self.enemiesList.append(newEnemy)
        lastItemIndex = len(self.enemiesList) - 1
        lastDrawObjectIndex = len(self.drawer.objectsList) - 1
        newPrioNumber = self.drawer.objectsList[lastDrawObjectIndex].prio + 1
        newPrioNumber2 = self.drawer.objectsList[lastDrawObjectIndex].prio + 2
        newEnemyNameIndex = str(len(self.enemiesList))
        self.drawer.AddObject("Enemy Ship" + newEnemyNameIndex, "Dynamic", self.enemiesList[lastItemIndex].pyGameObject, self.enemiesList[lastItemIndex].ReturnShipSprite(), 0, 0, newPrioNumber)
        self.drawer.AddObject("Enemy Ship Thruster" + newEnemyNameIndex, "Static", None, self.enemiesList[lastItemIndex].ReturnThrusterToDraw(), self.enemiesList[lastItemIndex].pyGameObject.x + 1, self.enemiesList[lastItemIndex].pyGameObject.y - 5, newPrioNumber2)

    def LevelHandler(self):
        if self.startedNewLevel == False:
            numberOfEnemies = random.randrange(0, 20)
            print("Number of enemies to spawn in level ", self.level, ": ", numberOfEnemies)
            for x in range(numberOfEnemies):
                posX = random.randrange(0, (self.window.get_width() - 50))
                self.SpawnNewEnemy(posX)

            self.startedNewLevel = True
        elif self.startedNewLevel == True:
            #print("Enemy List Size: ", len(self.enemiesList))
            if len(self.enemiesList) <= 0:
                self.level += 1
                self.startedNewLevel = False

    def MoveEnemies(self):
        enemyPrio: int
        enemyPosY : float
        for enemy in self.enemiesList:
            enemy.pyGameObject.y += enemy.speed
            for drawingObjects in self.drawer.objectsList:
                if drawingObjects.type == "Dynamic" and drawingObjects.PyObject == enemy.pyGameObject:
                    enemyPrio = drawingObjects.prio + 1
                    enemyPosY = drawingObjects.PyObject.y
                    break

            if enemyPrio is not None:
                thrusterName = self.drawer.objectsList[enemyPrio].name
                self.drawer.ChangeObject(thrusterName, 4, enemyPosY - 5)

    def Animator(self):
        self.animationTimer += self.clock.tick(60)

        if self.animationTimer >= self.animationTimerLimit :
            #Put changes in animator here
            self.player.SetNewThrusterFrame()
            self.drawer.ChangeObject("Player Ship Thruster", 2, self.player.ReturnThrusterToDraw())

            for enemy in self.enemiesList:
                enemy.SetNewThrusterFrame()
                enemyPrio : int
                for drawingObjects in self.drawer.objectsList:
                    if drawingObjects.type == "Dynamic" and drawingObjects.PyObject == enemy.pyGameObject:
                        enemyPrio = drawingObjects.prio + 1
                        break

                if enemyPrio is not None:
                    thrusterName = self.drawer.objectsList[enemyPrio].name
                    self.drawer.ChangeObject(thrusterName, 2, enemy.ReturnThrusterToDraw())
                    break


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










