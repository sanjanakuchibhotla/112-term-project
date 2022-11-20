from PIL import Image
from cmu_112_graphics import *
from flip import *
from rotate import *
from blur import *
from filters import *

im = Image.open("dog.jpeg")
im2 = Image.new(mode='RGB', size=im.size)

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

def arrToIm(arr, im2):
    rows = len(arr)
    cols = len(arr[0])
    for x in range(rows):
        for y in range(cols):
            (r,g,b) = arr[x][y]
            im2.putpixel((x,y),(r,g,b))
    return im2

# --------------- SPLASH SCREEN -----------------

def splashScreenMode_keyPressed(app, event):
    if event.key=='Space':
        app.mode = 'userMode'

def splashScreenMode_mousePressed(app, event):
    if clickedHere(app, event.x, event.y):
        app.mode = 'userMode'

def clickedHere(app, x, y):
    return app.width/3 < x < 2*app.width/3 and 5*app.height/8 < y < 6*app.height/8

def drawClickHere(app, canvas):
    canvas.create_rectangle(app.width/3, 5*app.height/8,
                            2*app.width/3, 6*app.height/8, fill='black')
    canvas.create_text(app.width/2, 5.5*app.height/8, text='Click Here to Edit!',
                       font='Helvetica 30 bold', fill = 'white')

def drawTitle(app, canvas):
    font = 'Times 36 bold italic'
    canvas.create_rectangle(app.width/3, app.height/5,
                            2*app.width/3, 7*app.height/15,
                            outline='darkorchid2', width=5)
    canvas.create_text(7*app.width/15, 4*app.height/15, text='Image',
                       font=font, fill='black')
    canvas.create_text(8*app.width/15, 6*app.height/15, text='Editor',
                       font=font, fill='black')

def splashScreenMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='paleturquoise1')
    canvas.create_rectangle(app.margin, app.margin,
                            app.width-app.margin, app.height-app.margin,
                            outline='dodgerblue',width=10)
    drawTitle(app, canvas)
    drawClickHere(app, canvas)

# -----------------------------------------------

def appStarted(app):
    app.margin = 10
    app.mode = 'splashScreenMode'
    app.im = app.loadImage('dog.jpeg')
    app.imWidth = app.im.size[0]
    app.imHeight = app.im.size[1]
    app.im2 = Image.new(mode='RGB', size=(app.imWidth, app.imHeight))
    for x in range(app.im2.width):
        for y in range(app.im2.height):
            r,g,b = app.im.getpixel((x,y))
            app.im2.putpixel((x,y),(r,g,b))
    app.im2Width = app.im2.size[0]
    app.im2Height = app.im2.size[1]

def userMode_keyPressed(app, event):
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
        blurred = blur(imArr,5)
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

def userMode_mouseDragged(app, event):
    imArr = getImArr(app.im2)



# def drawButton(app, canvas, button):
#     name = button.getName()
#     (x,y) = button.getCenter()
#     bWidth, bHeight = button.width, button.height
#     canvas.create_rectangle(x - bWidth, y - bHeight,
#                             x + bWidth, y + bHeight,
#                             fill = 'gray')

def userMode_redrawAll(app, canvas):
    canvas.create_image(app.width/4, app.height/2, image=ImageTk.PhotoImage(app.im))
    canvas.create_image(3*app.width/4, app.height/2, image=ImageTk.PhotoImage(app.im2))

width = 1200
height = 1200

runApp(width=width,height=height)