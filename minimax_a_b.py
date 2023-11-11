def STATIC(position, player):
    # evaluation function
    pass

def MOVE_GEN(position, player): 
    successors = []
    for row in range(6):
        for col in range(7):
            if position[row][col] == " ":
                position = modifyArray(position, createSpacePicked(row, col), player)
                successors.append(position)       
    return successors

def OPPOSITE(player): #may need to change depending on the system of the game
    if player == "max":
        player = "min"
    else:
        player = "max"
    pass

def DEEP_ENOUGH(position, depth):
        return  depth == (depth+depthLimit)   #return true if it reaches to the depth limit

def MINIMAX_AB(position, depth, player, passThresh, useThresh):
    if DEEP_ENOUGH(position, depth):
        return value, path
    
    value = STATIC(position, player)
    path = []
    
    successors = MOVE_GEN(position, player)
    
    if not successors:
        return value, path
    
    for succ in successors:
        result_succ = MINIMAX_AB(succ, depth + 1, OPPOSITE(player), -passThresh, -useThresh)
        new_value = -result_succ[0]
        
        if new_value > passThresh:
            passThresh = new_value
            best_path = [succ] + result_succ[1]
        
        if passThresh >= useThresh:
            return passThresh, best_path

    return passThresh, best_path 