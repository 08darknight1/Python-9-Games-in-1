from Labyrinthys import LabyrinthysMain
from PyGameTestGame import PyGameMain

print("Welcome to 9 Games in 1 [Python]")

gameOption = 0

while True:
    print("\nSelect a game to play: ")
    print("0- Labyrinthis")
    print("1- PyGameTest")
    print("10- Quit")
    gameOption = int(input("//-: "))

    if gameOption == 0:
        LabyrinthysMain.RunGame()
    elif gameOption == 1:
        PyGameMain.RunGame(800, 600, 50, 50, 5)
    elif gameOption == 10:
        break