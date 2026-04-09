import random

class Entity:
    position = [0,0]

    def __init__(self, posX: int, posY: int):
        self.position = [posX, posY]

    def ReturnEntityPosition(self, index: int):
        return self.position[index]

    def SetNewPosForEntity(self, value: int, index: int):
        self.position[index] = value

class Player(Entity):
    def __init__(self, posX: int, posY: int):
        super().__init__(posX, posY)

    def ReturnEntityPosition(self, index: int):
        #super().ReturnEntityPosition(index)
        return self.position[index]

    def SetNewPosForEntity(self, value: int, index: int):
        self.position[index] = value

class Enemy(Entity):
    def __init__(self, posX: int, posY: int):
        super().__init__(posX, posY)

    def ReturnEntityPosition(self, index: int):
        #super().ReturnEntityPosition(index)
        return self.position[index]

    def SetNewPosForEntity(self, value: int, index: int):
        self.position[index] = value

    def MoveAfterPlayer(self, player: Player):
        #print("\nMy current position[", self.ReturnEntityPosition(0), "][", self.ReturnEntityPosition(1), "]")

        playerPos = [player.ReturnEntityPosition(0), player.ReturnEntityPosition(1)]

        afterMovingUpPos = self.ReturnEntityPosition(0) - 1
        afterMovingDownPos = self.ReturnEntityPosition(0) + 1
        afterMovingLeftPos = self.ReturnEntityPosition(1) - 1
        afterMovingRightPos = self.ReturnEntityPosition(1) + 1

        '''
        print("If I move up, my position in X will change from [", self.ReturnEntityPosition(0),"] to [", afterMovingUpPos,"]")
        print("If I move down, my position in X will change from [", self.ReturnEntityPosition(0),"] to [", afterMovingDownPos,"]")
        print("If I move left, my position in Y will  change from [", self.ReturnEntityPosition(1),"] to [", afterMovingLeftPos,"]")
        print("If I move right, my position in Y will  change from [", self.ReturnEntityPosition(1),"] to [", afterMovingRightPos,"]")
        '''

        upDiff = [afterMovingUpPos - playerPos[0], self.ReturnEntityPosition(1) - playerPos[1]]
        downDiff = [afterMovingDownPos - playerPos[0], self.ReturnEntityPosition(1) - playerPos[1]]
        leftDiff = [self.ReturnEntityPosition(0) - playerPos[0], afterMovingLeftPos - playerPos[1]]
        rightDiff = [self.ReturnEntityPosition(0) - playerPos[0], afterMovingRightPos - playerPos[1]]

        '''
        print("Difference to player when moving up - X[", upDiff[0],"]Y[", upDiff[1],"]")
        print("Difference to player when moving down - X[", downDiff[0],"]Y[", downDiff[1],"]")
        print("Difference to player when moving left - X[", leftDiff[0],"]Y[", leftDiff[1],"]")
        print("Difference to player when moving right - X[", rightDiff[0],"]Y[", rightDiff[1],"]")
        '''

        for x in range(0, 5):
            for y in range(0, 2):
                if x == 0:
                    if upDiff[y] < 0:
                        upDiff[y] = upDiff[y] * -1
                if x == 1:
                    if downDiff[y] < 0:
                        downDiff[y] = downDiff[y] * -1
                if x == 2:
                    if leftDiff[y] < 0:
                        leftDiff[y] = leftDiff[y] * -1
                if x == 3:
                    if rightDiff[y] < 0:
                        rightDiff[y] = rightDiff[y] * -1

        fullDiffValues = [upDiff[0] + upDiff[1], downDiff[0] + downDiff[1], leftDiff[0] + leftDiff[1], rightDiff[0] + rightDiff[1]]

        '''
        for x in range(0, len(fullDiffValues)):
            if fullDiffValues[x] < 0:
                fullDiffValues[x] = fullDiffValues[x] * -1
        '''

        smallestValue = "none"

        indexFound = "none"

        duplicatesFound = []

        for x in range(0, len(fullDiffValues)):
            if(fullDiffValues[x] >= 0):                  #tem q definir se aqui precisa de ser maior que ou igual, ou só maior que
                if smallestValue == "none":
                    smallestValue = fullDiffValues[x]
                    indexFound = x
                elif fullDiffValues[x] < smallestValue:
                    smallestValue = fullDiffValues[x]
                    indexFound = x
                elif fullDiffValues[x] == smallestValue:
                    duplicatesFound.append(fullDiffValues[x])
                    duplicatesFound.append(smallestValue)

        if len(duplicatesFound) > 0:
            smallestValue = duplicatesFound[random.randrange(0, len(duplicatesFound))]

        #print("Best move to reach player:" , smallestValue)

        posToReturn = [self.ReturnEntityPosition(0), self.ReturnEntityPosition(1)]

        if indexFound == 0:
            self.SetNewPosForEntity(afterMovingUpPos, 0)
            #print("Im moving up!")
        elif indexFound == 1:
            self.SetNewPosForEntity(afterMovingDownPos, 0)
            #print("Im moving down!")
        elif indexFound == 2:
            self.SetNewPosForEntity(afterMovingLeftPos, 1)
            #print("Im moving left!")
        elif indexFound == 3:
            self.SetNewPosForEntity(afterMovingRightPos, 1)
            #print("Im moving right!")
        #o index 1 é pra mover no X e o index 0 é pra mover no Y

        return posToReturn