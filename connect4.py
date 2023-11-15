import random
import copy

#depthLimit1 = 2
#depthLimit1 = 4
depthLimit1 = 8

#depthLimit2 = 2
#depthLimit2 = 4
depthLimit2 = 8

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
## EV1 (preventing opponets' win)
def static(position, player):
    score = 0
    opponent = opposite(player)

    # Check for winning positions
    for row in range(rows): # Horizontal
        for col in range(cols-3):
            if position[row][col] == position[row][col+1] == position[row][col+2] == position[row][col+3] == player:
                score += 100

    for col in range(cols): # Vertical
        for row in range(row-3):
            if position[row][col] == position[row+1][col] == position[row+2][col] == position[row+3][col] == player:
                score += 100

    for row in range(rows-3):   # Positive diagnal
        for col in range(cols-3):
            if position[row][col] == position[row+1][col+1] == position[row+2][col+2] == position[row+3][col+3] == player:
                score += 100

    for row in range(3, rows):  # Negative diagnal
        for col in range(cols-3):
            if position[row][col] == position[row-1][col+1] == position[row-2][col+2] == position[row-3][col+3] == player:
                score += 100

    # Check for potential winning positions
    for row in range(rows): # Horizontal
        for col in range(cols-3):
            if position[row][col] == position[row][col+1] == position[row][col+2] == player:
                score += 50
        
    for col in range(cols): # Vertical
        for row in range(rows-3):
            if position[row][col] == position[row+1][col] == position[row+2][col] == player:
                score += 50

    for row in range(rows-3):   # Positive diagnal
        for col in range(cols-3):
            if position[row][col] == position[row+1][col+1] == position[row+2][col+2] == player:
                score += 50

    for row in range(3, rows):  # Negative diagnal
        for col in range(cols-3):
            if position[row][col] == position[row-1][col+1] == position[row-2][col+2] == player:
                score += 50
    
     # Check for preventing oppoenet's potential winning positions
    for row in range(rows): # Horizontal
        for col in range(cols-3):
            if((position[row][col] == position[row][col+1] == position[row][col+2] == opponent and position[row][col+3] == player) or 
            (position[row][col] == position[row][col+1] == position[row][col+3] == opponent and position[row][col+2] == player) or 
            (position[row][col] == position[row][col+2] == position[row][col+3] == opponent and position[row][col+1] == player) or 
            (position[row][col+1] == position[row][col+2] == position[row][col+3] == opponent and position[row][col] == player)):
                score += 90
        
    for col in range(cols): # Vertical
        for row in range(rows-3):
            if((position[row][col] == position[row+1][col] == position[row+2][col] == opponent and position[row+3][col] == player) or 
            (position[row][col] == position[row+1][col] == position[row+3][col] == opponent and position[row+2][col] == player) or 
            (position[row][col] == position[row+2][col] == position[row+3][col] == opponent and position[row+1][col] == player) or 
            (position[row+1][col] == position[row+2][col] == position[row+3][col] == opponent and position[row][col] == player)):
                score += 90

    for row in range(rows-3):   # Positive diagnal
        for col in range(cols-3):
            if((position[row][col] == position[row+1][col+1] == position[row+2][col+2] == opponent and position[row+3][col+3] == player) or 
            (position[row][col] == position[row+1][col+1] == position[row+3][col+3] == opponent and position[row+2][col+2] == player) or 
            (position[row][col] == position[row+2][col+2] == position[row+3][col+3] == opponent and position[row+1][col+1] == player) or
            (position[row+1][col+1] == position[row+2][col+2] == position[row+3][col+3] == opponent and position[row][col] == player)):
                score += 90

    for row in range(3, rows):  # Negative diagnal
        for col in range(cols-3):
            if((position[row][col] == position[row-1][col+1] == position[row-2][col+2] == opponent and position[row-3][col+3] == player) or 
            (position[row][col] == position[row-1][col+1] == position[row-3][col+3] == opponent and position[row-2][col+2] == player) or 
            (position[row][col] == position[row-2][col+2] == position[row-3][col+3] == opponent and position[row-1][col+1] == player) or 
            (position[row-1][col+1] == position[row-2][col-2] == position[row-3][col+3] == opponent and position[row][col] == player)):
                score += 90

    # Check for center control
    if position[rows-1][cols-4] == player:
        score += 20

    if player == "🔴":
        score = -score

    return score

## EV2 (preventing opponent is less important here)
def static2(position, player): 
    score = 0
    opponent = opposite(player)

    # Check for winning positions
    for row in range(rows): # Horizontal
        for col in range(cols-3):
            if position[row][col] == position[row][col+1] == position[row][col+2] == position[row][col+3] == player:
                score += 100

    for col in range(cols): # Vertical
        for row in range(row-3):
            if position[row][col] == position[row+1][col] == position[row+2][col] == position[row+3][col] == player:
                score += 100

    for row in range(rows-3):   # Positive diagnal
        for col in range(cols-3):
            if position[row][col] == position[row+1][col+1] == position[row+2][col+2] == position[row+3][col+3] == player:
                score += 100

    for row in range(3, rows):  # Negative diagnal
        for col in range(cols-3):
            if position[row][col] == position[row-1][col+1] == position[row-2][col+2] == position[row-3][col+3] == player:
                score += 100

    # Check for potential winning positions
    for row in range(rows): # Horizontal
        for col in range(cols-3):
            if position[row][col] == position[row][col+1] == position[row][col+2] == player:
                score += 80
        
    for col in range(cols): # Vertical
        for row in range(rows-3):
            if position[row][col] == position[row+1][col] == position[row+2][col] == player:
                score += 80

    for row in range(rows-3):   # Positive diagnal
        for col in range(cols-3):
            if position[row][col] == position[row+1][col+1] == position[row+2][col+2] == player:
                score += 80

    for row in range(3, rows):  # Negative diagnal
        for col in range(cols-3):
            if position[row][col] == position[row-1][col+1] == position[row-2][col+2] == player:
                score += 80
    
     # Check for preventing oppoenet's potential winning positions
    for row in range(rows): # Horizontal
        for col in range(cols-3):
            if((position[row][col] == position[row][col+1] == position[row][col+2] == opponent and position[row][col+3] == player) or 
            (position[row][col] == position[row][col+1] == position[row][col+3] == opponent and position[row][col+2] == player) or 
            (position[row][col] == position[row][col+2] == position[row][col+3] == opponent and position[row][col+1] == player) or 
            (position[row][col+1] == position[row][col+2] == position[row][col+3] == opponent and position[row][col] == player)):
                print("happend")
                score += 50
        
    for col in range(cols): # Vertical
        for row in range(rows-3):
            if((position[row][col] == position[row+1][col] == position[row+2][col] == opponent and position[row+3][col] == player) or 
            (position[row][col] == position[row+1][col] == position[row+3][col] == opponent and position[row+2][col] == player) or 
            (position[row][col] == position[row+2][col] == position[row+3][col] == opponent and position[row+1][col] == player) or 
            (position[row+1][col] == position[row+2][col] == position[row+3][col] == opponent and position[row][col] == player)):
                print("happend")
                score += 50

    for row in range(rows-3):   # Positive diagnal
        for col in range(cols-3):
            if((position[row][col] == position[row+1][col+1] == position[row+2][col+2] == opponent and position[row+3][col+3] == player) or 
            (position[row][col] == position[row+1][col+1] == position[row+3][col+3] == opponent and position[row+2][col+2] == player) or 
            (position[row][col] == position[row+2][col+2] == position[row+3][col+3] == opponent and position[row+1][col+1] == player) or
            (position[row+1][col+1] == position[row+2][col+2] == position[row+3][col+3] == opponent and position[row][col] == player)):
                print("happend")
                score += 50

    for row in range(3, rows):  # Negative diagnal
        for col in range(cols-3):
            if((position[row][col] == position[row-1][col+1] == position[row-2][col+2] == opponent and position[row-3][col+3] == player) or 
            (position[row][col] == position[row-1][col+1] == position[row-3][col+3] == opponent and position[row-2][col+2] == player) or 
            (position[row][col] == position[row-2][col+2] == position[row-3][col+3] == opponent and position[row-1][col+1] == player) or 
            (position[row-1][col+1] == position[row-2][col-2] == position[row-3][col+3] == opponent and position[row][col] == player)):
                print("happend")
                score += 50

    # Check for center control
    if position[rows-1][cols-4] == player:
        score += 70

    if player == "🔴":
        score = -score

    return score

### Convert row number and colomn number into board position  ###
def createSpacePicked(row, col): 
    n = possibleLetters[col]
    spacePicked = [n, int(row)]
    return spacePicked

### Generate leaf nodes ###
def move_gen(position, player): 
    successors = []
    new_position = copy.deepcopy(position)
    for row in range(rows):
        for col in range(cols):
            coordinate = coordinateParser(createSpacePicked(row, col))
            if isSpaceAvailable(new_position, coordinate) and gravityChecker(new_position, coordinate):
                new_position = modifyArray(new_position, coordinate, player)
                successors.append(new_position)
                new_position = copy.deepcopy(position)
    #print(successors)                 
    return successors

### Switch player ###
def opposite(player):   

    if player == "🔵":  
        return("🔴")  
    else:
        return("🔵")   

### Check if it reaches to the certain conditions ###
def deep_enough(position, depth):   

    if turnCounter % 2 == 0:    # Return true if it reaches to the depth limit for MAX player
        if depth == turnCounter + depthLimit1:   
            return True
        else:
            return False
    elif turnCounter+2 % 2 == 1:  # Return true if it reaches to the depth limit for MIN player
        if depth == turnCounter + depthLimit2:  
            return True
        else:
            return False
    elif checkForWinner(position, "🔵") or checkForWinner(position, "🔴"): # Return true if either player won
        return True
    else:   # False otherwise
        return False

### Minimax Alpha-Beta Pruing ###
## With EV1 
def minimax_ab_ev1(position, depth, player, useThresh, passThresh):
    #print()
    #print("depth ", depth)
    #print("position now:")
    #printGameBoard(position)
    if deep_enough(position, depth):
        value = static(position, player)
        path = None
        return value, path
        
    successors = move_gen(position, player)
    
    if not successors:
        value = static(position, player)
        path = None
        return value, path 

    bestPath= None
    for succ in successors:
        resultSucc = minimax_ab_ev1(succ, depth + 1, opposite(player), -passThresh, -useThresh)
        #print()
        #print("backed to depth ", depth)
        #print("position now:")
        #printGameBoard(position)
        new_value = -resultSucc[0]
        
        if player == "🔴":  # Revert the function when it's MIN turn
            new_value < passThresh
            passThresh = new_value
            bestPath = succ
        else:               # MAX turn
            if new_value > passThresh:
                passThresh = new_value
                bestPath = succ 
        
        if passThresh >= useThresh:
            return passThresh, bestPath

    return passThresh, bestPath

## With EV2 
def minimax_ab_ev2(position, depth, player, useThresh, passThresh): 

    if deep_enough(position, depth):
        value = static2(position, player)
        path = None
        return value, path
        
    successors = move_gen(position, player)
    
    if not successors:
        value = static2(position, player)
        path = None
        return value, path 

    bestPath= None
    for succ in successors:
        resultSucc = minimax_ab_ev2(succ, depth + 1, opposite(player), -passThresh, -useThresh)
        new_value = -resultSucc[0]
        
        if player == "🔴":  # Revert the function when it's MIN turn
            new_value < passThresh
            passThresh = new_value
            bestPath = succ
        else:               # MAX turn
            if new_value > passThresh:
                passThresh = new_value
                bestPath = succ 
        
        if passThresh >= useThresh:
            return passThresh, bestPath

    return passThresh, bestPath

############ Connect 4 ############
winner = False
valid = False
while (not winner):
    valid = False
    printGameBoard(gameBoard)
    if turnCounter % 2 == 0:
        print()
        print("TURN 🔵")

        result = minimax_ab_ev1(gameBoard, turnCounter, "🔵", 1000, -1000) # EV1
        #result = minimax_ab_ev2(gameBoard, turnCounter, "🔵", 1000, -1000) # EV2

        print(result[0])
        print(result[1])
        spacePicked = result[1]

        if spacePicked: # apply the result
            gameBoard = spacePicked
        else:   # Pick a random position when the path is empty
            while(not valid):
                spacePicked = random.choice(possibleLetters) + str(random.randint(0, 5))
                coordinate = coordinateParser(spacePicked)
                if isSpaceAvailable(gameBoard, coordinate) and gravityChecker(gameBoard, coordinate):
                    gameBoard = modifyArray(gameBoard, coordinate, "🔵")
                    valid = True
                    break
    
        winner = checkForWinner(gameBoard, "🔵")
        turnCounter += 1
    else:
        print()
        print("TURN 🔴")

        #result = minimax_ab_ev1(gameBoard, turnCounter, "🔴", -1000, 1000)  # EV1
        result = minimax_ab_ev2(gameBoard, turnCounter, "🔴", -1000, 1000) # EV2
        print(result[0])
        print(result[1])
        spacePicked = result[1]

        if spacePicked: # apply the result
            gameBoard = spacePicked
        else:   # Pick a random position when the path is empty
            while(not valid):
                spacePicked = random.choice(possibleLetters) + str(random.randint(0, 5))
                coordinate = coordinateParser(spacePicked)
                if isSpaceAvailable(gameBoard, coordinate) and gravityChecker(gameBoard, coordinate):
                    gameBoard = modifyArray(gameBoard, coordinate, "🔴")
                    valid = True
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







