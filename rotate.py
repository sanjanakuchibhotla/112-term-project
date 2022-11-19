def rotate90(L):
    rows, cols = len(L), len(L[0])
    rotated = [[0 for _ in range(rows)] for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            rotated[c][rows-1-r] = L[r][c]
    return rotated

def rotate180(L):
    rotated = rotate90(rotate90(L))
    return rotated
