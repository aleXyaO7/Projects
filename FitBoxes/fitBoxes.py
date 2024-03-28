def fit(b1, b2):
    return b1 < b2

def determineBoxes(boxes):
    # Create the maxArray
    maxArray = [0 for i in range(len(boxes))]

    # Iterate through all boxes
    for pointer in range(len(maxArray)):
        # Find the maximum number of boxes if a box in question was the outside box
        determineMax(pointer, maxArray)

    return max(maxArray)

def determineMax(box, maxArray):
    # If we already know the maximum number of boxes that fit, return that
    if maxArray[box] > 0: return maxArray[box]

    # Find all boxes that fit inside of current box
    nbrs = []
    for i in range(len(maxArray)):
        if fit(i, box):
            nbrs.append(i)
    
    # If no boxes fit inside of current box, the maximum is 1
    if not nbrs:
        maxArray[box] = 1
        return 1
    
    nbrs_max = []
    for n in nbrs:
        # Not need to recalculate maximum for a sub-box if we already calculated it
        # Otherwise, recursion to calculate maximum for sub-box
        if maxArray[n] != 0:
            nbrs_max.append(maxArray[n])
        else:
            nbrs_max.append(determineMax(n, maxArray))
    
    # Add the maximum among sub-boxes + 1 to the maxArray and return it
    maxArray[box] = max(nbrs_max) + 1
    return maxArray[box]

print(determineBoxes([3,2,5,6,1,4,7]))