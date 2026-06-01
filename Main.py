from Labyrinthys import LabyrinthysMain
from GalaxyRun import GalaxyRunMain
from DogFight import DogFightMain
from GalaxyRaiders import GalaxyRaidersMain

print("Welcome to 9 Games in 1 [Python]")

gameOption = 0

while True:
    print("\nSelect a game to play: ")
    print("0- Labyrinthys")
    print("1- Galaxy Run")
    print("2- Dog Fight")
    print("3- Galaxy Raiders")
    print("10- Quit")

    gameOption = int(input("//-: "))

    if gameOption == 0:
        LabyrinthysMain.RunGame()
    elif gameOption == 1:
        GalaxyRunMain.RunGame(500, 500, 50, 50, 5)
    elif gameOption == 2:
        DogFightMain.RunGame(500, 500)
    elif gameOption == 3:
        GalaxyRaidersMain.RunGame(500, 500)
    elif gameOption == 10:
        break