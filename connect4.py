import random

depthLimit1 = 2
depthLimit2 = 4
depthLimit3 = 8
turnCounter = 0
# "🔵" is MAX player
# "🔴" is MIN player


print("Welcome to Connect Four")
print("-----------------------")

############ Methods for Connect 4 game ############

### Create Connect 4 board ###
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


### Display the game ###
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


### Make a move ###
def modifyArray(position, spacePicked, turn): 
    position[spacePicked[0]][spacePicked[1]] = turn
    return position

### Check if there are 4 pieces lined up ###
def checkForWinner(position, chip): 
    # Check horizontal spaces
    for y in range(cols - 3):  
        for x in range(rows):
            if (
                position[x][y] == chip
                and position[x][y + 1] == chip
                and position[x][y + 2] == chip
                and position[x][y + 3] == chip
            ):
              print("\nGame over", chip, "wins! Thank you for playing :)")
              return True

    # Check vertical spaces
    for x in range(rows):
        for y in range(cols - 3):
            if (
                position[x][y] == chip
                and position[x][y + 1] == chip
                and position[x][y + 2] == chip
                and position[x][y + 3] == chip
            ):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    # Check upper right to bottom left diagonal spaces
    for x in range(rows - 3):
        for y in range(3, cols):
            if (
                position[x][y] == chip
                and position[x + 1][y - 1] == chip
                and position[x + 2][y - 2] == chip
                and position[x + 3][y - 3] == chip
            ):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    # Check upper left to bottom right diagonal spaces
    for x in range(rows - 3):
        for y in range(cols - 3):
            if (
                position[x][y] == chip
                and position[x + 1][y + 1] == chip
                and position[x + 2][y + 2] == chip
                and position[x + 3][y + 3] == chip
            ):
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True
    return False


### Check if the picked position is valid letters or not ###
def coordinateParser(inputString): 
    coordinate = [None] * 2
    if inputString[0] in possibleLetters:
        coordinate[1] = possibleLetters.index(inputString[0])
    else:
        print("Invalid")
    coordinate[0] = int(inputString[1])
    return coordinate

### Check if tthe picked position is empty ###
def isSpaceAvailable(position, intendedCoordinate): 
    if position[intendedCoordinate[0]][intendedCoordinate[1]] in ["🔴", "🔵"]:
        return False
    else:
        return True

### Check if the picked position is appropriate ###
def gravityChecker(position, intendedCoordinate):     
    spaceBelow = [None] * 2
    spaceBelow[0] = intendedCoordinate[0] + 1
    spaceBelow[1] = intendedCoordinate[1]
    if spaceBelow[0] == 6:
        return True
    if isSpaceAvailable(position, spaceBelow) == False:
        return True
    return False


############ Methods for minimax ############

### Static evaluation funtions ###
## EV1 
def static(position, player):
    score = 0

    # Check rows for winning positions
    for row in range(rows):
        for col in range(cols-3):
            if position[row][col] == position[row][col+1] == position[row][col+2] == position[row][col+3]:
                if position[row][col] == "🔵":
                    score += 100
                elif position[row][col] == "🔴":
                    score -= 100

    # Check columns for winning positions
    for col in range(cols):
        for row in range(row-3):
            if position[row][col] == position[row+1][col] == position[row+2][col] == position[row+3][col]:
                if position[row][col] == "🔵":
                    score += 100
                elif position[row][col] == "🔴":
                    score -= 100

    # Check diagonals for winning positions
    for row in range(rows-3):
        for col in range(cols-3):
            if position[row][col] == position[row+1][col+1] == position[row+2][col+2] == position[row+3][col+3]:
                if position[row][col] == "🔵":
                    score += 100
                elif position[row][col] == "🔴":
                    score -= 100

    for row in range(3, rows):
        for col in range(cols-3):
            if position[row][col] == position[row-1][col+1] == position[row-2][col+2] == position[row-3][col+3]:
                if position[row][col] == "🔵":
                    score += 100
                elif position[row][col] == "🔴":
                    score -= 100

    # Check for potential winning positions
    for row in range(rows):
        for col in range(cols-3):
            if position[row][col] == position[row][col+1] == position[row][col+2] == "🔵":
                score += 10
            elif position[row][col] == position[row][col+1] == position[row][col+2] == "🔴":
                score -= 10

    for col in range(cols):
        for row in range(rows-3):
            if position[row][col] == position[row+1][col] == position[row+2][col] == "🔵":
                score += 10
            elif position[row][col] == position[row+1][col] == position[row+2][col] == "🔴":
                score -= 10

    for row in range(rows-3):
        for col in range(cols-3):
            if position[row][col] == position[row+1][col+1] == position[row+2][col+2] == "🔵":
                score += 10
            elif position[row][col] == position[row+1][col+1] == position[row+2][col+2] == "🔴":
                score -= 10

    for row in range(3, rows):
        for col in range(cols-3):
            if position[row][col] == position[row-1][col+1] == position[row-2][col+2] == "🔵":
                score += 10
            elif position[row][col] == position[row-1][col+1] == position[row-2][col+2] == "🔴":
                score -= 10

    # Check for center control
    if position[rows-1][cols-4] == "🔵":
        score += 20
    elif position[rows-1][cols-4] == "🔴":
        score -= 20

    return score

## EV2 (Doesn't check the potential winning and the center control)
def static2(position, player): 
    score = 0

    # Check rows for winning positions
    for row in range(rows):
        for col in range(cols-3):
            if position[row][col] == position[row][col+1] == position[row][col+2] == position[row][col+3]:
                if position[row][col] == "🔵":
                    score += 100
                elif position[row][col] == "🔴":
                    score -= 100

    # Check columns for winning positions
    for col in range(cols):
        for row in range(row-3):
            if position[row][col] == position[row+1][col] == position[row+2][col] == position[row+3][col]:
                if position[row][col] == "🔵":
                    score += 100
                elif position[row][col] == "🔴":
                    score -= 100

    # Check diagonals for winning positions
    for row in range(rows-3):
        for col in range(cols-3):
            if position[row][col] == position[row+1][col+1] == position[row+2][col+2] == position[row+3][col+3]:
                if position[row][col] == "🔵":
                    score += 100
                elif position[row][col] == "🔴":
                    score -= 100

    for row in range(3, rows):
        for col in range(cols-3):
            if position[row][col] == position[row-1][col+1] == position[row-2][col+2] == position[row-3][col+3]:
                if position[row][col] == "🔵":
                    score += 100
                elif position[row][col] == "🔴":
                    score -= 100
    return score

### Convert row number and colomn number into board position  ###
def createSpacePicked(row, col): 
    n = possibleLetters[col]
    spacePicked = [n, int(row)]
    return spacePicked

### Generate leaf nodes ###
def move_gen(position, player): 
    successors = []
    for row in range(rows):
        for col in range(cols):
            coordinate = createSpacePicked(row, col)
            if isSpaceAvailable(position, coordinate) and gravityChecker(position, coordinate):
                position = modifyArray(position, coordinate, player)
                successors.append(position)       
    return successors

### Switch player ###
def opposite(player):   
    if player == "🔵":  
        player = "🔴"   
    else:
        player = "🔵"   
    pass

### Check if it reaches to the certain conditions ###
def deep_enough(position, depth):   

    if(depth == turnCounter + depthLimit1):   # Return true if it reaches to the depth limit
        boolean = True
    elif(checkForWinner(position, "🔵") or checkForWinner(position, "🔴")): # Return true if either player won
        boolean = True
    else:   # False otherwise
        boolean = False
    
        
    return boolean

### Minimax Alpha-Beta Pruing ###
## With EV1 
def minimax_ab_ev1(position, depth, player, passThresh, useThresh): 
    if deep_enough(position, depth):
        value = static(position, player)
        path = []
        return value, path
        
    else:
        successors = move_gen(position, player)
    
    if not successors:
        value = static(position, player)
        path = []
        return value, path

    else:
        for succ in successors:
            result_succ = minimax_ab_ev1(succ, depth + 1, opposite(player), -passThresh, -useThresh)
            new_value = -result_succ[0]
            
            if new_value > passThresh:
                passThresh = new_value
                bestPath = [succ] + result_succ[1]
            
            if passThresh >= useThresh:
                value = passThresh
                path = [bestPath]

    return passThresh, bestPath

## With EV2 
def minimax_ab_ev2(position, depth, player, passThresh, useThresh): 
    if deep_enough(position, depth):
        value = static2(position, player)
        path = []
        return value, path
        
    else:
        successors = move_gen(position, player)
    
    if not successors:
        value = static2(position, player)
        path = []
        return value, path

    else:
        for succ in successors:
            result_succ = minimax_ab_ev2(succ, depth + 1, opposite(player), -passThresh, -useThresh)
            new_value = -result_succ[0]
            
            if new_value > passThresh:
                passThresh = new_value
                bestPath = [succ] + result_succ[1]
            
            if passThresh >= useThresh:
                value = passThresh
                path = [bestPath]

    return passThresh, bestPath  


############ Connect 4 ############
while True:
    if turnCounter % 2 == 0:
        # MAX (🔵) turn
        printGameBoard()
        while True:
            #value, path = minimax_ab_ev1(gameBoard, turnCounter, "🔵", float('inf'), float('-inf') )
            #spacePicked = path[0]
            spacePicked = random.choice(possibleLetters) + str(random.randint(0, 5))
            coordinate = coordinateParser(spacePicked)
            if isSpaceAvailable(gameBoard, coordinate) and gravityChecker(gameBoard, coordinate):
                gameBoard = modifyArray(gameBoard, coordinate, "🔵")
                break
        winner = checkForWinner(gameBoard, "🔵")
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
        winner = checkForWinner(gameBoard, "🔴")
        turnCounter += 1

    if winner:
        printGameBoard()
        break







