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