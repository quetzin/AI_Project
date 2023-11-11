import random

print("Hello Welcome to Connect Four")
print("-----------------------------")
print("\n")

possibleLetters = ["A", "B", "C", "D", "E", "F", "G"]
rows = 6
cols = 7
gameBoard = [[" " for _ in range(cols)] for _ in range(rows)]

def printGameBoard():
    print("\n     A    B    C    D    E    F    G  ", end="")
    for x in range(rows):
        print("\n   +----+----+----+----+----+----+----+")
        print(x, " |", end="")
        for y in range(cols):
            print(" " + gameBoard[x][y] + "  |", end="")
    print("\n   +----+----+----+----+----+----+----+")

def modifyArray(position, spacePicked, turn):
    position[spacePicked[0]][spacePicked[1]] = turn

def checkForWinner(chip):
    for x in range(rows):
        for y in range(cols - 3):
            if all(gameBoard[x][y + i] == chip for i in range(4)):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    for x in range(rows - 3):
        for y in range(cols):
            if all(gameBoard[x + i][y] == chip for i in range(4)):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    for x in range(rows - 3):
        for y in range(3, cols):
            if all(gameBoard[x + i][y - i] == chip for i in range(4)):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    for x in range(rows - 3):
        for y in range(cols - 3):
            if all(gameBoard[x + i][y + i] == chip for i in range(4)):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    return False

def coordinateParser(inputString):
    if inputString[0] in possibleLetters and inputString[1:].isdigit():
        col = possibleLetters.index(inputString[0])
        row = int(inputString[1])
        return (row, col)
    else:
        print("Invalid")
        return None

def createSpacePicked(row, col):
    n = possibleLetters[col]
    inputString = [n, int(row)]
    return inputString

def isSpaceAvailable(intendedCoordinate):
    row, col = intendedCoordinate
    return gameBoard[row][col] == " "

def gravityChecker(intendedCoordinate):
    row, col = intendedCoordinate
    return row == 5 or gameBoard[row + 1][col] != " "

leaveLoop = False
turnCounter = 0

while not leaveLoop:
    if turnCounter % 2 == 0:
        printGameBoard()
        while True:
            spacePicked = input("\nChoose a space: ")
            coordinate = coordinateParser(spacePicked)
            if coordinate is not None:
                if isSpaceAvailable(coordinate) and gravityChecker(coordinate):
                    modifyArray(gameBoard,coordinate, '🔵')
                    break
                else:
                    print("Not a valid spot on the board. Please try again.")
    else:
        while True:
            col = random.choice(possibleLetters)
            row = random.randint(0, 5)
            cpuChoice = (row, possibleLetters.index(col))
            if isSpaceAvailable(cpuChoice) and gravityChecker(cpuChoice):
                modifyArray(gameBoard,cpuChoice, '🔴')
                break
    turnCounter += 1
    winner = checkForWinner('🔵' if turnCounter % 2 == 0 else '🔴')

    if winner:
        printGameBoard()
        break
