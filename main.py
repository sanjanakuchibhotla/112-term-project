# -----------------------
# | SANJANA KUCHIBHOTLA |
# | 15-112 TERM PROJECT |
# -----------------------

from PIL import Image
from PIL import ImageFilter
from cmu_112_graphics import *
from flip import *
from rotate import *
from classes import *
 
# dog image from google: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.petfinder.com%2Fdog-breeds%2F&psig=AOvVaw3Fm5UKfPEVjxaWVddBDKIY&ust=1669057075474000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCPDvvqS4vfsCFQAAAAAdAAAAABAD

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
                            2*app.width/3, 6*app.height/8, fill='black', activefill='dark green')
    canvas.create_text(app.width/2, 5.5*app.height/8, text='Click Here to Edit!',
                       font='Helvetica 30 bold', fill = 'white')

def drawTitle(app, canvas):
    font = 'Times 36 bold italic'
    canvas.create_rectangle(app.width/3, app.height/5,
                            2*app.width/3, 7*app.height/15,
                            outline='dark green', width=5)
    canvas.create_rectangle(app.width/3-15, app.height/5-15,
                            2*app.width/3+15, 7*app.height/15+15,
                            outline='dark green', width=5)
    canvas.create_text(7*app.width/15, 4*app.height/15, text='Image',
                       font=font, fill='white')
    canvas.create_text(8*app.width/15, 6*app.height/15, text='Editor',
                       font=font, fill='white')

def splashScreenMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='DarkOliveGreen4')
    canvas.create_rectangle(30, 30, app.width-30, app.height-30, 
                            outline='dark green', width=3)
    canvas.create_rectangle(app.margin, app.margin,
                            app.width-app.margin, app.height-app.margin,
                            outline='dark green',width=10)
    
    drawTitle(app, canvas)
    drawClickHere(app, canvas)

# ----------- USER MODE --------------

def appStarted(app):
    app.margin = 10
    app.mode = 'splashScreenMode'
    app.cxCanvas = app.width/3
    app.cyCanvas = 5*app.height/14
    app.im = EditedImage(app.loadImage('dog.jpeg'), (app.cxCanvas, app.cyCanvas))
    app.im2 = EditedImage(app.loadImage('image2.jpeg'), (app.cxCanvas+100, app.cyCanvas))
    app.imWidth = app.im.width
    app.imHeight = app.im.height

    # LAYERS
    app.im.mergeImage(app.im2)
    app.layer1 = SingleLayer(app.im)
    # app.layer1.addToLayer(app.im2)
    app.allLayers = Layers([app.layer1])
    app.currentLayer = app.allLayers.layers[0]
    app.currentImage = app.currentLayer.layer

    # STATES
    app.moving = False
    app.scaling = False
    app.isBW = False
    app.increasingRed = False
    app.increasingGreen = False
    app.increasingBlue = False

    # USER MODE BUTTONS
    app.flip = Button('flip', (5*app.width/6, app.height/8), 'dodgerblue')
    app.rotate = Button('rotate', (5*app.width/6, 1.5*app.height/8), 'dodgerblue')
    app.save = Button('save', (app.margin + 25, app.margin + 20),'dodgerblue')
    app.scale = Button('scale', (5*app.width/6, 0.75*app.height/8), 'dodgerblue')
    app.move = Button('move', (5*app.width/6, 0.5*app.height/8), 'dodgerblue')
    app.bw = Button('b+w', (5*app.width/6,1.75*app.height/8), 'dodgerblue')
    app.undo = Button('undo', (4.5*app.width/6,app.height/8), 'dodgerblue')
    app.buttons = [app.flip, app.rotate, app.scale, app.move, app.bw, app.undo, app.save]

    # USER MODE SLIDERS
    app.blur = Slider('blur', (5*app.width/6, 9*app.height/36), 'black')
    app.sharp = Slider('sharpen', (5*app.width/6, 15*app.height/36), 'black')
    app.red = Slider('red', (5*app.width/6, 11*app.height/36), 'red')
    app.green = Slider('green', (5*app.width/6, 12*app.height/36), 'green')
    app.blue = Slider('blue', (5*app.width/6, 13*app.height/36), 'blue')
    app.sliders = [app.blur, app.sharp, app.red, app.green, app.blue]

def userMode_keyPressed(app, event):
    if event.key == 'u':
        if len(app.im.edits) > 0:
            last = len(app.im.edits) - 1
            app.im.image = app.im.edits.pop(last)
    if event.key == 'r':
        pass
    if event.key == 's':
        pass

def userMode_mousePressed(app, event):
    if app.save.clicked(event.x,event.y):
        app.im.image.save('tpfile.jpeg',format='jpeg')

    for button in app.buttons:
        if button.clicked(event.x, event.y):
            button.color = 'gray'

    if app.flip.clicked(event.x,event.y):
        app.currentImage.flipH()

    if app.move.clicked(event.x, event.y):
        app.moving = not app.moving

    if app.bw.clicked(event.x, event.y):
        app.currentImage.makeBW()

    if app.rotate.clicked(event.x, event.y):
        app.currentImage.rotate()

    if app.undo.clicked(event.x, event.y) and len(app.currentImage.edits) > 0:
        last = len(app.currentImage.edits) - 1
        app.currentImage.image = app.currentImage.edits.pop(last)
    # if app.rotate.clicked:
    #     app.im.image = app.im.rotate90()

def userMode_mouseReleased(app, event):
    for button in app.buttons:
        if button.clicked(event.x, event.y):
            button.color = 'dodgerblue'
    
    if app.increasingRed:
        amount = (app.red.getPos() - app.red.left)/3
        app.currentImage.increaseRed(int(amount))
        app.increasingRed = False

    if app.increasingGreen:
        amount = (app.green.getPos() - app.green.left)/3
        app.currentImage.increaseGreen(int(amount))
        app.increasingGreen = False
    
    if app.increasingBlue:
        amount = (app.blue.getPos() - app.blue.left)/3
        app.currentImage.increaseBlue(int(amount))
        app.increasingBlue = False

def userMode_mouseDragged(app, event):
    # move slider if clicked and dragged
    for slider in app.sliders:
        if slider.clicked(event.x, event.y) and slider.left < event.x < slider.right:
            slider.pos = event.x
    
    # recenter image if moved outside canvas bounds
    if app.moving and app.im.clicked(event.x, event.y):
        if app.margin < app.im.cx - app.im.width/2 and \
           app.margin < app.im.cy - app.im.height/2 and \
           app.im.cx + app.im.width/2 < 2*app.width/3 and \
           app.im.cy + app.im.height/2 < 5*app.height/7:
           app.im.changeCenter(event.x, event.y)
        else:
            app.im.cx = app.width/3
            app.im.cy = 2.5*app.height/7
    
    # blur image if slider moved
    if app.blur.clicked(event.x, event.y):
        amount = (app.blur.getPos() - app.blur.left)/5
        app.currentImage.gaussianBlur(amount)
        # for _ in range(int(amount/2)):
        #     app.im.blur()
    
    # sharpen image if slider moved
    if app.sharp.clicked(event.x, event.y):
        amount = (app.sharp.getPos() - app.sharp.left)/10
        app.currentImage.sharpen(amount)

    # SLIDERS FOR COLORS
    if app.red.clicked(event.x,event.y) and app.red.movingRight(event.x):
        app.increasingRed = True

    if app.green.clicked(event.x,event.y):
        app.increasingGreen = True

    if app.blue.clicked(event.x,event.y):
        app.increasingBlue = True

def drawSingleLayer(singleLayer, canvas):
    singleLayer.drawLayer(canvas)

def drawBackground(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')

def drawCanvas(app, canvas):
    canvas.create_rectangle(app.margin,app.margin,
                            2*app.width/3-app.margin,
                            app.height-app.margin,fill='white')

def drawButton(canvas, button):
    name = button.getName()
    (x,y) = button.getCenter()
    bWidth, bHeight = button.w/2, button.h/2
    color = button.getColor()
    r = 10
    cx1, cy1 = x - bWidth + r, y - bHeight + r
    cx2, cy2 = x - bWidth + r, y + bHeight - r
    cx3, cy3 = x + bWidth - r, y - bHeight + r
    cx4, cy4 = x + bWidth - r, y + bHeight - r
    canvas.create_arc(cx1 - r, cy1 - r,
                      cx1 + r, cy1 + r,
                      outline = color, width = 1, style="arc",
                      start = 90, extent = 90)
    canvas.create_arc(cx2 - r, cy2 - r,
                      cx2 + r, cy2 + r,
                      outline = color, width = 1, style="arc",
                      start = -180, extent = 90)
    canvas.create_arc(cx3 - r, cy3 - r,
                      cx3 + r, cy3 + r,
                      outline = color, width = 1, style="arc",
                      start = 90, extent = -90)
    canvas.create_arc(cx4 - r, cy4 - r,
                      cx4 + r, cy4 + r,
                      outline = color, width = 1, style="arc",
                      start = 0, extent = -90)
    canvas.create_line(x - r, y - r, x + r, y - r, fill = color)
    canvas.create_line(x - r, y + r, x + r, y + r, fill = color)
    canvas.create_rectangle(x - r, y - r, x + r, y + r,
                            fill=color, outline=color)
    canvas.create_oval(cx1 - r, cy1 - r, cx1 + r, cy1 + r,
                       fill=color, outline=color)
    canvas.create_oval(cx3 - r, cy3 - r, cx3 + r, cy3 + r,
                       fill=color, outline=color)
    canvas.create_text(x, y, text=name, font='Arial 10 bold', fill='black')

def drawSlider(canvas, slider):
    (x,y) = slider.getCenter()
    sWidth = slider.w
    pos = slider.getPos()
    r = slider.r
    color = slider.getColor()
    name = slider.getName()
    namelen = len(name)
    canvas.create_text(x - sWidth - namelen*6, y, text=name, font='Helvetica 15')
    canvas.create_line(x - sWidth, y,
                       x + sWidth, y,
                       fill = 'black', width = 3)
    canvas.create_oval(pos - r, y - r,
                       pos + r, y + r, fill = color)

def drawLayerArea(app, canvas):
    canvas.create_rectangle(app.margin, 5*app.height/7,
                            2*app.width/3-app.margin, app.height-app.margin,
                            fill = 'lightgray')
    canvas.create_line(app.margin,5*app.height/7,
                       2*app.width/3-app.margin,5*app.height/7,
                       width=5)
    canvas.create_text(app.width/3-app.margin,5*app.height/7+20,
                       text='Layers:', font = 'Helvetica 20 bold italic')

def drawAddLayer(app, canvas):
    boxleftx = app.width/11 - app.margin
    boxlefty = 11*app.height/14
    size = 50
    cxBox = boxleftx + size/2
    cyBox = boxlefty + size/2
    plusW = 5*size/6
    plusH = size/3.5
    canvas.create_rectangle(boxleftx, boxlefty,
                            boxleftx + size, boxlefty + size,fill=None,
                            outline='black', width=3)
    # canvas.create_rectangle(cxBox - plusW/2, cyBox - plusH/2,
    #                         cxBox + plusW/2, cyBox + plusH/2,
    #                         fill = 'black')
    # canvas.create_rectangle(cxBox - plusH/2, cyBox - plusW/2,
    #                         cxBox + plusH/2, cyBox + plusW/2,
    #                         fill = 'black')
    canvas.create_text(cxBox, cyBox, text='Add', font = 'Helvetica 20 bold')

def drawLayers(app, canvas):
    numLayers = len(app.allLayers.layers)
    xrightAddLayer = app.width/11 - app.margin + 70
    yLayer = 11*app.height/14
    for n in range(numLayers):
        x0 = xrightAddLayer + n*50
        y0 = yLayer
        x1 = xrightAddLayer + (n+1)*50
        y1 = yLayer + 50
        canvas.create_rectangle(x0, y0, x1, y1, fill=None, outline='black', width=3)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=f'Layer {n+1}', font = 'Helvetica 10 bold')

def addLayerClicked(app, x, y):
    boxleftx = app.width/11 - app.margin
    boxlefty = 11*app.height/14
    size = 50
    return boxleftx <= x <= boxleftx + size and boxlefty <= y <= boxlefty + size

def drawToolArea(app, canvas):
    xleft = 2*app.width/3
    r = 20
    color = 'lightgray'
    canvas.create_oval(xleft, app.margin, xleft + 2*r, app.margin + 2*r,
                       fill=color, outline=color)
    canvas.create_oval(app.width-app.margin-2*r, app.margin, app.width - app.margin, app.margin + 2*r,
                       fill=color, outline=color)
    canvas.create_oval(xleft, app.height - app.margin - 2*r, xleft + 2*r, app.height - app.margin,
                       fill=color, outline=color)
    canvas.create_oval(app.width-app.margin-2*r, app.height-app.margin-2*r, app.width-app.margin, app.height-app.margin,
                       fill=color, outline=color)
    canvas.create_rectangle(xleft, app.margin + r, app.width-app.margin, app.height-app.margin-r,
                            fill=color, outline=color)
    canvas.create_rectangle(xleft + r, app.margin, app.width-app.margin-r, app.height-app.margin,
                            fill=color, outline=color)

def userMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawCanvas(app,canvas)
    drawLayerArea(app, canvas)
    drawAddLayer(app, canvas)
    drawLayers(app, canvas)
    drawToolArea(app, canvas)
    for button in app.buttons:
        drawButton(canvas, button)
    for slider in app.sliders:
        drawSlider(canvas, slider)
    for layer in app.allLayers.layers:
        drawSingleLayer(layer, canvas)

    
    #canvas.create_image(app.im.cx, app.im.cy, image=ImageTk.PhotoImage(app.im.image))

width = 1200
height = 800

runApp(width=width,height=height)