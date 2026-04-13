import random

from Labyrinthys import Entities

class Cell:
    def __init__(self, cellValue):
        self.cellValue = cellValue

    def ReturnCellValue(self):
        return self.cellValue

    def SetCellValue(self, newCellValue):
        self.cellValue = newCellValue

class Grid:
    gridOfCells = ""
    finalObjetive = [0,0]
    enemies = []

    def __init__(self, lines, columns):
        self.gridOfCells = [[Cell("") for x in range(lines)] for y in range(columns)]

        for x in range(0, len(self.gridOfCells)):
            for y in range(0, len(self.gridOfCells[0])):
                isCellWall = random.randrange(0, 21)
                cellChar = "[ ]"
                if (isCellWall > 15):
                    cellChar = "[W]"

                self.gridOfCells[x][y].SetCellValue(cellChar)

    def RegisterEnemies(self, includeEnemies, randomNumber, enemiesNumber):
        if includeEnemies:
            actualNumber = enemiesNumber

            if randomNumber:
                #actualNumber = random.randrange(0, len(self.gridOfCells) * len(self.gridOfCells[0]))
                actualNumber = random.randrange(0, enemiesNumber)

            self.enemies = [Entities.Enemy(0, 0) for x in range(actualNumber)]

            for x in range(0, actualNumber):
                while True:
                    randPosX = random.randrange(0, len(self.gridOfCells))
                    randPosY = random.randrange(0, len(self.gridOfCells[0]))

                    randCellValue = self.gridOfCells[randPosX][randPosY].cellValue

                    if randCellValue == "[ ]" and self.finalObjetive[0] != randPosX and self.finalObjetive[1] != randPosY:
                        self.enemies[x].SetNewPosForEntity(randPosX, 0)
                        self.enemies[x].SetNewPosForEntity(randPosY, 1)

                        self.gridOfCells[randPosX][randPosY].SetCellValue("[E]")
                        break
            '''
            print("Enemies list size: ", len(self.enemies))

            for y in range(0, len(self.enemies)):
                print("Enemy[", y, "]-POS: ", self.enemies[y].ReturnEntityPosition(0),",", self.enemies[y].ReturnEntityPosition(1),"]")
            '''

    def ReturnGridSize(self, index):
        if index == 1:
            return len(self.gridOfCells[0])
            
        return len(self.gridOfCells)

    def PrintCurrentGameGrid(self, divider):
        if divider:
            print("")
            print("")
            for x in range(0, self.ReturnGridSize(1)):
                print("---", end="")
            print("")

        for x in range(0, len(self.gridOfCells)):
            print("")
            for y in range(0, len(self.gridOfCells[0])):
                if(self.gridOfCells[x][y].cellValue == "[ ]" and self.finalObjetive[0] == x and self.finalObjetive[1] == y):
                    print("[F]", end="")
                else:
                    print(self.gridOfCells[x][y].cellValue, end="")


    def DefinePlayerObjective(self, coordX, coordY, newPlayer: Entities.Player):
        if coordX == -1 and coordY == -1:
            while True:
                playerPos = [newPlayer.ReturnEntityPosition(0), newPlayer.ReturnEntityPosition(1)]

                randX = random.randrange(0, len(self.gridOfCells))
                randY = random.randrange(0, len(self.gridOfCells[0]))

                if playerPos[0] != randX and playerPos[1] != randY:
                    self.gridOfCells[randX][randY].SetCellValue("[F]")
                    self.finalObjetive[0] = randX
                    self.finalObjetive[1] = randY
                    break
        else:
            self.gridOfCells[coordX][coordY].SetCellValue("[F]")
            self.finalObjetive[0] = coordX
            self.finalObjetive[1] = coordY

    def RegisterPlayer(self, newPlayer: Entities.Player):
        #print("PlayerPosX: ", newPlayer.ReturnEntityPosition(0), "|PlayerPosY: ", newPlayer.ReturnEntityPosition(1))
        self.gridOfCells[newPlayer.ReturnEntityPosition(0)][newPlayer.ReturnEntityPosition(1)].SetCellValue("[P]")

    def MovePlayerInGrid(self, posIndex: int, newPlayer: Entities.Player):
        arrayIndex = 0
        newPos = 0
        operation = "minus"

        if posIndex == 6 or posIndex == 5:
            operation = "plus"

        if posIndex == 6 or posIndex == 4:
            arrayIndex = 1

        #print("Operation: ", operation, "|ArrayIndex: ", arrayIndex)

        if operation == "minus":
            newPos = newPlayer.ReturnEntityPosition(arrayIndex) - 1
        elif operation == "plus":
            newPos = newPlayer.ReturnEntityPosition(arrayIndex) + 1

        print("")

        if newPos < 0 or newPos >= self.ReturnGridSize(0) or newPos >= self.ReturnGridSize(1):
            print("Impossible to move!")
        else:
            cellPlayerWantsToMoveToPosX = newPos
            cellPlayerWantsToMoveToPosY = newPlayer.ReturnEntityPosition(1)

            if arrayIndex == 1:
                cellPlayerWantsToMoveToPosX = newPlayer.ReturnEntityPosition(0)
                cellPlayerWantsToMoveToPosY = newPos

            cellPlayerWantsToMoveTo = self.gridOfCells[cellPlayerWantsToMoveToPosX][cellPlayerWantsToMoveToPosY]

            if cellPlayerWantsToMoveTo.ReturnCellValue() == "[W]":
                print("Player destroyed wall!")
                self.gridOfCells[cellPlayerWantsToMoveToPosX][cellPlayerWantsToMoveToPosY].SetCellValue("[ ]")
            elif cellPlayerWantsToMoveTo.ReturnCellValue() == "[E]":
                print("Player destroyed enemy!")
                self.gridOfCells[cellPlayerWantsToMoveToPosX][cellPlayerWantsToMoveToPosY].SetCellValue("[ ]")

                #print("Length of enemies array: ", len(self.enemies))

                for x in range(0, len(self.enemies)):
                    #print("X Value: ", x)
                    #print("EnemyPosX: ", self.enemies[x].ReturnEntityPosition(0), ",", self.enemies[x].ReturnEntityPosition(1))
                    enemyPos = [self.enemies[x].ReturnEntityPosition(0), self.enemies[x].ReturnEntityPosition(1)]
                    if enemyPos[0] == cellPlayerWantsToMoveToPosX and enemyPos[1] == cellPlayerWantsToMoveToPosY:
                        self.enemies.pop(x)
                        break
            else:
                self.gridOfCells[newPlayer.ReturnEntityPosition(0)][newPlayer.ReturnEntityPosition(1)].SetCellValue("[ ]")
                newPlayer.SetNewPosForEntity(newPos, arrayIndex)
                self.gridOfCells[newPlayer.ReturnEntityPosition(0)][newPlayer.ReturnEntityPosition(1)].SetCellValue("[P]")

    def CheckIfPlayerWonOrDied(self, newPlayer: Entities.Player):
        playerPos = [newPlayer.ReturnEntityPosition(0), newPlayer.ReturnEntityPosition(1)]

        if playerPos[0] == self.finalObjetive[0] and playerPos[1] == self.finalObjetive[1]:
            print("\n\nPlayer reached the end! You won, congratulations!!!")
            return True

        for x in range(0, len(self.enemies)):
            enemyPos = [self.enemies[x].ReturnEntityPosition(0), self.enemies[x].ReturnEntityPosition(1)]
            if playerPos[0] == enemyPos[0] and playerPos[1] == enemyPos[1]:
                print("\n\nPlayer killed by enemy :(")
                return True

        return False

    def MoveEnemiesInGrid(self, newPlayer: Entities.Player):
       #print("\n\nPlayer Current Pos: ", newPlayer.ReturnEntityPosition(0),",", newPlayer.ReturnEntityPosition(1))
       if self.enemies != "":
            for x in range(0, len(self.enemies)):
                posToRemove = self.enemies[x].MoveAfterPlayer(newPlayer)
                newEnemyPos = [self.enemies[x].ReturnEntityPosition(0),self.enemies[x].ReturnEntityPosition(1)]

                if self.gridOfCells[newEnemyPos[0]][newEnemyPos[1]].ReturnCellValue() == "[E]":
                    #print("\nWaiting for another one to move like a good boy :) !")
                    self.enemies[x].SetNewPosForEntity(posToRemove[0], 0)
                    self.enemies[x].SetNewPosForEntity(posToRemove[1], 1)
                else:
                    self.gridOfCells[posToRemove[0]][posToRemove[1]].SetCellValue("[ ]")
                    self.gridOfCells[newEnemyPos[0]][newEnemyPos[1]].SetCellValue("[E]")

    def ReturnEnemiesAlive(self):
        return len(self.enemies)
