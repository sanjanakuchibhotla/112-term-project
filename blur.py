from PIL import Image
from cmu_112_graphics import *

def openIm(url):
    return Image.open(url)

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

def blur(arr, kernelSize):
    rows = len(arr)
    cols = len(arr[0])
    drows = list(range(-kernelSize//2+1, kernelSize//2+1))
    dcols = list(range(-kernelSize//2+1, kernelSize//2+1))
    for m in range(rows):
        for n in range(cols):
            rSum = 0
            gSum = 0
            bSum = 0
            for drow in drows:
                for dcol in dcols:
                    if m+drow < 0 or m+drow >= rows \
                    or n+dcol < 0 or n+dcol >= cols:
                        continue
                    (r1,g1,b1) = arr[m+drow][n+dcol]
                    rSum += r1
                    gSum += g1
                    bSum += b1
            r = int(rSum/(kernelSize**2))
            g = int(gSum/(kernelSize**2))
            b = int(bSum/(kernelSize**2))
            arr[m][n] = (r, g, b)
    return arr

def sharpen(arr, kernelSize):
    rows = len(arr)
    cols = len(arr[0])
    drows = list(range(-kernelSize//2+1, kernelSize//2+1))
    dcols = list(range(-kernelSize//2+1, kernelSize//2+1))
    for m in range(rows):
        for n in range(cols):
            rSub = 0
            gSub = 0
            bSub = 0
            for drow in drows:
                for dcol in dcols:
                    if (m+drow < 0 or m+drow >= rows or
                    n+dcol < 0 or n+dcol >= cols) or (drow == 0 and dcol == 0):
                        continue
                    (r1,g1,b1) = arr[m+drow][n+dcol]
                    rSub += .6*r1
                    gSub += .6*g1
                    bSub += .6*b1
            r = arr[m][n][0] - int(rSub/(kernelSize**2))
            g = arr[m][n][1] - int(gSub/(kernelSize**2))
            b = arr[m][n][2] - int(bSub/(kernelSize**2))
            arr[m][n] = (r, g, b)
    return arr