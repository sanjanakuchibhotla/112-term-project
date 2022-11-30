# def floodfill(arr, startRow, startCol, new):
#     for idx in result

def floodfillHelp(arr, startRow, startCol, old, result):
    if not isLegal(arr, startRow, startCol, old):
        return result
    for drow,dcol in [(-1,0),(1,0),(0,-1),(0,1)]:
        newRow = startRow + drow
        newCol = startCol + dcol
        if 0 > newRow or newRow >= len(arr) or 0 > newCol or newCol >= len(arr[0]):
            continue
        if arr[newRow][newCol] == old:
            result.append((newRow,newCol))
            result += floodfillHelp(arr, newRow, newCol, old, result)
    return result

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
#print2DList(floodfill(A, 1, 5, 3))
print(isLegal(A, 2, 3, 5))