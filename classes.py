from PIL import Image
from PIL import ImageFilter
from floodfill import *
from cmu_112_graphics import *

class Button():
    def __init__(self, name, center, currColor, changeColor):
        self.name = name
        self.w = 60
        self.h = 20
        self.c = center
        self.color = currColor
        self.activecolor = changeColor

    def getName(self):
        return self.name

    def getCenter(self):
        return self.c
    
    def getColor(self):
        return self.color
    
    def getCellBounds(self):
        (x,y) = self.c
        x0 = x - self.w/2
        y0 = y - self.h/2
        x1 = x + self.w/2
        y1 = y + self.h/2
        return x0,y0,x1,y1
    
    def clicked(self,mouseX,mouseY):
        x0,y0,x1,y1 = self.getCellBounds()
        return x0 <= mouseX <= x1 and y0 <= mouseY <= y1

    
class Slider():
    def __init__(self, name, center, color):
        self.name = name
        self.w = 50
        self.h = 1
        self.c = center
        self.color = color
        self.pos = self.c[0] - self.w
        self.r = self.h + 5
        self.left = self.c[0] - self.w
        self.right = self.c[0] + self.w
    
    def getName(self):
        return self.name
    
    def getCenter(self):
        return self.c
    
    def getPos(self):
        return self.pos

    def getColor(self):
        return self.color
    
    def getColorAmount(self,dx):
        amount = (dx/self.w)*255
        return amount
    
    def setSliderPos(self, newPos):
        self.pos = newPos
    
    def reset(self):
        self.pos = self.left
    
    def clicked(self, x, y):
        return self.pos - self.r - 5 < x < self.pos + self.r + 5 and \
               self.c[1] - self.r - 5 < y < self.c[1] + self.r + 5
    
    def movingRight(self, x):
        return x > self.getPos() - 1
    
    def movingLeft(self, x):
        return x < self.getPos()

class Layers():
    def __init__(self,layers):
        self.layers = layers
        self.hiddenLayers = dict()
        self.currentLayer = self.layers[-1]

    def getLayer(self, idx):
        return self.layers[idx]
    
    def addLayer(self, layer):
        self.layers.append(layer)
    
    def hideLayer(self, idx):
        layer = self.layers.pop(idx)
        self.hiddenLayers[idx] = layer
    
    def showLayer(self, idx):
        layer = self.hiddenLayers[idx]
        self.layers.insert(idx, layer)

# class SingleLayer():
#     def __init__(self, layer):
#         self.layer = layer
    
#     def getImage(self):
#         return self.layer
    
#     def addToLayer(self, newIm):
#         self.layer.mergeImage(newIm)
    
#     def drawLayer(self, canvas):
#         self.layer.drawImage(canvas)

class EditedImage():
    def __init__(self, image, center):
        self.image = image
        self.width = image.size[0]
        self.height = image.size[1]

        self.ogCopy = self.makeCopy()

        self.redAdded = 0
        self.greenAdded = 0
        self.blueAdded = 0

        self.cx = center[0]
        self.left = self.cx - self.width/2
        self.right = self.cx + self.width/2

        self.cy = center[1]
        self.top = self.cy - self.height/2
        self.bottom = self.cy + self.height/2

        self.edits = []

    def getImArr(self):
        im = self.image
        im.convert('RGB')
        rows = im.width
        cols = im.height
        imArr = [[0 for _ in range(cols)] for _ in range(rows)]
        for x in range(im.width):
            for y in range(im.height):
                r,g,b = im.getpixel((x,y))
                imArr[x][y] = (r,g,b)
        return imArr
    
    def drawImage(self, canvas):
        canvas.create_image(self.cx, self.cy, image=ImageTk.PhotoImage(self.image))
    
    def clicked(self, x, y):
        return self.cx - self.width/2 <= x <= self.cx + self.width/2 and \
               self.cy - self.height/2 <= y <= self.cy + self.height/2
    
    def changeCenter(self, x, y):
        im2 = self.makeCopy()
        self.addEdit(im2)
        self.cx = x
        self.cy = y
    
    def xCanvasToImage(self, x):
        xImage = x - self.left
        return xImage
    
    def yCanvasToImage(self, y):
        yImage = y - self.top
        return yImage
    
    def makeCopy(self):
        im2 = Image.new(mode='RGB', size=self.image.size)
        for x in range(self.width):
            for y in range(self.height):
                r,g,b = self.image.getpixel((x,y))
                im2.putpixel((x,y),(r,g,b))
        return im2
    
    def addEdit(self, edit):
        self.edits.append(edit)
    
    def mergeImage(self, other):
        self.image.paste(other.image, (int(other.left), int(other.top)))

    def blur(self):
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        drows = list(range(-3//2+1, 3//2+1))
        dcols = list(range(-3//2+1, 3//2+1))
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
                r = int(rSum/(3**2))
                g = int(gSum/(3**2))
                b = int(bSum/(3**2))
                arr[m][n] = (r, g, b)

        for x in range(rows):
            for y in range(cols):
                (r,g,b) = arr[x][y]
                self.image.putpixel((x,y),(r,g,b))
    
    def gaussianBlur(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        self.image = self.image.filter(ImageFilter.GaussianBlur(amount))

    def sharpen(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        self.image = self.image.filter(ImageFilter.UnsharpMask(amount,50,3))
    
    def increaseRed(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                r2 = min(r1 + amount, 255)
                self.image.putpixel((r,c),(r2,g1,b1))
    
    def increaseGreen(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                g2 = min(g1 + amount, 255)
                self.image.putpixel((r,c),(r1,g2,b1))
    
    def increaseBlue(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                b2 = min(b1 + amount, 255)
                self.image.putpixel((r,c),(r1,g1,b2))

    def decreaseRed(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                minR = self.ogCopy.getpixel((r,c))[0]
                r2 = max(r1 - amount, minR)
                self.image.putpixel((r,c),(r2,g1,b1))

    def decreaseGreen(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                g2 = max(g1 - amount, 0)
                self.image.putpixel((r,c),(r1,g2,b1))
    
    def decreaseBlue(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                b2 = max(b1 - amount, 0)
                self.image.putpixel((r,c),(r1,g1,b2))
    
    # grayscale conversion formula from https://tannerhelland.com/2011/10/01/grayscale-image-algorithm-vb6.html
    def makeBW(self):
        im2 = self.makeCopy()
        self.addEdit(im2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                gray = int(0.3*r1 + 0.59*g1 + 0.11*b1)
                self.image.putpixel((r,c),(gray,gray,gray))
    
    def fill(self, color, xClicked, yClicked):
        im2 = self.makeCopy()
        self.addEdit(im2)
        arr = self.getImArr()
        xClicked = int(self.xCanvasToImage(xClicked))
        yClicked = int(self.yCanvasToImage(yClicked))
        arr = floodfill(arr, xClicked, yClicked, color)
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                self.image.putpixel((r,c),(r1,g1,b1))
    
    def flipH(self):
        im2 = self.makeCopy()
        self.addEdit(im2)
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
    
    def flipV(self):
        im2 = self.makeCopy()
        self.addEdit(im2)
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
    
    # def rotate90(self):
    #     arr = self.getImArr()
    #     rows, cols = len(arr), len(arr[0])
    #     for r in range(rows):
    #         for c in range(cols):
    #             (r1,g1,b1) = arr[r][c]
    #             self.image.putpixel((r,c),(r1,g1,b1))
    def rotate(self):
        im2 = self.makeCopy()
        self.addEdit(im2)
        self.image = self.image.transpose(Image.ROTATE_90)