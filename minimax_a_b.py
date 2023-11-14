def STATIC(position, player):
    # evaluation function
    return value

def MOVE_GEN(position, player): 
    successors = []
    for row in range(rows):
        for col in range(cols):
            coordinate = createSpacePicked(row, col)
            if isSpaceAvailable(coordinate) and gravityChecker(coordinate):
                position = modifyArray(position, coordinate, player)
                successors.append(position)       
    return successors

def OPPOSITE(player):
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