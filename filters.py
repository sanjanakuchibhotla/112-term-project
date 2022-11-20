# RED FILTER

def redFilter(arr, level):
    rows = len(arr)
    cols = len(arr[0])
    filtered = [[0 for _ in range(cols)] for _ in range(rows)]
    for m in range(rows):
        for n in range(cols):
            _, g, b = arr[m][n]
            filtered[m][n] = (level,g,b)
    return filtered

# GREEN FILTER

def greenFilter(arr, level):
    rows = len(arr)
    cols = len(arr[0])
    filtered = [[0 for _ in range(cols)] for _ in range(rows)]
    for m in range(rows):
        for n in range(cols):
            r, _, b = arr[m][n]
            filtered[m][n] = (r,level,b)
    return filtered

# BLUE FILTER

def blueFilter(arr, level):
    rows = len(arr)
    cols = len(arr[0])
    filtered = [[0 for _ in range(cols)] for _ in range(rows)]
    for m in range(rows):
        for n in range(cols):
            r, g, _ = arr[m][n]
            filtered[m][n] = (r,g,level)
    return filtered

# BLACK AND WHITE FILTER

# grayscale conversion formula from https://tannerhelland.com/2011/10/01/grayscale-image-algorithm-vb6.html
def BWFilter(arr):
    rows = len(arr)
    cols = len(arr[0])
    filtered = [[0 for _ in range(cols)] for _ in range(rows)]
    for m in range(rows):
        for n in range(cols):
            r, g, b = arr[m][n]
            gray = int(0.3*r + 0.59*g + 0.11*b)
            filtered[m][n] = (gray,gray,gray)
    return filtered