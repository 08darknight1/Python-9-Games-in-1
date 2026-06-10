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

        self.bullets = []

        self.reloadTimer = 0

        self.reloadStarted = False

        self.reloadTimerStart = 0

        self.canShoot = True

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.background = pygame.transform.scale(pygame.image.load(script_dir + "/Resources/spaceBackground.jpeg"),
                                                 (Width, Height))

        self.level_label = self.defaultFont.render(f"Level: {self.level}", True, (255, 255, 255))

        self.player = Entities.Ship("Player", 50, 50, (Width/2)-25, Height-50, 0, 10)

        self.bullet_label = self.defaultFont.render(f"Bullets: {self.player.ammo}", True, (255, 255, 255))

        self.drawer.AddObject("Background", "Static", None, self.background, 0, 0, 0)
        self.drawer.AddObject("Level Text", "Static", None, self.level_label, 0, 0, 1)
        self.drawer.AddObject("Bullet Text", "Static", None, self.bullet_label,0, 75, 2)

        playerObj = self.player.pyGameObject

        self.drawer.AddObject("Player Ship", "Dynamic", playerObj, self.player.ReturnShipSprite(), 0, 0, 3)
        self.drawer.AddObject("Player Ship Thruster", "Static", None, self.player.ReturnThrusterToDraw(), playerObj.x, playerObj.y + 40, 4)

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

        self.LevelHandler(2)

        self.Animator()

        self.drawer.Draw()

        self.GetUserInput()

        self.MoveEnemies()

        self.MoveBullets()

        self.ReloadBullets()

    def ReloadBullets(self):
        if self.player.ammo < self.player.ammoMax:
            if self.reloadStarted == False:
                self.reloadTimerStart = time.time()
                self.reloadStarted = True

            self.reloadTimer = time.time() - self.reloadTimerStart

            if self.reloadTimer >= self.player.reloadTimerMax:
                self.player.ammo += 1
                self.reloadStarted = False

                self.bullet_label = self.defaultFont.render(f"Bullets: {self.player.ammo}", True, (255, 255, 255))
                self.drawer.ChangeObject("Bullet Text", 2, self.bullet_label)


    def SpawnNewEnemy(self, posXforEnemy):
        newEnemyNameIndex = str(len(self.enemiesList))

        posYforEnemy = (self.window.get_height()/2) * -1
        newEnemy = Entities.Ship("Enemy Ship" + newEnemyNameIndex, 50, 50, posXforEnemy, posYforEnemy, 180, 5)
        self.enemiesList.append(newEnemy)
        lastItemIndex = len(self.enemiesList) - 1

        self.drawer.AddObject("Enemy Ship" + newEnemyNameIndex, "Dynamic", self.enemiesList[lastItemIndex].pyGameObject, self.enemiesList[lastItemIndex].ReturnShipSprite(), 0, 0, -1)
        self.drawer.AddObject("Enemy Ship Thruster" + newEnemyNameIndex, "Static", None, self.enemiesList[lastItemIndex].ReturnThrusterToDraw(), self.enemiesList[lastItemIndex].pyGameObject.x + 1, self.enemiesList[lastItemIndex].pyGameObject.y - 5, -1)

    def LevelHandler(self, enemies):
        if enemies == None:
            enemies = random.randrange(0, 20)
        if self.startedNewLevel == False:
            print("Number of enemies to spawn in level ", self.level, ": ", enemies)
            for x in range(enemies):
                posX = random.randrange(0, (self.window.get_width() - 50))
                self.SpawnNewEnemy(posX)

            self.startedNewLevel = True
        elif self.startedNewLevel == True:
            if len(self.enemiesList) <= 0:
                self.level += 1
                self.startedNewLevel = False
                self.level_label = self.defaultFont.render(f"Level: {self.level}", True, (255, 255, 255))
                self.drawer.ChangeObject("Level Text", 2, self.level_label)

    def MoveBullets(self):
        for bullet in self.bullets[:]:
            if bullet.owner == self.player:
                bullet.pyGameObject.y -= bullet.speed

                for x in range(len(self.drawer.objectsList)):
                    if self.drawer.objectsList[x].type == "Dynamic" and self.drawer.objectsList[x].name == bullet.Name:
                        self.drawer.ChangeObject(bullet.Name, 4, bullet.pyGameObject.y)

                if bullet.pyGameObject.y == bullet.pyGameObject.height * -1:
                    self.drawer.RemoveObject(bullet.Name)
                    self.bullets.remove(bullet)

                for enemy in self.enemiesList:
                    bulletObj = bullet.pyGameObject
                    enemyObj = enemy.pyGameObject
                    if bullet.currentMask.overlap(enemy.currentMask, (enemyObj.x - bulletObj.x, enemyObj.y - bulletObj.y)):
                        for x in range(len(self.drawer.objectsList)):
                            if self.drawer.objectsList[x].type == "Dynamic" and self.drawer.objectsList[x].name == enemy.Name:
                                thursterName = self.drawer.objectsList[x + 1].name
                                self.drawer.RemoveObject(thursterName)
                                break

                        self.drawer.RemoveObject(bullet.Name)

                        self.bullets.remove(bullet)

                        self.drawer.RemoveObject(enemy.Name)

                        self.enemiesList.remove(enemy)

                        break

    def MoveEnemies(self):
        for enemy in self.enemiesList:
            enemy.pyGameObject.y += enemy.speed
            for x in range(len(self.drawer.objectsList)):
                obj = self.drawer.objectsList[x]
                if obj.type == "Dynamic" and obj.PyObject == enemy.pyGameObject:
                    thrusterName = self.drawer.objectsList[x + 1].name
                    self.drawer.ChangeObject(thrusterName, 4, enemy.pyGameObject.y - 5)
                    break

            if enemy.pyGameObject.y > (self.window.get_height() + enemy.pyGameObject.height):
                enemy.pyGameObject.y = (self.window.get_height()/2) * -1

    def Animator(self):
        self.animationTimer += self.clock.tick(60)

        if self.animationTimer >= self.animationTimerLimit :
            #Put changes in animator here
            self.player.SetNewThrusterFrame()
            self.drawer.ChangeObject("Player Ship Thruster", 2, self.player.ReturnThrusterToDraw())

            for enemy in self.enemiesList:
                enemy.SetNewThrusterFrame()

                enemyPrio : int

                for x in range(len(self.drawer.objectsList)):
                    obj = self.drawer.objectsList[x]
                    if obj.type == "Dynamic" and obj.name == enemy.Name:
                        thrusterName = self.drawer.objectsList[x + 1].name
                        self.drawer.ChangeObject(thrusterName, 2, enemy.ReturnThrusterToDraw())
                        break

            for bullet in self.bullets[:]:
                bullet.SetNewMissileFrame()
                self.drawer.ChangeObject(bullet.Name, 2, bullet.ReturnCurrentMissileSprite())

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

        if self.canShoot == True and userInput[pygame.K_SPACE] and self.player.ammo > 0:
            p1_Obj = self.player.pyGameObject
            self.player.ammo = self.player.ammo - 1
            bulletNumber = str((self.player.ammo - self.player.ammoMax) + 1)
            newBullet = Entities.Bullet("Bullet" + bulletNumber, 50, 50, p1_Obj.x, p1_Obj.y - 15, self.player,
                                        self.player.Color)
            self.drawer.AddObject("Bullet" + bulletNumber, "Dynamic", newBullet.pyGameObject,
                                  newBullet.ReturnCurrentMissileSprite(), None, None, -1)

            self.bullets.append(newBullet)

            self.bullet_label = self.defaultFont.render(f"Bullets: {self.player.ammo}", True, (255, 255, 255))
            self.drawer.ChangeObject("Bullet Text", 2, self.bullet_label)

            self.canShoot = False
        elif self.canShoot == False and not userInput[pygame.K_SPACE]:
            self.canShoot = True






