import random
import time
import pygame
import os
from GalaxyRun import Entities

class RunGame:
    def __init__(self, Width: int, Height: int, playerH: int, playerW: int, meteorsPerCycle) -> None:
        pygame.font.init()

        self.font = pygame.font.SysFont("Arial", 20)

        self.gameOverFont = pygame.font.SysFont("Arial", 80)

        self.window = pygame.display.set_mode((Width, Height))

        pygame.display.set_caption("Galaxy Run")

        self.running = True

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.background = pygame.transform.scale(pygame.image.load(script_dir + "/Resources/spaceBackground.jpeg"), (Width, Height))

        self.player = Entities.Player("Ship", playerW, playerH, 10, (Width-playerW)/2, Height-playerH, False)

        self.clock = pygame.time.Clock()

        self.startTime = time.time()

        self.elapsedTime = 0

        self.meteorIncrement = 2000

        self.meteorCount = 0

        self.meteors = []

        self.meteorsToSpawn = meteorsPerCycle

        self.animationTimerLimit = 30

        self.animationTimer = 0

        while self.running:
            self.PlayGame()

        pygame.quit()

    def PlayGame(self):
        self.meteorCount += self.clock.tick(60)

        self.elapsedTime = time.time() - self.startTime

        if self.meteorCount > self.meteorIncrement:
            for x in range(self.meteorsToSpawn):
                meteorWidth = self.player.width/2
                meteorHeight = self.player.height/2
                posX = random.randrange(0, self.window.get_width())
                meteorName = "Meteor " + str(x)
                newMeteor = Entities.Meteor(meteorName, meteorWidth, meteorHeight, 2, posX, ((meteorHeight*2) * -1), False)

                self.meteors.append(newMeteor)

            self.meteorIncrement = max(200, self.meteorIncrement - 50)

            # Fazendo uma operação no meteor increment, analisando se o valor dele é maior do que o primeiro citando no parenteses, e caso não fazendo a operação seguinte

            self.meteorCount = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        self.GetUserInput(self.player)

        for meteor in self.meteors[:]: #esses 2 pontos no meio dos colchetes e para fazer as operações do FOR em uma copia pra só depois iterar na lista original e não gerar problemas
            meteorObj = meteor.ReturnPyGameObject()
            playerObj = self.player.ReturnPyGameObject()

            meteorObj.y = meteorObj.y + meteor.speed

            if meteorObj.y > self.window.get_height() + meteorObj.height:
                self.meteors.remove(meteor)
            elif meteor.currentMask.overlap(self.player.currentMask, (playerObj.x - meteorObj.x, playerObj.y - meteorObj.y)):
                self.meteors.remove(meteor)
                self.player.dead = True
                break

        self.DrawGame()

        self.CheckForGameOver(self.player)

        self.AnimationCheck()

    def DrawGame(self):
        self.window.blit(self.background, (0, 0))

        timeText = self.font.render(f"Time: {round(self.elapsedTime)}", 1, "white")

        self.window.blit(timeText, (10, 10))

        if self.player.debug:
            pygame.draw.rect(self.window, "red", self.player.ReturnPyGameObject())
        else:
            playerObj = self.player.ReturnPyGameObject()
            thrusterPosY = playerObj.y + self.player.height/1.25
            self.window.blit(self.player.DrawThruster(), (playerObj.x, thrusterPosY))
            self.window.blit(self.player.currentSprite, (playerObj.x, playerObj.y))

        for x in range(len(self.meteors)):
            meteorObj = self.meteors[x].ReturnPyGameObject()

            if self.meteors[x].debug:
                pygame.draw.rect(self.window, (0, 255, 0), meteorObj)
            else:
                self.window.blit(self.meteors[x].DrawCurrentSprite(), (meteorObj.x, meteorObj.y))

        pygame.display.update()

    def AnimationCheck(self):
        self.animationTimer += self.clock.tick(60)

        if self.animationTimer >= self.animationTimerLimit :
            self.player.SetNewThrusterFrame()

            for x in range(0, len(self.meteors)):
                self.meteors[x].SetNextFrame()

            self.animationTimer = 0

    def GetUserInput(self, player):
        self.userInput = pygame.key.get_pressed()

        if self.userInput[pygame.K_LEFT] and player.ReturnPyGameObject().x >= 0:
            player.ReturnPyGameObject().x = player.ReturnPyGameObject().x - player.speed
            player.SetNewPlayerSprite(1, False)
        elif self.userInput[pygame.K_RIGHT] and player.ReturnPyGameObject().x <= self.window.get_width() - player.width:
            player.ReturnPyGameObject().x = player.ReturnPyGameObject().x + player.speed
            player.SetNewPlayerSprite(1, True)
        else:
            player.SetNewPlayerSprite(0, False)

    def CheckForGameOver(self, player: Entities.Player):
        if player.dead:
            lostText= self.gameOverFont.render("You lost!", 1, "White")

            textWidth = self.window.get_width()/2 - lostText.get_width()/2
            textHeight = self.window.get_height()/2 - lostText.get_height()/2

            self.window.blit(lostText, (textWidth, textHeight))

            pygame.display.update()
            pygame.time.wait(4000)
            
            self.running = False