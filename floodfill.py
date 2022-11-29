def floodfill(arr, startRow, startCol, new, old):
    for direction in [(-1,0),(1,0),(0,-1),(0,1)]:
        dcol = direction[0]
        drow = direction[1]
        newRow = startRow + drow
        newCol = startCol + dcol
        if arr[newRow][newCol] == old:
            arr[newRow][newCol] = new
            floodfill(arr, newRow, newCol, new, old)

    pass

def isLegal(board, newRow, newCol, old):
    return board[newRow][newCol] == old


[[0,0,0,1,2,3,4],
 [1,2,4,5,5,5,5],
 [2,3,4,5,5,6,7]]