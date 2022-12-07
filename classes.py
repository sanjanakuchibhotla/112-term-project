from PIL import Image
from PIL import ImageFilter
from floodfill import *
from cmu_112_graphics import *

# Button class
class Button():
    def __init__(self, name, center, currColor, changeColor):
        self.name = name
        self.w = 100
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
    
    # returns whether the button was clicked at the given x,y
    def clicked(self,mouseX,mouseY):
        x0,y0,x1,y1 = self.getCellBounds()
        return x0 <= mouseX <= x1 and y0 <= mouseY <= y1

# Slider class
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
    
    # resets the position of the slider
    def reset(self):
        self.setSliderPos(self.left)
    
    # returns whether the slider was clicked at the given x,y
    def clicked(self, x, y):
        return self.pos - self.r - 5 < x < self.pos + self.r + 5 and \
               self.c[1] - self.r - 5 < y < self.c[1] + self.r + 5

# Class of all layers (made up of SingleLayers)
class Layers():
    def __init__(self,layers):
        self.layers = layers
        self.hiddenLayers = dict()
        if len(self.layers) > 0:
            self.currentLayer = self.layers[-1]

    def getLayer(self, idx):
        return self.layers[idx]
    
    def addLayer(self, layer):
        self.layers.append(layer)

# SingleLayer class with image and hidden boolean as attributes
class SingleLayer():
    def __init__(self, im):
        self.im = im
        self.hidden = False
    
    def isHidden(self):
        return self.hidden
    
    def hide(self):
        self.hidden = True
    
    def show(self):
        self.hidden = False

# EditedImage class which makes up each layer
class EditedImage():
    def __init__(self, image, center):
        self.image = image
        self.width = image.size[0]
        self.height = image.size[1]

        self.ogCopy = self.makeCopy()

        self.cx = center[0]
        self.left = self.cx - self.width/2
        self.right = self.cx + self.width/2

        self.cy = center[1]
        self.top = self.cy - self.height/2
        self.bottom = self.cy + self.height/2

        self.edits = []
        self.centers = []

        self.filename = ''

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
        self.left = self.cx - self.width/2
        self.top = self.cy - self.height/2
        self.right = self.cx + self.width/2
        self.bottom = self.cy + self.height/2
    
    # translates the x value of a canvas coordinate to an image coordinate
    def xCanvasToImage(self, x):
        xImage = x - self.left
        return xImage
    
    # translates the y value of a canvas coordinate to an image coordinate
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
    
    def copyCenter(self):
        center = (self.cx, self.cy)
        return center
    
    def addEdit(self, edit):
        self.edits.append(edit)
    
    def addCenter(self, center):
        self.centers.append(center)
    
    def mergeImage(self, other):
        self.image.paste(other.image, (int(other.left), int(other.top)))
    
    # returns the pixel value of an image at a given canvas coordinate
    def getPixelAtCoord(self, x, y):
        imX = self.xCanvasToImage(x)
        imY = self.yCanvasToImage(y)
        pixel = self.image.getpixel((imX,imY))
        return pixel
    
    def gaussianBlur(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        center2 = self.copyCenter()
        self.addCenter(center2)
        self.image = self.image.filter(ImageFilter.GaussianBlur(amount))

    def sharpen(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        center2 = self.copyCenter()
        self.addCenter(center2)
        self.image = self.image.filter(ImageFilter.UnsharpMask(amount,50,3))
    
    def increaseRed(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        center2 = self.copyCenter()
        self.addCenter(center2)
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
        center2 = self.copyCenter()
        self.addCenter(center2)
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
        center2 = self.copyCenter()
        self.addCenter(center2)
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
        center2 = self.copyCenter()
        self.addCenter(center2)
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
        center2 = self.copyCenter()
        self.addCenter(center2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                minG = self.ogCopy.getpixel((r,c))[1]
                g2 = max(g1 - amount, minG)
                self.image.putpixel((r,c),(r1,g2,b1))
    
    def decreaseBlue(self, amount):
        im2 = self.makeCopy()
        self.addEdit(im2)
        center2 = self.copyCenter()
        self.addCenter(center2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                minB = self.ogCopy.getpixel((r,c))[2]
                b2 = max(b1 - amount, minB)
                self.image.putpixel((r,c),(r1,g1,b2))
    
    # grayscale conversion formula from https://tannerhelland.com/2011/10/01/grayscale-image-algorithm-vb6.html
    def makeBW(self):
        im2 = self.makeCopy()
        self.addEdit(im2)
        center2 = self.copyCenter()
        self.addCenter(center2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                gray = int(0.3*r1 + 0.59*g1 + 0.11*b1)
                self.image.putpixel((r,c),(gray,gray,gray))
    
    def fill(self, color, xClicked, yClicked, similarityVal):
        im2 = self.makeCopy()
        self.addEdit(im2)
        center2 = self.copyCenter()
        self.addCenter(center2)
        arr = self.getImArr()
        xClicked = int(self.xCanvasToImage(xClicked))
        yClicked = int(self.yCanvasToImage(yClicked))
        arr = floodfill(arr, xClicked, yClicked, color, similarityVal)
        rows = len(arr)
        cols = len(arr[0])
        for r in range(rows):
            for c in range(cols):
                (r1,g1,b1) = arr[r][c]
                self.image.putpixel((r,c),(r1,g1,b1))
    
    def flipH(self):
        im2 = self.makeCopy()
        self.addEdit(im2)
        center2 = self.copyCenter()
        self.addCenter(center2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        flipped = [[0 for _ in range(cols)] for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                flipped[rows-r-1][c] = arr[r][c]
        for x in range(rows):
            for y in range(cols):
                (r1,g1,b1) = flipped[x][y]
                self.image.putpixel((x,y),(r1,g1,b1))
    
    def flipV(self):
        im2 = self.makeCopy()
        self.addEdit(im2)
        center2 = self.copyCenter()
        self.addCenter(center2)
        arr = self.getImArr()
        rows = len(arr)
        cols = len(arr[0])
        flipped = [[0 for _ in range(cols)] for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                flipped[r][cols-c-1] = arr[r][c]
        for x in range(rows):
            for y in range(cols):
                (r1,g1,b1) = flipped[x][y]
                self.image.putpixel((x,y),(r1,g1,b1))

    def rotate(self):
        im2 = self.makeCopy()
        self.addEdit(im2)
        center2 = self.copyCenter()
        self.addCenter(center2)
        self.image = self.image.transpose(Image.ROTATE_90)
        copyH = self.height
        copyW = self.width
        self.width = copyH
        self.height = copyW
        copyCY = self.cy
        copyCX = self.cx
        self.cx = copyCY
        self.cy = copyCX
        self.left = self.cx - self.width/2
        self.right = self.cx + self.width/2
        self.top = self.cy - self.height/2
        self.bottom = self.cy + self.height/2