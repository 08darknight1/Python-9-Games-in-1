import random

class Cell:
    cellValue = ""

    def __init__(self, cellValue):
        self.cellValue = cellValue

    def ReturnCellValue(self):
        return self.cellValue

    def SetCellValue(self, newCellValue):
        self.cellValue = newCellValue

class Player:
    position = [0,0]

    def __init__(self, posX, posY):
        self.position[0] = posX
        self.position[1] = posY

    def ReturnPlayerPosition(self, index):
        return self.position[index]

    def SetNewPosForPlayer(self, value: int, index: int):
        self.position[index] = value

class Grid:
    gridOfCells = ""
    finalObjetive = [0,0]
    player = ""

    def __init__(self, lines, columns):
        self.gridOfCells = [[Cell("") for x in range(lines)] for y in range(columns)]

        for x in range(0, len(self.gridOfCells)):
            for y in range(0, len(self.gridOfCells[0])):
                isCellWall = random.randrange(0, 21)
                cellChar = "[ ]"
                if (isCellWall > 15):
                    cellChar = "[W]"

                self.gridOfCells[x][y].SetCellValue(cellChar)

    def ReturnGridSize(self, index):
        if(index == 1):
            return len(self.gridOfCells[0])
            
        return len(self.gridOfCells)

    def PrintCurrentGameGrid(self):
        for x in range(0, len(self.gridOfCells)):
            print("")
            for y in range(0, len(self.gridOfCells[0])):
                print(self.gridOfCells[x][y].cellValue, end="")

    def DefinePlayerObjective(self, coordX, coordY):
        if(coordX == -1 and coordY == -1):
            randX = random.randrange(0, len(self.gridOfCells))
            randY = random.randrange(0, len(self.gridOfCells[0]))

            self.gridOfCells[randX][randY].SetCellValue("[F]")
            self.finalObjetive[0] = randX
            self.finalObjetive[1] = randY
        else:
            self.gridOfCells[coordX][coordY].SetCellValue("[F]")
            self.finalObjetive[0] = coordX
            self.finalObjetive[1] = coordY

    def RegisterPlayer(self, newPlayer: Player):
        self.player = newPlayer
        self.gridOfCells[self.player.ReturnPlayerPosition(0)][self.player.ReturnPlayerPosition(1)].SetCellValue("[P]")

    def MovePlayerInGrid(self, posIndex: int):
        arrayIndex = 0
        newPos = 0
        operation = "minus"

        if posIndex == 6 or posIndex == 5:
            operation = "plus"

        if posIndex == 8 or posIndex == 5:
            arrayIndex = 1

        if operation == "minus":
            newPos = self.player.ReturnPlayerPosition(arrayIndex) - 1
        elif operation == "plus":
            newPos = self.player.ReturnPlayerPosition(arrayIndex) + 1

        if(newPos < 0 or newPos >= self.ReturnGridSize(0) or newPos >= self.ReturnGridSize(1)):
            print("Impossible to move!")
        else:
            cellPlayerWantsToMoveToPosX = newPos
            cellPlayerWantsToMoveToPosY = self.player.ReturnPlayerPosition(1)

            if(arrayIndex == 1):
                cellPlayerWantsToMoveToPosX = self.player.ReturnPlayerPosition(0)
                cellPlayerWantsToMoveToPosY = newPos

            cellPlayerWantsToMoveTo = self.gridOfCells[cellPlayerWantsToMoveToPosY][cellPlayerWantsToMoveToPosX]

            if(cellPlayerWantsToMoveTo.ReturnCellValue() == "[W]"):
                print("Player destroyed wall!")
                self.gridOfCells[cellPlayerWantsToMoveToPosY][cellPlayerWantsToMoveToPosX].SetCellValue("[ ]")
            else:
                self.gridOfCells[self.player.ReturnPlayerPosition(1)][self.player.ReturnPlayerPosition(0)].SetCellValue("[ ]")
                self.player.SetNewPosForPlayer(newPos, arrayIndex)
                self.gridOfCells[self.player.ReturnPlayerPosition(1)][self.player.ReturnPlayerPosition(0)].SetCellValue("[P]")

    def CheckIfPlayerHasWon(self):
        if(self.player.ReturnPlayerPosition(1) == self.finalObjetive[0] and self.player.ReturnPlayerPosition(0) == self.finalObjetive[1]):
            print("\n\nPlayer reached the end! You won, congratulations!!!")
            return True

        return False