# ----------------------- #
# | SANJANA KUCHIBHOTLA | #
# | 15-112 TERM PROJECT | #
# ----------------------- #

from cmu_112_graphics import *
from classes import *
from floodfill import *
 
# SAMPLE IMAGES:
# dog image from google: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.petfinder.com%2Fdog-breeds%2F&psig=AOvVaw3Fm5UKfPEVjxaWVddBDKIY&ust=1669057075474000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCPDvvqS4vfsCFQAAAAAdAAAAABAD
# duck image from google: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.bestprintingonline.com%2Fresolution.htm&psig=AOvVaw0fu7WJ7dQ9LvwCfQCWN03z&ust=1670468964572000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCLCY84XE5vsCFQAAAAAdAAAAABAD
# square image from google: https://www.google.com/url?sa=i&url=https%3A%2F%2Fillustoon.com%2F%3Fid%3D7281&psig=AOvVaw0h_pkpfIxYlsMN0T5FgrDe&ust=1670469096949000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCOD81LrE5vsCFQAAAAAdAAAAABAD

# ############################################### #
# --------------- SPLASH SCREEN ----------------- #
# ############################################### #

def splashScreenMode_keyPressed(app, event):
    if event.key=='Space':
        app.mode = 'userMode'

def splashScreenMode_mousePressed(app, event):
    if clickedHere(app, event.x, event.y):
        app.mode = 'startMode'

def clickedHere(app, x, y):
    return app.width/3 < x < 2*app.width/3 and 5*app.height/8 < y < 6*app.height/8

def drawClickHere(app, canvas):
    canvas.create_rectangle(app.width/3-10, 5*app.height/8-10,
                            2*app.width/3+10, 6*app.height/8+10, outline='dark green', width=5)
    canvas.create_rectangle(app.width/3, 5*app.height/8,
                            2*app.width/3, 6*app.height/8, fill='black', activefill='dark green')
    canvas.create_text(app.width/2, 5.5*app.height/8, text='Click Here to Edit!',
                       font='Copperplate 30 bold', fill = 'SlateGray1')

def drawTitle(app, canvas):
    font = 'Copperplate 50 bold'
    canvas.create_rectangle(app.width/3, app.height/5,
                            2*app.width/3, 7*app.height/15,
                            outline='dark green', width=5)
    canvas.create_rectangle(app.width/3-15, app.height/5-15,
                            2*app.width/3+15, 7*app.height/15+15,
                            outline='dark green', width=5)
    canvas.create_text(7.5*app.width/15, 4.5*app.height/15, text='Image',
                       font=font, fill='SlateGray1')
    canvas.create_text(7.5*app.width/15, 5.5*app.height/15, text='Editor',
                       font=font, fill='SlateGray1')

def splashScreenMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='DarkOliveGreen4')
    canvas.create_rectangle(30, 30, app.width-30, app.height-30, 
                            outline='dark green', width=3)
    canvas.create_rectangle(app.margin, app.margin,
                            app.width-app.margin, app.height-app.margin,
                            outline='dark green',width=10)
    
    drawTitle(app, canvas)
    drawClickHere(app, canvas)

# ############################################ #
# --------------- START MODE ----------------- #
# ############################################ #

def drawOpenButton(app, canvas):
    cx, cy = app.width/2, app.height/2
    canvas.create_rectangle(cx - 100, cy - 30, cx + 100, cy + 30, fill='LightSteelBlue1',
                  activefill='LightSteelBlue3')
    canvas.create_text(cx, cy, text='Pick image', font='Courier 20 bold')

def openButtonClicked(app, x, y):
    cx, cy = app.width/2, app.height/2
    return cx - 100 <= x <= cx + 100 and cy - 30 <= y <= cy + 30

def startMode_mousePressed(app, event):
    if openButtonClicked(app, event.x, event.y):
        userInput = app.getUserInput('Open Image:')
        try:
            im = EditedImage(app.loadImage(userInput), (app.cxCanvas, app.cyCanvas))
            im.filename = userInput
            app.layers.addLayer(SingleLayer(im))
            app.mode = 'userMode'
        except:
            pass

def startMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='DarkOliveGreen4')
    canvas.create_rectangle(30, 30, app.width-30, app.height-30, 
                            outline='dark green', width=3)
    canvas.create_rectangle(app.margin, app.margin,
                            app.width-app.margin, app.height-app.margin,
                            outline='dark green',width=10)
    canvas.create_rectangle(app.width/2 - 110, app.height/2 - 40,
                            app.width/2 + 110, app.height/2 + 40,
                            fill=None, outline='dark green', width = 7)
    drawOpenButton(app, canvas)

# ########################################### #
# --------------- USER MODE ----------------- #
# ########################################### #

# initializing app variables:
def appStarted(app):
    app.margin = 10
    app.mode = 'splashScreenMode'
    app.cxCanvas = app.width/3
    app.cyCanvas = 5*app.height/14
    app.startingImage = Image.new(mode='RGB',size=(1,1),color=(255,255,255))
    app.im = EditedImage(app.startingImage, (app.cxCanvas, app.cyCanvas))
    app.layer1 = SingleLayer(app.im)
    app.imWidth = app.im.width
    app.imHeight = app.im.height

    # LAYERS
    app.layers = Layers([])
    if len(app.layers.layers) > 0:
        app.currentImage = app.layers.layers[len(app.layers.layers)-1].im
    app.changingLayer = False

    # STATES
    app.moving = False
    app.scaling = False
    app.isBW = False
    app.filling = False
    app.blurring = False
    app.sharpening = False
    app.picking = False

    app.pixelPicked = None

    # COLOR STATES
    app.increasingRed = False
    app.decreasingRed = False

    app.increasingGreen = False
    app.decreasingGreen = False

    app.increasingBlue = False
    app.decreasingBlue = False

    # SAVING
    app.finalImage = Image.new(mode='RGB',size=(int(2*app.width/3),int(5*app.height/7)),color=(255,255,255))

    # FLOODFILL
    app.fillcolor = (0,0,0)
    app.similarityVal = 40

    # USER MODE BUTTONS
    app.flipH = Button('flip horizontal', (5*app.width/6, app.height/8), 'dodgerblue', 'dodgerblue')
    app.flipV = Button('flip vertical', (5*app.width/6, 1.25*app.height/8), 'dodgerblue', 'dodgerblue')
    app.rotate = Button('rotate', (5*app.width/6, 1.5*app.height/8), 'dodgerblue', 'dodgerblue')
    app.save = Button('save', (18*app.width/19, app.margin + 20),'dodgerblue', 'dodgerblue')
    app.move = Button('move', (5*app.width/6, 0.5*app.height/8), 'dodgerblue', 'dodgerblue')
    app.bw = Button('b+w', (5*app.width/6,1.75*app.height/8), 'dodgerblue', 'dodgerblue')
    app.undo = Button('undo', (2*app.width/3 + 60, app.margin + 20), 'dodgerblue', 'dodgerblue')
    app.fill = Button('fill', (5*app.width/6, 22*app.height/36), 'dodgerblue', 'dodgerblue')
    app.sim = Button('similarity', (5*app.width/6, 26*app.height/36), 'slategray1', 'slategray1')
    app.colorPicker = Button('color picker', (5*app.width/6, 28*app.height/36), 'dodgerblue', 'dodgerblue')
    app.buttons = [app.flipH, app.flipV, app.rotate, app.move, app.bw, app.undo, app.save, app.fill, app.colorPicker]

    # USER MODE SLIDERS
    app.blur = Slider('blur', (5*app.width/6, 13*app.height/36), 'black')
    app.sharp = Slider('sharpen', (5*app.width/6, 12*app.height/36), 'black')
    app.red = Slider('red', (5*app.width/6, 17*app.height/36), 'red')
    app.green = Slider('green', (5*app.width/6, 18*app.height/36), 'green')
    app.blue = Slider('blue', (5*app.width/6, 19*app.height/36), 'blue')
    app.sliders = [app.blur, app.sharp, app.red, app.green, app.blue]

    # POSITIONS
    app.startRed = app.red.left
    app.endRed = app.red.getPos()

    app.startGreen = app.green.left
    app.endGreen = app.green.getPos()

    app.startBlue = app.blue.left
    app.endBlue = app.blue.getPos()

    app.startBlur = app.blur.left
    app.endBlur = app.blur.getPos()

    app.startSharp = app.sharp.left
    app.endSharp = app.sharp.getPos()

def userMode_keyPressed(app, event):
    if event.key == 'u':
        if len(app.currentImage.edits) > 0:
            last = len(app.currentImage.edits) - 1
            app.currentImage.image = app.currentImage.edits.pop(last)

def userMode_timerFired(app):
    if not app.changingLayer and len(app.layers.layers) > 0:
        app.currentImage = app.layers.layers[-1].im

def userMode_mousePressed(app, event):
    for button in app.buttons:
        if button.clicked(event.x, event.y):
            button.color = 'gray'
    
    # save the image with all the layers currently shown if the save button clicked
    if app.save.clicked(event.x,event.y):
        for layer in app.layers.layers:
            im = layer.im
            if not layer.isHidden():
                app.finalImage.paste(im.image, (int(im.cx-im.width/2), int(im.cy-im.height/2)))
        app.finalImage.save('final image.jpeg',format='jpeg')
    
    # flip the image horizontally if clicked
    if app.flipH.clicked(event.x,event.y):
        app.currentImage.flipH()
    
    # flip the image vertically if clicked
    if app.flipV.clicked(event.x,event.y):
        app.currentImage.flipV()
    
    # toggle the moving state and let the image be moved if the move button is clicked
    if app.move.clicked(event.x, event.y):
        app.moving = not app.moving
        if app.moving:
            app.move.name = 'moving...'
        else:
            app.move.name = 'move'
    
    # make the image black and white if the black and white button is clicked
    if app.bw.clicked(event.x, event.y):
        app.currentImage.makeBW()
    
    # rotate the image 90 degrees ccw if rotate is clicked
    if app.rotate.clicked(event.x, event.y):
        app.currentImage.rotate()
    
    # undo the last edit made if the undo button is clicked
    if app.undo.clicked(event.x, event.y) and len(app.currentImage.edits) > 0:
        last = len(app.currentImage.edits) - 1
        app.currentImage.image = app.currentImage.edits.pop(last)
    
    # fill the image if the filling state is true
    if app.filling:
        if (app.currentImage.right >= event.x >= app.currentImage.left and \
            app.currentImage.top <= event.y <= app.currentImage.bottom):
            app.currentImage.fill(app.fillcolor, event.x, event.y, app.similarityVal)
    
    if app.picking and app.currentImage.clicked(event.x,event.y):
        app.pixelPicked = app.currentImage.getPixelAtCoord(event.x,event.y)
    
    # add a layer if the add layer button is clicked
    if addLayerClicked(app, event.x, event.y):
        userInput = app.getUserInput('Add a layer:')
        try:
            im = app.loadImage(userInput)
            eIm = EditedImage(im, (app.cxCanvas, app.cyCanvas))
            app.layers.addLayer(SingleLayer(eIm))
            eIm.filename = userInput
            app.currentImage = app.layers.layers[-1].im
            for slider in app.sliders:
                slider.reset()
        except:
            pass
    
    # switch to layer clicked if a certain layer is clicked
    if layerClicked(app, event.x, event.y):
        idx = layerClicked(app, event.x, event.y)
        app.changingLayer = True
        app.currentImage = app.layers.layers[idx-1].im
        for slider in app.sliders:
            slider.reset()
    
    # toggle layer hiding if hide/show button clicked
    if hideClicked(app, event.x, event.y):
        idx = hideClicked(app, event.x, event.y)
        layer = app.layers.layers[idx-1]
        if layer.isHidden():
            layer.show()
        else:
            layer.hide()

def userMode_mouseReleased(app, event):
    for button in app.buttons:
        if button.clicked(event.x, event.y):
            button.color = button.activecolor
    
    # fills the area of the image clicked if fill is clicked
    if app.fill.clicked(event.x, event.y):
        app.filling = not app.filling
        if not app.filling:
            app.fill.name = 'fill'
        if app.filling:
            color = app.getUserInput('input rgb value in the form (r,g,b):')
            try:
                app.fill.name = 'filling...'
                if color[0] == '(':
                    color = color[1:]
                if color[-1] == ')':
                    color = color[:-1]
                rgbVals = color.split(',')
                r,g,b = int(rgbVals[0]),int(rgbVals[1]),int(rgbVals[2])
                while not ((0 <= r <= 255) and (0 <= g <= 255) and (0 <= b <= 255)):
                    color = app.getUserInput('input rgb value in the form (r,g,b):')
                    color = color[1:-1]
                    rgbVals = color.split(',')
                    r,g,b = int(rgbVals[0]),int(rgbVals[1]),int(rgbVals[2])
                app.fillcolor = (r,g,b)
            except:
                pass
    
    # allows user to input a similarity value to check how similar the pixels next to each other are
    # (i.e. a higher similarity value will allow the user to fill more of the area clicked)
    if app.filling and app.sim.clicked(event.x, event.y):
        val = app.getUserInput('enter value between 10 and 70:')
        try:
            val = int(val)
            while not (10 <= val <= 70):
                val = app.getUserInput('enter value between 10 and 70:')
                val = int(val)
            app.similarityVal = val
        except:
            pass
    
    # increases the red value if red slider moved right
    if app.increasingRed:
        dx = app.endRed - app.startRed
        amount = app.red.getColorAmount(dx)
        app.currentImage.increaseRed(int(amount))
        app.startRed = app.endRed
        app.increasingRed = False
    
    # decreases the red value if red slider moved left
    if app.decreasingRed:
        dx = app.endRed - app.startRed
        amount = abs(app.red.getColorAmount(dx))
        app.currentImage.decreaseRed(int(amount))
        app.startRed = app.endRed # update new start pos
        app.decreasingRed = False
    
    # increases the green value if green slider moved right
    if app.increasingGreen:
        dx = app.endGreen - app.startGreen
        amount = app.green.getColorAmount(dx)
        app.currentImage.increaseGreen(int(amount))
        app.startGreen = app.endGreen # update new start pos
        app.increasingGreen = False
    
    # decreases the green value if green slider moved left
    if app.decreasingGreen:
        dx = app.endGreen - app.startGreen
        amount = abs(app.green.getColorAmount(dx))
        app.currentImage.decreaseGreen(int(amount))
        app.startGreen = app.endGreen # update new start pos
        app.decreasingGreen = False
    
    # increases the blue value if blue slider moved right
    if app.increasingBlue:
        dx = app.endBlue - app.startBlue
        amount = app.blue.getColorAmount(dx)
        app.currentImage.increaseBlue(int(amount))
        app.startBlue = app.endBlue # update new start pos
        app.increasingBlue = False
    
    # decreases the blue value if blue slider moved left
    if app.decreasingBlue:
        dx = app.endBlue - app.startBlue
        amount = abs(app.blue.getColorAmount(dx))
        app.currentImage.decreaseBlue(int(amount))
        app.startBlue = app.endBlue # update new start pos
        app.decreasingBlue = False
    
    # blurs the image if the blur slider is moved to the right
    if app.blurring:
        dx = app.endBlur - app.startBlur
        amount = dx/5
        app.currentImage.gaussianBlur(amount)
        app.startBlur = app.endBlur
        app.blurring = False
    
    # sharpens the image if the sharpen slider is moved to the right
    if app.sharpening:
        dx = app.endSharp - app.startSharp
        amount = dx/10
        app.currentImage.sharpen(amount)
        app.startSharp = app.endSharp
        app.sharpening = False
    
    if app.colorPicker.clicked(event.x, event.y):
        app.picking = not app.picking
        if app.picking:
            app.colorPicker.name = 'picking...'
        else:
            app.colorPicker.name = 'color picker'

def userMode_mouseDragged(app, event):
    # move slider if clicked and dragged
    for slider in app.sliders:
        if slider.clicked(event.x, event.y) and slider.left < event.x < slider.right:
            slider.pos = event.x
    
    # recenter image if moved outside canvas bounds
    if app.moving and app.currentImage.clicked(event.x, event.y):
        if app.margin < app.currentImage.cx - app.currentImage.width/2 and \
           app.margin < app.currentImage.cy - app.currentImage.height/2 and \
           app.currentImage.cx + app.currentImage.width/2 < 2*app.width/3 and \
           app.currentImage.cy + app.currentImage.height/2 < 5*app.height/7:
           app.currentImage.changeCenter(event.x, event.y)
        else: # change center to canvas center if moved outside canvas bounds
            app.currentImage.cx = app.width/3
            app.currentImage.cy = 2.5*app.height/7

    # blur image if slider moved
    if app.blur.clicked(event.x, event.y):
        app.endBlur = event.x
        if app.endBlur > app.startBlur:
            app.blurring = True
    
    # sharpen image if slider moved
    if app.sharp.clicked(event.x, event.y):
        app.endSharp = event.x
        if app.endSharp > app.startSharp:
            app.sharpening = True

    # SLIDERS FOR COLORS
    if app.red.clicked(event.x,event.y):
        app.endRed = event.x
        if app.endRed > app.startRed: # moving right
            app.increasingRed = True
        else:
            app.decreasingRed = True

    if app.green.clicked(event.x,event.y):
        app.endGreen = event.x
        if app.endGreen > app.startGreen: # moving right
            app.increasingGreen = True
        else:
            app.decreasingGreen = True

    if app.blue.clicked(event.x,event.y):
        app.endBlue = event.x
        if app.endBlue > app.startBlue: # moving right
            app.increasingBlue = True
        else:
            app.decreasingBlue = True
    
    if app.picking and app.currentImage.clicked(event.x,event.y):
        app.pixelPicked = app.currentImage.getPixelAtCoord(event.x,event.y)

def drawBackground(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')

# draws the canvas area
def drawCanvas(app, canvas):
    canvas.create_rectangle(app.margin,app.margin,
                            2*app.width/3-app.margin,
                            app.height-app.margin,fill='bisque2')

# draws a button given a button object
def drawButton(canvas, button):
    name = button.getName()
    (x,y) = button.getCenter()
    bWidth, bHeight = button.w/2, button.h/2
    buttonLeft = x - bWidth
    buttonRight = x + bWidth
    color = button.getColor()
    r = bHeight
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
    canvas.create_rectangle(buttonLeft + r, y - r, buttonRight - r, y + r,
                            fill=color, outline=color)
    canvas.create_oval(cx1 - r, cy1 - r, cx1 + r, cy1 + r,
                       fill=color, outline=color)
    canvas.create_oval(cx3 - r, cy3 - r, cx3 + r, cy3 + r,
                       fill=color, outline=color)
    canvas.create_text(x, y, text=name, font='Copperplate 11 bold', fill='black')

# draws a slider given slider object
def drawSlider(canvas, slider):
    (x,y) = slider.getCenter()
    sWidth = slider.w
    pos = slider.getPos()
    r = slider.r
    color = slider.getColor()
    name = slider.getName()
    namelen = len(name)
    canvas.create_text(x - sWidth - namelen*7, y, text=name, font='Courier 15')
    canvas.create_line(x - sWidth, y,
                       x + sWidth, y,
                       fill = 'black', width = 3)
    canvas.create_oval(pos - r, y - r,
                       pos + r, y + r, fill = color)

# given r,g,b values, returns hex value (from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors)
def rgbString(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

# draws current fill color
def drawFillColor(app, canvas):
    (r,g,b) = app.fillcolor
    color = rgbString(r,g,b)
    pos = app.fill.getCenter()[1]
    canvas.create_rectangle(5*app.width/6 - 20, pos + 30,
                            5*app.width/6 + 20, pos + 70,
                            fill=color, outline='black')

# draws area with all the layers
def drawLayerArea(app, canvas):
    xleft = app.margin
    color = 'NavajoWhite3'
    r = 20
    canvas.create_rectangle(0,5*app.height/7-5,2*app.width/3,app.height,
                            fill='black')
    canvas.create_oval(xleft, 5*app.height/7, xleft + 2*r, 5*app.height/7 + 2*r,
                       fill=color, outline=color)
    canvas.create_oval(2*app.width/3-app.margin-2*r, 5*app.height/7,
                       2*app.width/3-app.margin, 5*app.height/7 + 2*r,
                       fill=color, outline=color)
    canvas.create_oval(xleft, app.height - app.margin - 2*r, xleft + 2*r, app.height - app.margin,
                       fill=color, outline=color)
    canvas.create_oval(2*app.width/3-app.margin-2*r, app.height-app.margin-2*r,
                       2*app.width/3-app.margin, app.height-app.margin,
                       fill=color, outline=color)
    canvas.create_rectangle(app.margin+r, 5*app.height/7,
                            2*app.width/3-app.margin-r, app.height-app.margin,
                            fill = color, outline=color)
    canvas.create_rectangle(app.margin, 5*app.height/7+r,
                            2*app.width/3-app.margin, app.height-app.margin-r,
                            fill = color,outline=color)
    canvas.create_text(app.width/3-app.margin,5*app.height/7+20,
                       text='Layers:', font = 'Helvetica 20 bold italic')

# draws the add layer button
def drawAddLayer(app, canvas):
    boxleftx = app.width/11 - app.margin
    boxlefty = 11*app.height/14
    size = 50
    cxBox = boxleftx + size/2
    cyBox = boxlefty + size/2
    canvas.create_rectangle(boxleftx, boxlefty,
                            boxleftx + size, boxlefty + size,fill='lightgray',
                            outline='black', width=3, activefill='gray')
    canvas.create_text(cxBox, cyBox, text='Add', font = 'Helvetica 20 bold')

# draws button for each layer in the layer area
def drawLayers(app, canvas):
    numLayers = len(app.layers.layers)
    xleftLayer1 = app.width/11 - app.margin + 70
    yLayer = 11*app.height/14
    for n in range(numLayers):
        x0 = 10*n + xleftLayer1 + n*50
        y0 = yLayer
        x1 = 10*n + xleftLayer1 + (n+1)*50
        y1 = yLayer + 50
        canvas.create_rectangle(x0, y0, x1, y1, fill='lightgray', outline='black', activefill='gray',width=3)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=f'Layer {n+1}', font = 'Helvetica 10 bold')
        # draws hide portion of button
        hideText = ''
        if app.layers.layers[n].isHidden():
            hideText = 'show'
        else:
            hideText = 'hide'
        hidey0 = y0 + 60
        hidey1 = y1 + 30
        canvas.create_rectangle(x0, hidey0, x1, hidey1, fill='azure', outline='black', activefill='gray',width=2)
        canvas.create_text((x0+x1)/2, (hidey0+hidey1)/2, text=hideText, font = 'Helvetica 10 bold')

# given a layer index, returns the bounds of the layer square
def getLayerBounds(app, idx):
    xleftLayer1 = app.width/11 - app.margin + 70
    yLayer = 11*app.height/14
    x0 = 10*idx + xleftLayer1 + idx*50
    y0 = yLayer
    x1 = 10*idx + xleftLayer1 + (idx+1)*50
    y1 = yLayer + 50
    return x0, y0, x1, y1

# returns which layer button was clicked, or False if none were clicked
def layerClicked(app, x, y):
    numLayers = len(app.layers.layers)
    for n in range(numLayers):
        x0, y0, x1, y1 = getLayerBounds(app, n)
        if x0 <= x <= x1 and y0 <= y <= y1:
            return n+1
    return False

# returns which layer was hidden if the hide button was clicked, or False if none were clicked
def hideClicked(app, x, y):
    numLayers = len(app.layers.layers)
    for n in range(numLayers):
        x0, y0, x1, y1 = getLayerBounds(app, n)
        y0 += 60
        y1 += 30
        if x0 <= x <= x1 and y0 <= y <= y1:
            return n+1
    return False

# returns true if the add layer button is clicked
def addLayerClicked(app, x, y):
    boxleftx = app.width/11 - app.margin
    boxlefty = 11*app.height/14
    size = 50
    return boxleftx <= x <= boxleftx + size and boxlefty <= y <= boxlefty + size

# draws the value of the pixel picked
def drawPixelPicked(app, canvas):
    pixel = str(app.pixelPicked)
    canvas.create_text(5*app.width/6, 29.5*app.height/36, text=pixel, font = 'Helvetica 20 bold')

# draws a box of the color that is picked on the canvas
def drawColorPicked(app, canvas):
    r = app.pixelPicked[0]
    g = app.pixelPicked[1]
    b = app.pixelPicked[2]
    color = rgbString(r,g,b)
    canvas.create_rectangle(5*app.width/6 - 20, 31.5*app.height/36 - 20,
                            5*app.width/6 + 20, 31.5*app.height/36 + 20,
                            fill=color)

# draws area with all tools shown
def drawToolArea(app, canvas):
    xleft = 2*app.width/3
    r = 20
    color = 'NavajoWhite3'
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
    drawFillColor(app, canvas)
    for button in app.buttons:
        drawButton(canvas, button)
    if app.filling:
        drawButton(canvas, app.sim)
    for slider in app.sliders:
        drawSlider(canvas, slider)
    for layer in app.layers.layers:
        im = layer.im
        hidden = layer.isHidden()
        if not hidden:
            im.drawImage(canvas)
    if app.pixelPicked != None:
        drawPixelPicked(app, canvas)
        drawColorPicked(app, canvas)

width = 1200
height = 800

runApp(width=width,height=height,title='Editor')