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

# def padArr(imArr, x, y):
#     rows = len(imArr)
#     cols = len(imArr[0])
#     extraRows = y - rows
#     extraCols = x - cols
#     addToTop 