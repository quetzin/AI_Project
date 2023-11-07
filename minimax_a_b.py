depthLimit = 2
def STATIC(position, player):
    # evaluation function
    pass

def MOVE_GEN(position, player): 
    successors = []
    for row in range(6):
        for col in range(7):
            if position[row][col] == " ":
                position = modifyArray(position, player)
                successors.append(position)       
    return successors

def OPPOSITE(player): #may need to change depending on the system of the game
    if player == "max":
        player = "min"
    else:
        player = "max"
    pass

class SearchResult: #This function may not be needed
    def __init__(self, value, path):
        self.value = value
        self.path = path

def DEEP_ENOUGH(position, depth):
        return  depth == depthLimit   #return true if it reaches to the depth limit

def MINIMAX_AB(position, depth, player, passThresh, useThresh):
    if DEEP_ENOUGH(position, depth):
        value = STATIC(position, player)
        path = []
    else:
        successors = MOVE_GEN(position, player) #list of bourd pattern
        if not successors: #when it reaches to the terminal node
            value = STATIC(position, player)
            path = []

    value = float('-inf')
    for succ in successors: #go through each leaf node
        resultSucc = MINIMAX_AB(succ, depth + 1, OPPOSITE(player), -passThresh, -useThresh)
        newValue = -resultSucc.value

        if newValue > passThresh:
            passThresh = newValue
            path = resultSucc.path.copy()
            path.insert(0, succ)

        if passThresh >= useThresh:
            return SearchResult(passThresh, path)

        if newValue > value:
            value = newValue
            path = resultSucc.path.copy()
            path.insert(0, succ)

    return SearchResult(passThresh, path)