def keyPressed(app, event):
    if event.key == 'f':
        imArr = getImArr(app.im2)
        flipped = flipVertical(imArr)
        app.im2 = Image.new(mode='RGB', size=(app.im2Width, app.im2Height))
        app.im2 = arrToIm(flipped, app.im2)
    if event.key == 'g':
        imArr = getImArr(app.im2)
        flipped = flipHorizontal(imArr)
        app.im2 = Image.new(mode='RGB', size=(app.im2Width, app.im2Height))
        app.im2 = arrToIm(flipped, app.im2)
    if event.key == 'r':
        imArr = getImArr(app.im2)
        rotated = rotate90(imArr)
        app.im2 = Image.new(mode='RGB', size=(app.im2.size[1], app.im2.size[0]))
        app.im2 = arrToIm(rotated, app.im2)
    if event.key == 'b':
        imArr = getImArr(app.im2)
        blurred = blur(imArr,3)
        app.im2 = Image.new(mode='RGB', size=(app.im2.size[0], app.im2.size[1]))
        app.im2 = arrToIm(blurred, app.im2)
    if event.key == 's':
        imArr = getImArr(app.im2)
        sharpened = sharpen(imArr,3)
        app.im2 = Image.new(mode='RGB', size=(app.im2.size[0], app.im2.size[1]))
        app.im2 = arrToIm(sharpened, app.im2)
    if event.key == 'p':
        imArr = getImArr(app.im2)
        filtered = redFilter(imArr,200)
        app.im2 = Image.new(mode='RGB', size=(app.im2.size[0], app.im2.size[1]))
        app.im2 = arrToIm(filtered, app.im2)
    if event.key == 'j':
        imArr = getImArr(app.im2)
        filtered = greenFilter(imArr,200)
        app.im2 = Image.new(mode='RGB', size=(app.im2.size[0], app.im2.size[1]))
        app.im2 = arrToIm(filtered, app.im2)
    if event.key == 'k':
        imArr = getImArr(app.im2)
        filtered = blueFilter(imArr,200)
        app.im2 = Image.new(mode='RGB', size=(app.im2.size[0], app.im2.size[1]))
        app.im2 = arrToIm(filtered, app.im2)
    if event.key == 'o':
        imArr = getImArr(app.im2)
        filtered = BWFilter(imArr)
        app.im2 = Image.new(mode='RGB', size=(app.im2.size[0], app.im2.size[1]))
        app.im2 = arrToIm(filtered, app.im2)


# BLEND

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

def blend2Layers(layer0, layer1):
    rows = max(len(layer0),len(layer1))
    cols = max(len(layer0[0]),len(layer1[0]))
    blended = [[0 for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            (r1,g1,b1) = layer0[row][col]
            (r2,g2,b2) = layer1[row][col]
            newR = int((r1+r2)/2)
            newG = int((g1+g2)/2)
            newB = int((b1+b2)/2)
            blended[row][col] = (newR,newG,newB)
    return blended

def blendLayers(layerList):
    if len(layerList) == 0:
        return False
    if len(layerList) == 1:
        return layerList[0]
    if len(layerList) == 2:
        return blend2Layers(layerList[0],layerList[1])
    else:
        blend2Layers(layerList[0], blendLayers(layerList[1:]))