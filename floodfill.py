import math

# floodfills image based on similarity value between pixels
def floodfill(arr, startRow, startCol, new, similarityVal):
    possible = [] # list of next pixels
    old = arr[startRow][startCol]
    seen = set() # set of pixels already checked
    possible.append((startRow, startCol))
    seen.add((startRow, startCol))
    while len(possible) > 0: # loops while there are still remaining pixels
        currValue = possible.pop(0)
        arr[currValue[0]][currValue[1]] = new # changes pixel
        for drow, dcol in [(-1,0),(1,0),(0,-1),(0,1)]: # checks each possible direction
            nextRow = currValue[0] + drow
            nextCol = currValue[1] + dcol
            nextPos = (nextRow,nextCol)
            if onImage(arr, nextRow, nextCol) and \
               similarPixelValue(arr[nextRow][nextCol], old, similarityVal) and \
               nextPos not in seen: # checks if valid possible next pixel
                seen.add(nextPos)
                possible.append(nextPos)
    return arr

# function that takes in two pixels and returns if they are similar based on their similarity value
def similarPixelValue(p1,p2,similarityVal):
    (r1,g1,b1) = p1
    (r2,g2,b2) = p2
    dR = r2 - r1
    dG = g2 - g1
    dB = b2 - b1
    similarity = math.sqrt(dR**2 + dG**2 + dB**2)
    return similarity < similarityVal

# checks if the row and col are still in the range of pixels in the image
def onImage(arr, row, col):
    rows = len(arr)
    cols = len(arr[0])
    return 0 <= row < rows and 0 <= col < cols