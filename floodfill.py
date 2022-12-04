import math

def floodfill(arr, startRow, startCol, new):
    old = arr[startRow][startCol]
    arr[startRow][startCol] = new
    floodfillHelp(arr, startRow, startCol, old, new)
    return arr

def floodfillHelp(arr, startRow, startCol, old, new):
    arr[startRow][startCol] = new
    for drow,dcol in [(-1,0),(1,0),(0,-1),(0,1)]:
        newRow = startRow + drow
        newCol = startCol + dcol
        if not onBoard(arr, newRow, newCol) or arr[newRow][newCol] == new:
            continue
        if similarPixelValue(arr[newRow][newCol], old):
            floodfillHelp(arr, newRow, newCol, old, new)

def similarPixelValue(p1,p2):
    (r1,g1,b1) = p1
    (r2,g2,b2) = p2
    dR = r2 - r1
    dG = g2 - g1
    dB = b2 - b1
    similarity = math.sqrt(dR**2 + dG**2 + dB**2)
    return similarity < 30

def onBoard(arr, row, col):
    rows = len(arr)
    cols = len(arr[0])
    return 0 <= row < rows and 0 <= col < cols