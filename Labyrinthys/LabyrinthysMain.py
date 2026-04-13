import random

from Labyrinthys import GameGrid, Entities

#gameRunning = True

scene = 0

class RunGame:
    def __init__(self):
        self.gameRunning = True
        self.scene = 0

        while self.gameRunning:
            self.PlayGame()

    def GameMenu(self):
        print("\nL A B Y R I N T H Y S")
        print("\n1- Play Random Map/Configs")
        print("2- Play Personalized Map")
        print("3- Instructions")
        print("4- Quit")
        self.scene = int(input("//-: "))

    def PlayGame(self):
        if self.scene == 0:
            self.GameMenu()
        if self.scene == 1:
            self.LoadRandomMap()
        if self.scene == 2:
            self.LoadSpecificMap()
        if self.scene == 3:
            print("Imagine me printing all the games info here for now!")
        if self.scene == 4:
            self.gameRunning = False

    def LoadRandomMap(self):
        gridSize = random.randrange(12, 21)
        enemiesCount = int(gridSize / 2)
        newGrid = GameGrid.Grid(5, 5)
        newPlayer = Entities.Player(0, 0)
        newGrid.RegisterPlayer(newPlayer)
        newGrid.DefinePlayerObjective(-1, -1, newPlayer)
        newGrid.RegisterEnemies(True, True, enemiesCount)
        newGrid.PrintCurrentGameGrid(False)

        self.NextMoves(newGrid, newPlayer)

    def LoadSpecificMap(self):
        gridSizeX = int(input("\nPlease input the number of rows for the map: "))
        gridSizeY = int(input("Please input the number of columns for the map: "))

        newGrid = GameGrid.Grid(gridSizeX, gridSizeY)

        print("Do you want to input player starting position? ")
        print("0 - Yes")
        print("1 - No")
        answer = int(input("//-: "))

        playerPosX = 0
        playerPosY = 0

        if answer == 0:
            print("Please input player position on the rows(Max number: ", gridSizeX - 1 ,")")
            playerPosX = int(input("//-:"))

            print("Please input player position on the columns(Max number: ", gridSizeY - 1 ,")")
            playerPosY = int(input("//-:"))

        newPlayer = Entities.Player(playerPosX, playerPosY)

        newGrid.RegisterPlayer(newPlayer)

        while True:
            print("Do you want to input player objective position? ")
            print("0 - Yes")
            print("1 - No")
            answer = int(input("//-: "))

            playerObjectiveX = -1
            playerObjectiveY = -1

            if answer == 0:
                print("Please input player final objective on the rows(Max number: ", gridSizeX - 1, ")")
                playerObjectiveX = int(input("//-:"))

                print("Please input player final objective on the columns(Max number: ", gridSizeY - 1 ,")")
                playerObjectiveY = int(input("//-:"))

            if(playerPosX != playerObjectiveX and playerPosY != playerObjectiveY):
                newGrid.DefinePlayerObjective(playerObjectiveX, playerObjectiveY, newPlayer)
                break

        print("Do you want to include enemies? ")
        print("0- Yes")
        print("1- No")
        answer = int(input("//-: "))

        includeEnemies = False
        randomNumber = False
        enemiesCount = 0

        if answer == 0:
            includeEnemies = True

        if includeEnemies:
            print("Randomize number? ")
            print("0- Yes")
            print("1- No")
            answer = int(input("//-: "))

            if answer == 0:
                randomNumber = True
                enemiesCount = int((gridSizeX * gridSizeY)/2)

            if not randomNumber:
                while True:
                    maxNumberOfEnemies = (gridSizeX * gridSizeY) - 2
                    print("Please input the number of enemies(Max number: ", maxNumberOfEnemies ,")")
                    enemiesCount = int(input("//-: "))

                    if enemiesCount <= maxNumberOfEnemies:
                        break

        newGrid.RegisterEnemies(includeEnemies, randomNumber, enemiesCount)
        newGrid.PrintCurrentGameGrid(False)

        self.NextMoves(newGrid, newPlayer)


    def NextMoves(self, newGrid: GameGrid.Grid, newPlayer: Entities.Player):
        while True:
            # get input from player
            print("\n\n4 - Left | 8 - Top | 6 - Right | 5 - Down")
            # print("CurrentPlayerPos[", newPlayer.ReturnEntityPosition(0), "][" , newPlayer.ReturnEntityPosition(1), "] | ", end="")
            movement = input("Enter your next move: ")

            # print("Movement chosen by the player: ", movement)

            if movement != "":
                newGrid.MovePlayerInGrid(int(movement), newPlayer)

            newGrid.PrintCurrentGameGrid(False)

            gameOver = newGrid.CheckIfPlayerWonOrDied(newPlayer)

            if gameOver:
                self.scene = 0
                break

            if newGrid.ReturnEnemiesAlive() > 0:
                newGrid.MoveEnemiesInGrid(newPlayer)

                newGrid.PrintCurrentGameGrid(True)

            gameOver = newGrid.CheckIfPlayerWonOrDied(newPlayer)

            if gameOver:
                self.scene = 0
                break
