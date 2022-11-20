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

def BWFilter(arr):
    rows = len(arr)
    cols = len(arr[0])
    filtered = [[0 for _ in range(cols)] for _ in range(rows)]
    for m in range(rows):
        for n in range(cols):
            r, g, b = arr[m][n]
            gray = int((r + g  + b)/3)
            filtered[m][n] = (gray,gray,gray)
    return filtered