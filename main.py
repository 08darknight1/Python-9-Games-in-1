import GameGrid

gameRunning = True

newGrid = GameGrid.Grid(12, 12)

newGrid.DefinePlayerObjective(5, 4)

newPlayer = GameGrid.Player(0, 0)

newGrid.RegisterPlayer(newPlayer)

#print("Game still running...")
#print("Creating new game grid...")

#print("Game grid created! Current size " , newGrid.ReturnGridSize(0) , "X" , newGrid.ReturnGridSize(1))

newGrid.PrintCurrentGameGrid()

while gameRunning:
    #get input from player
    print("\n\n4 - Left | 8 - Top | 6 - Right | 5 - Down")
    print("CurrentPlayerPos[", newPlayer.ReturnPlayerPosition(0), "][" , newPlayer.ReturnPlayerPosition(1), "]", end="")
    movement = input(" | Enter your next move: ")

    #print("Movement chosen by the player: ", movement)

    if movement != "":
        newGrid.MovePlayerInGrid(int(movement))

    newGrid.PrintCurrentGameGrid()

    gameRunning = not newGrid.CheckIfPlayerHasWon()


