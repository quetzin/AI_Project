import random
import copy

#depthLimit1 = 2
#depthLimit1 = 4
depthLimit1 = 8

depthLimit2 = 2
#depthLimit2 = 4
#depthLimit2 = 8

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
def printGameBoard(position):
    print("\n     A    B    C    D    E    F    G  ", end="")
    for x in range(rows):
        print("\n   +----+----+----+----+----+----+----+")
        print(x, " |", end="")
        for y in range(cols):
            if position[x][y] == "🔵":
                print("", position[x][y], end=" |")
            elif position[x][y] == "🔴":
                print("", position[x][y], end=" |")
            else:
                print(" ", position[x][y], end="  |")
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
              #print("\nGame over", chip, "wins! Thank you for playing :)")
              return True

    # Check vertical spaces
    for x in range(rows - 3):
        for y in range(cols):
            if (
                position[x][y] == chip
                and position[x + 1][y] == chip
                and position[x + 2][y] == chip
                and position[x + 3][y] == chip
            ):
                #print("\nGame over", chip, "wins! Thank you for playing :)")
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
                #print("\nGame over", chip, "wins! Thank you for playing :)")
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
                #print("\nGame over", chip, "wins! Thank you for playing :)")
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
    #print("in move_gem")
    successors = []
    new_position = copy.deepcopy(position)
    #print("check initial position")
    #printGameBoard(new_position)
    for row in range(rows):
        for col in range(cols):
            coordinate = coordinateParser(createSpacePicked(row, col))
            if isSpaceAvailable(new_position, coordinate) and gravityChecker(new_position, coordinate):
                new_position = modifyArray(new_position, coordinate, player)
                #print("check new position")
                #printGameBoard(new_position)
                successors.append(new_position)
                new_position = copy.deepcopy(position)
    #print(successors)                 
    return successors

### Switch player ###
def opposite(player):   
    if player == "🔵":  
        player = "🔴"   
    else:
        player = "🔵"   
    return player

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
def minimax_ab_ev1(position, depth, player, passThresh, useThresh, count):
    #print("in minimax_ab") 
    #print("depth ", count)
    #print("turn ", player)
    if deep_enough(position, depth):
        #print("it is deep enough")
        value = static(position, player)
        path = []
        #print("depth ", count)
        #print("value returned: ", value)
        #print("path returned: ", path)
        return value, path
        
    #print("generate successors")
    successors = move_gen(position, player)
    
    if not successors:
        #print("successors is empty")
        value = static(position, player)
        path = []
        #print("depth ", count)
        #print("value returned: ", value)
        #print("path returned: ", path)
        return value, path 

    bestPath= []
    for succ in successors:
        #print("in for loop")
        resultSucc = minimax_ab_ev1(succ, depth + 1, opposite(player), -passThresh, -useThresh, count+1)
        new_value = -resultSucc[0]
        
        if new_value > passThresh:
            passThresh = new_value
            bestPath = [succ] + resultSucc[1]
        
        if passThresh >= useThresh:
            #print("depth ", count)
            #print("value returned: ", passThresh)
            #print("path returned: ")
            #printGameBoard(position)
            return passThresh, bestPath

    #print("depth ", count)
    #print("value returned: ", passThresh)
    #print("path returned: ")
    #printGameBoard(position)
    return passThresh, bestPath

## With EV2 
def minimax_ab_ev2(position, depth, player, passThresh, useThresh, count): 
    #print("in minimax_ab") 
    #print("depth ", count)
    #print("turn ", player)
    if deep_enough(position, depth):
        #print("it is deep enough")
        value = static2(position, player)
        path = []
        #print("depth ", count)
        #print("value returned: ", value)
        #print("path returned: ", path)
        return value, path
        
    #print("generate successors")
    successors = move_gen(position, player)
    
    if not successors:
        #print("successors is empty")
        value = static2(position, player)
        path = []
        #print("depth ", count)
        #print("value returned: ", value)
        #print("path returned: ", path)
        return value, path 

    bestPath= []
    for succ in successors:
        #print("in for loop")
        resultSucc = minimax_ab_ev2(succ, depth + 1, opposite(player), -passThresh, -useThresh, count+1)
        new_value = -resultSucc[0]
        
        if new_value > passThresh:
            passThresh = new_value
            bestPath = [succ] + resultSucc[1]
        
        if passThresh >= useThresh:
            #print("depth ", count)
            #print("value returned: ", passThresh)
            #print("path returned: ")
            #printGameBoard(position)
            return passThresh, bestPath

    #print("depth ", count)
    #print("value returned: ", passThresh)
    #print("path returned: ")
    #printGameBoard(position)
    return passThresh, bestPath

############ Connect 4 ############
while True:
    if turnCounter % 2 == 0:
        # MAX (🔵) turn
        printGameBoard(gameBoard)
        while True:
            #print("ACTUAL TURN 🔵")
            result = minimax_ab_ev1(gameBoard, turnCounter, "🔵", 100, -100,0 )
            #print(result[1])
            spacePicked = result[1]
            if not spacePicked: # Pick a random position when the path is empty
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
            #print("ACTUAL TURN 🔴")
            cpuChoice = [random.choice(possibleLetters), random.randint(0, 5)]
            cpuCoordinate = coordinateParser(
                "".join(map(str, cpuChoice))
            )
            if isSpaceAvailable(gameBoard, cpuCoordinate) and gravityChecker(gameBoard, cpuCoordinate):
                gameBoard = modifyArray(gameBoard, cpuCoordinate, "🔴")
                break
        winner = checkForWinner(gameBoard, "🔴")
        turnCounter += 1

    #printGameBoard(gameBoard)

    if(checkForWinner(gameBoard, "🔵")):
        printGameBoard(gameBoard)
        print("\nGame over 🔵 wins! Thank you for playing :)")
        break;
    if(checkForWinner(gameBoard, "🔴")):
        printGameBoard(gameBoard)
        print("\nGame over 🔴 wins! Thank you for playing :)")
        break;







