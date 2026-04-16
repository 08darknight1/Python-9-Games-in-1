import random
import time
import pygame
from PyGameTestGame import Entities
pygame.font.init()

class RunGame:

    def __init__(self, Width: int, Height: int, playerH: int, playerW: int, starsNumberPerCycle) -> None:
        self.font = pygame.font.SysFont("Arial", 20)

        self.window = pygame.display.set_mode((Width, Height))

        pygame.display.set_caption("Dog Fight!")

        self.running = True

        self.background = pygame.transform.scale(pygame.image.load("PyGameTestGame/Resources/spaceBackground.jpeg"), (Width, Height))

        self.player = Entities.Player("Ship", playerW, playerH, 10, (Width-playerW)/2, Height-playerH, True)

        self.clock = pygame.time.Clock()

        self.startTime = time.time()

        self.elapsedTime = 0

        self.meteorIncrement = 2000

        self.meteorCount = 0

        self.meteors = []

        self.starsToSpawn = starsNumberPerCycle

        while self.running:
            self.PlayGame()

        pygame.quit()

    def PlayGame(self):
        self.meteorCount += self.clock.tick(60)
        self.elapsedTime = time.time() - self.startTime

        if self.meteorCount > self.meteorIncrement:
            for x in range(self.starsToSpawn):
                #mt fodido isso mds
                meteorWidth = self.player.width/2

                print("Defined meteor Width as: ", meteorWidth)

                meteorHeight = self.player.height/2

                print("Defined meteor Height as: ", meteorHeight)

                posX = random.randrange(0, self.window.get_width())

                print("Defined meteor PosX as: ", posX)

                meteorName = "Meteor " + str(x)

                newStar = Entities.Meteor(meteorName, meteorWidth, meteorHeight, 2, posX, (meteorHeight * -1), True)

                self.meteors.append(newStar)

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

            meteorObj.y = meteorObj.y + meteor.speed

            if meteorObj.y > self.window.get_height() + meteorObj.height:
                self.meteors.remove(meteor)
            elif meteorObj.y + meteorObj.height >= self.player.ReturnPyGameObject().y and meteorObj.colliderect(self.player.ReturnPyGameObject()):
                self.meteors.remove(meteor)
                #Implement something about the player being hit here!
                break

        self.DrawGame()

    def DrawGame(self):
        self.window.blit(self.background, (0, 0))

        timeText = self.font.render(f"Time: {round(self.elapsedTime)}", 1, "white")

        self.window.blit(timeText, (10, 10))

        if self.player.debug:
            pygame.draw.rect(self.window, "red", self.player.ReturnPyGameObject())

        for x in range(len(self.meteors)):
            meteorObj = self.meteors[x].ReturnPyGameObject()
            pygame.draw.rect(self.window, (0, 255, 0), meteorObj)
            print("Hi my name is", self.meteors[x].name, " | My current Position is: [", meteorObj.x,"][", meteorObj.y,"]")

        pygame.display.update()

    def GetUserInput(self, player):
        self.userInput = pygame.key.get_pressed()

        if self.userInput[pygame.K_LEFT] and player.ReturnPyGameObject().x >= 0:
            player.ReturnPyGameObject().x = player.ReturnPyGameObject().x - player.speed

        if self.userInput[pygame.K_RIGHT] and player.ReturnPyGameObject().x <= self.window.get_width() - player.width:
            player.ReturnPyGameObject().x = player.ReturnPyGameObject().x + player.speed