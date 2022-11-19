def cropRight(L, x):
    rows = len(L)
    cols = len(L[0])
    cropped = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(len(L)):
        cropped[r] = L[r][:(cols-x)]
    return cropped
    
def cropBottom(L, y):
    cropped = L[:y]
    return cropped
    
def cropTop(L, y):
    cropped = L[y:]
    return cropped

def cropLeft(L, x):
    rows = len(L)
    cols = len(L[0])
    cropped = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        cropped[r] = L[r][x:]
    return cropped

def cropTopRight(L, x, y):
    rows = len(L)
    cols = len(L[0])
    cropped = [[0 for _ in range(cols-x)] for _ in range(rows-y)]
    for r in range(len(cropped)):
        for c in range(len(cropped[0])):
            cropped[r][c] = L[r+x][c+x-1]
    return cropped

def cropTopLeft(L, x, y):
    rows = len(L)
    cols = len(L[0])
    cropped = [[0 for _ in range(cols-x)] for _ in range(rows-y)]
    for r in range(len(cropped)):
        for c in range(len(cropped[0])):
            cropped[r][c] = L[r+x][c+x]
    return cropped

def cropBottomRight(self, x, y):
    self.L = self.cropBottom(y)
    self.L = self.cropRight(x)
    return self.L

def cropBottomLeft(self, x, y):
    self.L = self.cropBottom(y)
    self.L = self.cropLeft(x)
    return self.L

A = [[1,2,3],
     [4,5,6],
     [7,8,9]]