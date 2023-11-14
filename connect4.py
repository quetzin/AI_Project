import random

# "🔵" is MAX player
# "🔴" is MIN player

##### Methods for implementing Connect Four game #####

print("Welcome to Connect Four")
print("-----------------------")

# Create Connect 4 board
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

def printGameBoard():   # Display the game
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


def modifyArray(position, spacePicked, turn):   # Make a move
    position[spacePicked[0]][spacePicked[1]] = turn
    return position


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


def coordinateParser(inputString): # Check if the picked position is valid letters or not
    coordinate = [None] * 2
    if inputString[0] in possibleLetters:
        coordinate[1] = possibleLetters.index(inputString[0])
    else:
        print("Invalid")
    coordinate[0] = int(inputString[1])
    return coordinate


def isSpaceAvailable(position, intendedCoordinate):   # Check if the picked position is empty
    if position[intendedCoordinate[0]][intendedCoordinate[1]] in ["🔴", "🔵"]:
        return False
    else:
        return True


def gravityChecker(position, intendedCoordinate):     # Check if the picked position is appropriate
    spaceBelow = [None] * 2
    spaceBelow[0] = intendedCoordinate[0] + 1
    spaceBelow[1] = intendedCoordinate[1]
    if spaceBelow[0] == 6:
        return True
    if isSpaceAvailable(position, spaceBelow) == False:
        return True
    return False


turnCounter = 0
while True:
    if turnCounter % 2 == 0:
        # MAX (🔵) turn
        printGameBoard()
        while True:
            spacePicked = random.choice(possibleLetters) + str(random.randint(0, 5))
            coordinate = coordinateParser(spacePicked)
            if isSpaceAvailable(gameBoard, coordinate) and gravityChecker(gameBoard, coordinate):
                gameBoard = modifyArray(gameBoard, coordinate, "🔵")
                break
        winner = checkForWinner("🔵")
        turnCounter += 1
    else:
        # MIN (🔴) turn
        while True:
            cpuChoice = [random.choice(possibleLetters), random.randint(0, 5)]
            cpuCoordinate = coordinateParser(
                "".join(map(str, cpuChoice))
            )
            if isSpaceAvailable(gameBoard, cpuCoordinate) and gravityChecker(gameBoard, cpuCoordinate):
                gameBoard = modifyArray(gameBoard, cpuCoordinate, "🔴")
                break
        winner = checkForWinner("🔴")
        turnCounter += 1

    if winner:
        printGameBoard()
        break


##### Methods for MINIMAX #####

def STATIC(position, player): # Static evalation function
    value = 0

    if(player == "🔵"):
        # Check for wins
        if is_winner(board, player):
            return float('inf')
        elif is_winner(board, get_opponent(player)):
            return float('-inf')

        # Evaluate based on connected pieces
        score += connected_pieces_score(board, player)

        # Evaluate based on blocking opponent's wins
        score += block_opponent_wins_score(board, player)

        # Evaluate based on center control
        score += center_control_score(board, player)

        # Add more evaluation criteria as needed
   # else:
        #
   # return value

def MOVE_GEN(position, player): # Generate leaf nodes
    successors = []
    for row in range(rows):
        for col in range(cols):
            coordinate = createSpacePicked(row, col)
            if isSpaceAvailable(position, coordinate) and gravityChecker(position, coordinate):
                position = modifyArray(position, coordinate, player)
                successors.append(position)       
    return successors

def OPPOSITE(player):   # Switch player
    if player == "🔵":  
        player = "🔴"   
    else:
        player = "🔵"   
    pass

def DEEP_ENOUGH(position, depth):    
    if(depth == turnCounter + depthLimit):   # Return true if it reaches to the depth limit
        boolean = True
    elif(depth == 0):   # Return true if it reaches to the root node
        boolean = True
    elif(checkForWinner(position, player) or checkForWinner(position, OPPOSITE(player))): # Return true if either player won
        boolean = True
    else:   # False otherwise
        boolean = False
        
    return boolean

def MINIMAX_AB(position, depth, player, passThresh, useThresh): # Minimax alpha-beta pruing
    if DEEP_ENOUGH(position, depth):
        value = STATIC(position, player)
        path = []
    else:
        successors = MOVE_GEN(position, player)
    
    if not successors:
        value = STATIC(position, player)
        path = []
    
    for succ in successors:
        result_succ = MINIMAX_AB(succ, depth + 1, OPPOSITE(player), -passThresh, -useThresh)
        new_value = -result_succ[0]
        
        if new_value > passThresh:
            passThresh = new_value
            bestPath = [succ] + result_succ[1]
        
        if passThresh >= useThresh:
            value = passThresh
            path = [bestPath]

    return passThresh, bestPath 

def createSpacePicked(row, col):    # Convert row number and colomn number into board psition  
    n = possibleLetters[col]
    spacePicked = [n, int(row)]
    return spacePicked