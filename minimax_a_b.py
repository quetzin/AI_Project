def STATIC(position, player):
    # evaluation function
    pass

def MOVE_GEN(position, player): 
    # generate leaf nodes
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
        return  position == depth   #return true if it reaches to the depth limit

def MINIMAX_AB(position, depth, player, passThresh, useThresh):
    if DEEP_ENOUGH(position, depth):
        return SearchResult(STATIC(position, player), []) 

    successors = MOVE_GEN(position, player)

    if not successors: #when it reaches to the terminal node
        return SearchResult(STATIC(position, player), [])

    value = float('-inf')
    path = []
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