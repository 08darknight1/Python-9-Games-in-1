import time
import pygame
import os
from DogFight import Entities

class RunGame:

    def __init__(self, Width: int, Height: int) -> None:
        pygame.font.init()

        self.font = pygame.font.SysFont("Arial", 20)

        self.gameOverFont = pygame.font.SysFont("Arial", 50)

        self.biggerGameOverFont = pygame.font.SysFont("Arial", 51)

        self.window = pygame.display.set_mode((Width, Height))

        pygame.display.set_caption("Dog Fight")

        self.running = True

        self.gameOver = False

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.background = pygame.transform.scale(pygame.image.load(script_dir + "/Resources/spaceBackground.jpeg"),
                                                 (Width, Height))

        self.clock = pygame.time.Clock()

        self.startTime = time.time()

        self.animationTimerLimit = 30

        self.animationTimer = 0

        self.borderSize = 10

        self.bulletList = []

        self.reloadP1Timer = 0

        self.reloadP1TimerStart = 0

        self.reloadP1Started = False

        self.reloadP2Timer = 0

        self.reloadP2TimerStart = 0

        self.reloadP2Started = False

        self.Player1 = Entities.SpaceShip("P1", 50, 50, 0, (Height/2)-25, 10, True, -90)

        self.Player2 = Entities.SpaceShip("P2", 50, 50, Width-50, (Height/2)-25, 10, True, 90)

        while self.running:
            self.PlayGame()

        pygame.quit()

    def PlayGame(self):
        self.clock.tick(60)

        self.elapsedTime = time.time() - self.startTime

        self.GetUserInput()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.Player1.ammo > 0:
                    p1_Obj = self.Player1.ReturnPyGameObject()
                    newBullet = Entities.Bullet("BulletP1", 50, 50, 10, p1_Obj.x, p1_Obj.y, False, self.Player1, self.Player1.Color)
                    self.bulletList.append(newBullet)
                    self.Player1.ammo -= 1


                if event.key == pygame.K_RETURN and self.Player2.ammo > 0:
                    p2_Obj = self.Player2.ReturnPyGameObject()
                    newBullet = Entities.Bullet("BulletP2", 50, 50, 10, p2_Obj.x, p2_Obj.y, True, self.Player2,
                                                self.Player2.Color)
                    self.bulletList.append(newBullet)
                    self.Player2.ammo -= 1

        for bullet in self.bulletList[:]:
            bulletObj = bullet.ReturnPyGameObject()
            p1_Obj = self.Player1.ReturnPyGameObject()
            p2_Obj = self.Player2.ReturnPyGameObject()

            if bullet.owner == self.Player1:
                bulletObj.x = bulletObj.x + bullet.speed
                if bullet.currentMask.overlap(self.Player2.currentMask, (p2_Obj.x - bulletObj.x, p2_Obj.y - bulletObj.y)):
                    self.bulletList.remove(bullet)
                    self.Player2.life -= 1

                    if self.Player2.life <= 0:
                        self.gameOver = True
            else:
                bulletObj.x = bulletObj.x - bullet.speed
                if bullet.currentMask.overlap(self.Player1.currentMask, (p1_Obj.x - bulletObj.x, p1_Obj.y - bulletObj.y)):
                    self.bulletList.remove(bullet)
                    self.Player1.life -= 1

                    if self.Player1.life <= 0:
                        self.gameOver = True

            if bulletObj.x < bullet.width * -1 or bulletObj.x > self.window.get_width() + bullet.width:
                self.bulletList.remove(bullet)

        #print("Bullet list size: ", + len(self.bulletList))

        self.AddAmmo()

        self.AnimationCheck()

        self.DrawGame()

        self.GameOverCheck()

    def DrawGame(self):
        #Draw Background
        self.window.blit(self.background, (0, 0))

        ''' Colored background to test sprites
        newColor = pygame.Color(100, 10, 10)
        self.window.fill(newColor)'''

        #Draw Players Bullets
        for bullet in self.bulletList[:]:
            bulletSprite = bullet.ReturnCurrentMissileSprite()
            bulletObj = bullet.ReturnPyGameObject()
            self.window.blit(bulletSprite, (bulletObj.x, bulletObj.y))

        #Draw Players
        p1_Obj = self.Player1.ReturnPyGameObject()
        p2_Obj = self.Player2.ReturnPyGameObject()

        self.window.blit(self.Player1.ReturnShipSprite(), (p1_Obj.x, p1_Obj.y))
        self.window.blit(self.Player2.ReturnShipSprite(), (p2_Obj.x, p2_Obj.y))

        #Draw Ships Thrusters
        P1thrusterPosX = p1_Obj.x - 5
        self.window.blit(self.Player1.ReturnThrusterToDraw(0), (P1thrusterPosX, p1_Obj.y))

        P2thrusterPosX = p2_Obj.x + (self.Player2.width/1.25)
        self.window.blit(self.Player2.ReturnThrusterToDraw(1), (P2thrusterPosX, p2_Obj.y))

        #everything needs to be above this line
        pygame.display.update()

    def AnimationCheck(self):
        self.animationTimer += self.clock.tick(60)

        if self.animationTimer >= self.animationTimerLimit :
            #Put changes in animator here
            self.Player1.SetNewThrusterFrame()

            self.Player2.SetNewThrusterFrame()

            for bullet in self.bulletList[:]:
                bullet.SetNewMissileFrame()

            self.animationTimer = 0

    def AddAmmo(self):
        if self.Player1.ammo < self.Player1.ammoMax:
            if not self.reloadP1Started:
                self.reloadP1TimerStart = time.time()
                self.reloadP1Started = True

            self.reloadP1Timer = time.time() - self.reloadP1TimerStart

            if self.reloadP1Timer >= self.Player1.reloadTimerMax:
                self.Player1.ammo += 1
                self.reloadP1Started = False

        if self.Player2.ammo < self.Player2.ammoMax:
            if not self.reloadP2Started:
                self.reloadP2TimerStart = time.time()
                self.reloadP2Started = True

            self.reloadP2Timer = time.time() - self.reloadP2TimerStart

            if self.reloadP2Timer >= self.Player2.reloadTimerMax:
                self.Player2.ammo += 1
                self.reloadP2Started = False

    def GameOverCheck(self):
        if self.gameOver:
            lostText= self.gameOverFont.render("PLAYER 1 WON!", 1, "Black")
            lostTextBackground = self.biggerGameOverFont.render("PLAYER 1 WON!", 1, self.Player1.Color)

            if self.Player1.life <= 0:
                lostText= self.gameOverFont.render("PLAYER 2 WON!", 1, "Black")
                lostTextBackground = self.biggerGameOverFont.render("PLAYER 2 WON!", 1, self.Player2.Color)

            textWidth = self.window.get_width() / 2 - lostText.get_width() / 2
            textHeight = self.window.get_height() / 2 - lostText.get_height() / 2

            self.window.blit(lostTextBackground, (textWidth-3.5, textHeight+1.80))
            self.window.blit(lostText, (textWidth, textHeight))

            pygame.display.update()
            pygame.time.wait(4000)

            self.running = False

    def GetUserInput(self):
        userInput = pygame.key.get_pressed()

        p1_Obj = self.Player1.ReturnPyGameObject()
        p2_Obj = self.Player2.ReturnPyGameObject()

        #Player 1 input Y moving
        if userInput[pygame.K_w] and p1_Obj.y >= 0:
            p1_Obj.y = p1_Obj.y - self.Player1.speed
            self.Player1.ChangeShipMainSprite(True, False)
        elif userInput[pygame.K_s] and p1_Obj.y <= self.window.get_height() - self.Player1.height:
            p1_Obj.y = p1_Obj.y + self.Player1.speed
            self.Player1.ChangeShipMainSprite(True, True)
        else:
            self.Player1.ChangeShipMainSprite(False, False)

        #Player 1 input X moving
        if userInput[pygame.K_a] and p1_Obj.x >= 0:
            p1_Obj.x = p1_Obj.x - self.Player1.speed
        elif userInput[pygame.K_d] and p1_Obj.x <= (self.window.get_width()/2) - self.Player1.width - self.borderSize:
            p1_Obj.x = p1_Obj.x + self.Player1.speed

        #Player 2 input Y moving
        if userInput[pygame.K_UP] and p2_Obj.y >= 0:
            p2_Obj.y = p2_Obj.y - self.Player2.speed
            self.Player2.ChangeShipMainSprite(True, True)
        elif userInput[pygame.K_DOWN] and p2_Obj.y <= self.window.get_height() - self.Player2.height:
            p2_Obj.y = p2_Obj.y + self.Player2.speed
            self.Player2.ChangeShipMainSprite(True, False)
        else:
            self.Player2.ChangeShipMainSprite(False, False)

        #Player 2 input X moving
        if userInput[pygame.K_LEFT] and p2_Obj.x >= self.window.get_width()/2 + self.borderSize:
            p2_Obj.x = p2_Obj.x - self.Player2.speed
        elif userInput[pygame.K_RIGHT] and p2_Obj.x <= self.window.get_width() - self.Player2.width:
            p2_Obj.x = p2_Obj.x + self.Player2.speed


