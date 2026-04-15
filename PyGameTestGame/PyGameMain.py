from turtledemo import clock

import pygame

from PyGameTestGame import Entities

class RunGame:

    def __init__(self, Width: int, Height: int):
        self.window = pygame.display.set_mode((Width, Height))
        pygame.display.set_caption("Dog Fight!")
        self.running = True
        self.background = pygame.transform.scale(pygame.image.load("PyGameTestGame/Resources/spaceBackground.jpeg"), (Width, Height))

        self.player = Entities.Player("Ship", 50, 50, 10, True)

        self.clock = pygame.time.Clock()

        while self.running:
            self.PlayGame()

        pygame.quit()

    def PlayGame(self):
        self.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        self.GetUserInput(self.player)

        self.DrawGame(self.player)

    def DrawGame(self, player):
        self.window.blit(self.background, (0, 0))

        if player.debug:
            pygame.draw.rect(self.window, "red", player.ReturnPlayerObject())

        pygame.display.update()

    def GetUserInput(self, player):
        self.userInput = pygame.key.get_pressed()

        if self.userInput[pygame.K_LEFT]:
            player.ReturnPlayerObject().x = player.ReturnPlayerObject().x - player.speed

        if self.userInput[pygame.K_RIGHT]:
            player.ReturnPlayerObject().x = player.ReturnPlayerObject().x + player.speed