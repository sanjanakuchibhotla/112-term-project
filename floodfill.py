import math

from PIL import Image

im = Image.open('image3.jpeg')

def getImArr(im):
    im.convert('RGB')
    rows = im.width
    cols = im.height
    imArr = [[0 for _ in range(cols)] for _ in range(rows)]
    for x in range(im.width):
        for y in range(im.height):
            r,g,b = im.getpixel((x,y))
            imArr[x][y] = (r,g,b)
    return imArr

imArr = getImArr(im)

croppedIm = imArr[:3]

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
        if arr[newRow][newCol] == old:
            floodfillHelp(arr, newRow, newCol, old, new)

def similarPixelValue(p1,p2):
    (r1,g1,b1) = p1
    (r2,g2,b2) = p2
    dR = r2 - r1
    dG = g2 - g1
    dB = b2 - b1
    similarity = math.sqrt(dR**2 + dG**2 + dB**2)
    return similarity < 5

def onBoard(arr, row, col):
    rows = len(arr)
    cols = len(arr[0])
    return 0 <= row < rows and 0 <= col < cols

def isLegal(arr, startRow, startCol, old):
    rows = len(arr)
    cols = len(arr[0])
    for drow,dcol in [(0,-1),(1,0),(0,-1),(0,1)]:
        newRow = startRow+drow
        newCol = startCol+dcol
        if newRow >= rows or newRow < 0 or newCol >= cols or newCol < 0:
            continue
        if arr[newRow][newCol] == old:
            return True
    return False

A = [[0,0,0,1,2,3,4],
     [1,2,4,5,5,5,5],
     [2,3,4,5,5,6,7]]

def print2DList(L):
    for row in range(len(L)):
        print(L[row])

print2DList(A)
print()
print2DList(floodfill(A, 0, 1, 15))