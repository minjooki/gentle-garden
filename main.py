from cmu_112_graphics import *
from plant import *
from terrain import *
from helper import *

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
    app.plantingMarginTop = 200
    app.plantingMarginSide = 50
    app.goPlantX0,app.goPlantX1,app.goPlantY0,app.goPlantY1 = (50,75,200,225)
    app.plantingX0,app.plantingX1,app.plantingY0,app.plantingY1 = (50,850,
                                                                    200,500)
    app.seedInv = [[{'apple seed':0},{'peach seed':0},{'lemon seed':0}],
                [{'strawberry seed':0},{'tomato seed':0},{'blackberry seed':0}]]
    
    app.appleSeeds = 5
    app.apples = 0
    app.peachSeeds = 5
    app.peaches = 0
    app.lemonSeeds = 5
    app.lemons = 0
    app.strawbSeeds = 5
    app.strawberries = 0
    app.tomatoSeeds = 5
    app.tomatoes = 0
    app.blackbSeeds = 5
    app.blackberries = 0

    app.isPlanting = False
    app.startSeed = False
    app.currSeed = 'apple' #CHANGE, temp demo only

    # dictionary mapping level to generated terrain
    app.terrain = makeTerrain(app)
    app.cellSize = 10
    

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
    
    # plant demo seed
    if (app.openPlanting and app.cx>app.goPlantX0 and app.cx<app.goPlantX1 and 
                            app.cy>app.goPlantY0 and app.cy<app.goPlantY1):
        app.isPlanting = True
        app.openPlanting = False
    if (app.isPlanting and app.cx>400 and app.cx<450 and 
                                app.cy>400 and app.cy<450):
        app.startSeed = True

def isStartSeed(app):
    if app.startSeed==True:
        newSeed = Plant(app.currSeed)


def redrawAll(app,canvas):
    drawTerrain(app,canvas)
    # drawChar(app,canvas)
    drawMenuHead(app,canvas)
    # drawPlots(app,canvas)

    if app.openInventory==True:
        drawInventory(app,canvas)
    elif app.openPlanting==True:
        drawPlanting(app,canvas)
    
    # demo tree plot
    canvas.create_rectangle(400,400,450,450,fill="white")
    

def drawTerrain(app,canvas):
    # pairs voronoi point to a color
    terrains = [0,1,2,3,4]
    colorPairs = []
    i = 0
    for seed in app.terrain:
        terrainType = terrains[i]
        i += 1
        colorPairs.append((seed,terrainType))
    
    for seedPair in colorPairs:
        terrainType = seedPair[1]
        seed = seedPair[0]
        color = getTerrainColor(app,terrainType)
        for (row,col) in app.terrain[seed]:
            x0 = col*app.cellSize
            y0 = row*app.cellSize + app.menuButtonHeight
            x1 = x0 + app.cellSize
            y1 = y0 + app.cellSize + app.menuButtonHeight
            canvas.create_rectangle(x0,y0,x1,y1,fill=color,outline='')

def getTerrainColor(app,terrainNum):
    if terrainNum==0:
        return rgbString(126,200,80)
    elif terrainNum==1 or terrainNum==3:
        return rgbString(155,103,60)
    else:
        return rgbString(131,105,83)



# def drawChar(app,canvas):
#     x0 = app.charX - app.charWidth/2
#     y0 = app.charY - app.charHeight/2
#     x1 = app.charX + app.charWidth/2
#     y1 = app.charY + app.charHeight/2
#     canvas.create_rectangle(x0,y0,x1,y1,fill="yellow")


def drawMenuHead(app,canvas):
    menuItems = ["Inventory","Plant","Water","Harvest"]
    for i in range(4):
        x0 = i*100
        x1 = x0 + app.menuButtonWidth
        y0 = 0
        y1 = app.menuButtonHeight
        canvas.create_rectangle(x0,y0,x1,y1)
        canvas.create_text(x0+app.menuButtonWidth/2,y1/2,text=menuItems[i])
    
    timeX0 = 700
    timeX1 = timeX0 + app.menuButtonWidth
    timeY0 = 0
    timeY1 = timeY0 + app.menuButtonHeight
    canvas.create_rectangle(timeX0,timeY0,timeX1,timeY1)
    canvas.create_text(timeX0+app.menuButtonWidth/2,
                            timeY1/2,text="12:00 PM")

    tempX0 = 800
    tempX1 = tempX0 + app.menuButtonWidth
    tempY0 = 0
    tempY1 = tempY0 + app.menuButtonHeight
    canvas.create_rectangle(tempX0,tempY0,tempX1,tempY1)
    canvas.create_text(tempX0+app.menuButtonWidth/2,tempY1/2,text="temp #")

def updateSeedInv(app):
    app.seedInv['apple seed'] = app.appleSeeds
    app.seedInv['peach seed'] = app.peachSeeds
    app.seedInv['lemon seed'] = app.lemonSeeds
    app.seedInv['strawberry seed'] = app.strawbSeeds
    app.seedInv['tomato seed'] = app.tomatoSeeds
    app.seedInv['blackberry seed'] = app.blackbSeeds


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
    sideSpace = ((app.plantingX1-app.plantingX0) - (app.plantingSlot*3))/4
    topSpace = ((app.plantingY1-app.plantingY0) - (app.plantingSlot*2))/3
    canvas.create_rectangle(app.plantingX0,app.plantingY0,
                            app.plantingX1,app.plantingY1,fill="white")
    canvas.create_text(app.plantingX1-app.closePlantingHeight/2,
                    app.plantingY0+app.closePlantingHeight/2,text="X")
    
    for j in range(2):
        for i in range(3):
            colX0 = (app.plantingX0 + app.plantingSlot*i + sideSpace*(i+1))
            colY0 = (app.plantingY0 + app.plantingSlot*j + topSpace*(j+1))
            canvas.create_rectangle(colX0,colY0,colX0+app.plantingSlot,
                colY0+app.plantingSlot)
            
            inv = app.seedInv[j][i]
            for seedName in inv:
                seedNum = inv[seedName]
            canvas.create_text(colX0+app.plantingSlot/2,
                colY0+app.plantingSlot/2,text=seedName+' '+str(seedNum))


runApp(width=900,height=700)