from Labyrinthys import LabyrinthysMain

print("Welcome to 9 Games in 1 [Python]")

gameOption = 0

while True:
    print("\nSelect a game to play: ")
    print("0- Labyrinthis")
    print("10- Quit")
    gameOption = int(input("//-: "))

    if gameOption == 0:
        LabyrinthysMain.RunGame()
    elif gameOption == 10:
        break