import GameGrid
import Entities
import random

gameRunning = True

gridSize = random.randrange(12, 21)

#print("GridSize selected: ", gridSize)

enemiesCount = gridSize/2

#print("Enemies Count selected: ", enemiesCount)

newGrid = GameGrid.Grid(5, 5)

newPlayer = Entities.Player(0, 0)

newGrid.RegisterPlayer(newPlayer)

newGrid.DefinePlayerObjective(-1, -1, newPlayer)

#print("PlayerzaoPOS[", newPlayer.ReturnEntityPosition(0), "][" , newPlayer.ReturnEntityPosition(1), "]")

newGrid.RegisterEnemies(True, False, 1)

#print("Game still running...")
#print("Creating new game grid...")

#print("Game grid created! Current size " , newGrid.ReturnGridSize(0) , "X" , newGrid.ReturnGridSize(1))

newGrid.PrintCurrentGameGrid(False)

while gameRunning:
    #get input from player
    print("\n\n4 - Left | 8 - Top | 6 - Right | 5 - Down")
    #print("CurrentPlayerPos[", newPlayer.ReturnEntityPosition(0), "][" , newPlayer.ReturnEntityPosition(1), "] | ", end="")
    movement = input("Enter your next move: ")

    #print("Movement chosen by the player: ", movement)

    if movement != "":
        newGrid.MovePlayerInGrid(int(movement), newPlayer)

    newGrid.PrintCurrentGameGrid(False)

    gameRunning = not newGrid.CheckIfPlayerWonOrDied(newPlayer)

    if not gameRunning: break

    if newGrid.ReturnEnemiesAlive() > 0:
        newGrid.MoveEnemiesInGrid(newPlayer)

        newGrid.PrintCurrentGameGrid(True)

    gameRunning = not newGrid.CheckIfPlayerWonOrDied(newPlayer)

    if not gameRunning: break



