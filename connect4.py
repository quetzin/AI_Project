import random

print("Welcome to Connect Four")
print("-----------------------")

possibleLetters = ["A", "B", "C", "D", "E", "F", "G"]
gameBoard = [
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
]

rows = 6
cols = 7

def printGameBoard():
    print("\n     A    B    C    D    E    F    G  ", end="")
    for x in range(rows):
        print("\n   +----+----+----+----+----+----+----+")
        print(x, " |", end="")
        for y in range(cols):
            if gameBoard[x][y] == "🔵":
                print("", gameBoard[x][y], end=" |")
            elif gameBoard[x][y] == "🔴":
                print("", gameBoard[x][y], end=" |")
            else:
                print(" ", gameBoard[x][y], end="  |")
    print("\n   +----+----+----+----+----+----+----+")


def modifyArray(spacePicked, turn):
    gameBoard[spacePicked[0]][spacePicked[1]] = turn


def checkForWinner(chip):
    # Check horizontal spaces
    for y in range(cols - 3):  
        for x in range(rows):
            if (
                gameBoard[x][y] == chip
                and gameBoard[x][y + 1] == chip
                and gameBoard[x][y + 2] == chip
                and gameBoard[x][y + 3] == chip
            ):
              print("\nGame over", chip, "wins! Thank you for playing :)")
              return True

    # Check vertical spaces
    for x in range(rows):
        for y in range(cols - 3):
            if (
                gameBoard[x][y] == chip
                and gameBoard[x][y + 1] == chip
                and gameBoard[x][y + 2] == chip
                and gameBoard[x][y + 3] == chip
            ):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    # Check upper right to bottom left diagonal spaces
    for x in range(rows - 3):
        for y in range(3, cols):
            if (
                gameBoard[x][y] == chip
                and gameBoard[x + 1][y - 1] == chip
                and gameBoard[x + 2][y - 2] == chip
                and gameBoard[x + 3][y - 3] == chip
            ):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    # Check upper left to bottom right diagonal spaces
    for x in range(rows - 3):
        for y in range(cols - 3):
            if (
                gameBoard[x][y] == chip
                and gameBoard[x + 1][y + 1] == chip
                and gameBoard[x + 2][y + 2] == chip
                and gameBoard[x + 3][y + 3] == chip
            ):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True
    return False


def coordinateParser(inputString):
    coordinate = [None] * 2
    if inputString[0] in possibleLetters:
        coordinate[1] = possibleLetters.index(inputString[0])
    else:
        print("Invalid")
    coordinate[0] = int(inputString[1])
    return coordinate


def isSpaceAvailable(intendedCoordinate):
    if gameBoard[intendedCoordinate[0]][intendedCoordinate[1]] in ["🔴", "🔵"]:
        return False
    else:
        return True


def gravityChecker(intendedCoordinate):
    spaceBelow = [None] * 2
    spaceBelow[0] = intendedCoordinate[0] + 1
    spaceBelow[1] = intendedCoordinate[1]
    if spaceBelow[0] == 6:
        return True
    if isSpaceAvailable(spaceBelow) == False:
        return True
    return False


turnCounter = 0
while True:
    if turnCounter % 2 == 0:
        # Player 1 (🔵) turn
        printGameBoard()
        while True:
            spacePicked = random.choice(possibleLetters) + str(random.randint(0, 5))
            coordinate = coordinateParser(spacePicked)
            if isSpaceAvailable(coordinate) and gravityChecker(coordinate):
                modifyArray(coordinate, "🔵")
                break
        winner = checkForWinner("🔵")
        turnCounter += 1
    else:
        # Player 2 (🔴) turn
        while True:
            cpuChoice = [random.choice(possibleLetters), random.randint(0, 5)]
            cpuCoordinate = coordinateParser(
                "".join(map(str, cpuChoice))
            )
            if isSpaceAvailable(cpuCoordinate) and gravityChecker(cpuCoordinate):
                modifyArray(cpuCoordinate, "🔴")
                break
        winner = checkForWinner("🔴")
        turnCounter += 1

    if winner:
        printGameBoard()
        break