import math

# def floodfillOld(arr, startRow, startCol, new):
#     old = arr[startRow][startCol]
#     arr[startRow][startCol] = new
#     floodfillHelp(arr, startRow, startCol, old, new)
#     return arr

# def floodfillHelp(arr, startRow, startCol, old, new):
#     arr[startRow][startCol] = new
#     for drow,dcol in [(-1,0),(1,0),(0,-1),(0,1)]:
#         newRow = startRow + drow
#         newCol = startCol + dcol
#         if not onBoard(arr, newRow, newCol) or arr[newRow][newCol] == new:
#             continue
#         if similarPixelValue(arr[newRow][newCol], old):
#             floodfillHelp(arr, newRow, newCol, old, new)

def floodfill(arr, startRow, startCol, new, similarityVal):
    possible = []
    old = arr[startRow][startCol]
    seen = set()
    possible.append((startRow, startCol))
    seen.add((startRow, startCol))
    while len(possible) > 0:
        currValue = possible.pop(0)
        arr[currValue[0]][currValue[1]] = new
        for drow, dcol in [(-1,0),(1,0),(0,-1),(0,1)]:
            nextPos = (currValue[0] + drow, currValue[1] + dcol)
            if onBoard(arr, nextPos[0], nextPos[1]) and \
               similarPixelValue(arr[nextPos[0]][nextPos[1]], old, similarityVal) and \
               nextPos not in seen:
                seen.add(nextPos)
                possible.append(nextPos)
    return arr

def similarPixelValue(p1,p2,similarityVal):
    (r1,g1,b1) = p1
    (r2,g2,b2) = p2
    dR = r2 - r1
    dG = g2 - g1
    dB = b2 - b1
    similarity = math.sqrt(dR**2 + dG**2 + dB**2)
    return similarity < similarityVal

def onBoard(arr, row, col):
    rows = len(arr)
    cols = len(arr[0])
    return 0 <= row < rows and 0 <= col < cols