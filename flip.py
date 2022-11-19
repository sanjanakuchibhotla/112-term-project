def flipVertical(L):
    rows = len(L)
    cols = len(L[0])
    flipped = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            flipped[r][cols-c-1] = L[r][c]
    return flipped

def flipHorizontal(L):
    rows = len(L)
    cols = len(L[0])
    flipped = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            flipped[rows-r-1][c] = L[r][c]
    return flipped
