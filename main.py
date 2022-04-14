from cmu_112_graphics import *
from plant import *
from terrain import *

def appStarted(app):
    app.width,app.height = 900,700

    app.openInventory = False
    app.closeInvHeight = 25

    app.invItems = [
                    [{'apple': 0},{'peach':1},{'lemon':3},{'strawberry':2},
                    {'orange':0},{'tomatoes':4}],

                    [{'apple seed':8},{'peach seeds':4},{'lemon seeds':8},
                    {'strawberry seeds':5},{'sample':0},{'sample':0}],

                    [{'sample':1},{'sample':1},{'sample':1},{'sample':1},
                    {'sample':1},{'sample':1}],

                    [{'sample':1},{'sample':1},{'sample':1},{'sample':1},
                    {'sample':1},{'sample':1}],
                    ]

    app.menuButtonHeight = 50
    app.menuButtonWidth = 100

    app.openPlanting = False
    app.closePlantingHeight = 25
    app.plantingSlot = 75

    # dictionary mapping level to generated terrain
    app.terrain = makeTerrain(app)
    app.cellSize = 25
    

def makeTerrain(app):
    # makes terrain to app.terrain
    gameHeight = app.height-app.menuButtonHeight
    voronoiPoints = voronoiSeeds(app.width,gameHeight)
    return getClosestSeeds(voronoiPoints,app.width,gameHeight)
    

def isLegalMove(app,dx,dy):
    tempX = app.charX + dx
    tempY = app.charY + dy
    if (tempX-(app.charWidth/2)<0 or tempX+(app.charWidth/2)>app.width or 
        tempY-(app.charHeight/2)<0 or tempY+(app.charHeight/2)>app.height):
        return False
    return True

def keyPressed(app,event):
    dy,dx = 0,0
    if event.key == 'Up':
        dy = -10
        if isLegalMove(app,dx,dy):
            app.charY -= 10
    elif event.key == 'Down':
        dy = +10
        if isLegalMove(app,dx,dy):
            app.charY += 10
    elif event.key == 'Right':
        dx = +10
        if isLegalMove(app,dx,dy):
            app.charX += 10
    elif event.key == 'Left':
        dx = -10
        if isLegalMove(app,dx,dy):
            app.charX -= 10

def mousePressed(app,event):
    app.cx,app.cy = event.x,event.y

    # open/close inventory
    if app.cx<=app.menuButtonWidth and app.cy<=app.menuButtonHeight:
        app.openInventory = True
        app.openPlanting = False
    elif (app.cx<=825+app.closeInvHeight and app.cx>=825 and 
                app.cy<=50+app.closeInvHeight and app.cy>=50):
        app.openInventory = False
    
    #open/close planting
    if (app.cx<=app.menuButtonWidth*2 and app.cx>app.menuButtonWidth and 
                                            app.cy<=app.menuButtonHeight):
        app.openPlanting = True
        app.openInventory = False
    elif (app.cx<=825+app.closePlantingHeight and app.cx>=825 and  
                    app.cy<=225 and app.cy>=200):
        app.openPlanting = False

def redrawAll(app,canvas):
    drawTerrain(app,canvas)
    # drawChar(app,canvas)
    drawMenuHead(app,canvas)
    # drawPlots(app,canvas)

    if app.openInventory==True:
        drawInventory(app,canvas)
    elif app.openPlanting==True:
        drawPlanting(app,canvas)

def drawTerrain(app,canvas):
    # pairs voronoi point to a color
    colors = ['red','blue','green','yellow','purple','pink','orange']
    colorPairs = []
    i = 0
    for seed in app.terrain:
        color = colors[i]
        i += 1
        colorPairs.append((seed,color))
    
    for seedPair in colorPairs:
        color = seedPair[1]
        seed = seedPair[0]
        for (row,col) in app.terrain[seed]:
            x0 = col*app.cellSize
            y0 = row*app.cellSize + app.menuButtonHeight
            x1 = x0 + app.cellSize
            y1 = y0 + app.cellSize + app.menuButtonHeight
            canvas.create_rectangle(x0,y0,x1,y1,fill=color)





# def drawChar(app,canvas):
#     x0 = app.charX - app.charWidth/2
#     y0 = app.charY - app.charHeight/2
#     x1 = app.charX + app.charWidth/2
#     y1 = app.charY + app.charHeight/2
#     canvas.create_rectangle(x0,y0,x1,y1,fill="yellow")


def drawMenuHead(app,canvas):
    buttonWidth = 100
    buttonHeight = 40
    menuItems = ["Inventory","Plant","Water","Harvest"]
    for i in range(4):
        x0 = i*100
        x1 = x0 + app.menuButtonWidth
        y0 = 0
        y1 = app.menuButtonHeight
        canvas.create_rectangle(x0,y0,x1,y1)
        canvas.create_text(x0+app.menuButtonWidth/2,y1/2,text=menuItems[i])
    
    timeX0 = 700
    timeX1 = timeX0 + buttonWidth
    timeY0 = 0
    timeY1 = timeY0 + buttonHeight
    canvas.create_rectangle(timeX0,timeY0,timeX1,timeY1)
    canvas.create_text(timeX0+buttonWidth/2,timeY1/2,text="12:00 PM")

    tempX0 = 800
    tempX1 = tempX0 + buttonWidth
    tempY0 = 0
    tempY1 = tempY0 + buttonHeight
    canvas.create_rectangle(tempX0,tempY0,tempX1,tempY1)
    canvas.create_text(tempX0+buttonWidth/2,tempY1/2,text="temp #")

def drawInventory(app,canvas):
    invMargin = 50
    canvas.create_rectangle(invMargin,invMargin,
                app.width-invMargin,app.height-invMargin,fill="white")

    colWidth = 75
    rowSpace = 250/3
    colSpace = 60
    for i in range(4):
        for j in range(6):
            colX0 = invMargin + 25 + colWidth*j + colSpace*j
            colY0 = invMargin + 25 + colWidth*i + rowSpace*i
            canvas.create_rectangle(colX0,colY0,
                            colX0+colWidth,colY0+colWidth)

            for item in app.invItems[i][j]:
                itemCount = app.invItems[i][j][item]
                canvas.create_text(colX0+colWidth/2,colY0+colWidth/2,
                                    text=item+" "+str(itemCount))
    
    canvas.create_text(825+app.closeInvHeight/2,50+app.closeInvHeight/2,
                            text='X')

def drawPlanting(app,canvas):
    marginTop = 200
    marginSide = 50
    sideSpace = (app.width-(2*marginSide))/4
    topSpace = (app.height-(2*marginTop))/3
    canvas.create_rectangle(marginSide,marginTop,
                        app.width-marginSide,app.height-marginTop,fill="white")
    canvas.create_text(850-app.closePlantingHeight/2,
                    200+app.closePlantingHeight/2,text="X")
    
    for j in range(1,3):
        for i in range(1,4):
            colX0 = marginSide + app.plantingSlot*i + sideSpace*(i-1)
            colY0 = marginTop + app.plantingSlot*(j-1) + topSpace*(j)
            canvas.create_rectangle(colX0,colY0,colX0+app.plantingSlot,
                colY0+app.plantingSlot)


runApp(width=900,height=700)