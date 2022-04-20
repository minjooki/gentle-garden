from cmu_112_graphics import *
from plant import *
from terrain import *
from helper import *

# getBoardRowCol from cmu 112 animations website
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html 

def appStarted(app):
    app.timeElapsed = 0

    app.width,app.height = 900,700
    app.mode = 'startMode'

    app.isNewGame = True
    app.newX0,app.newY0,app.newWidth,app.newHeight = (350,325,200,75)
    app.oldX0,app.oldY0 = (350,450)

    app.charX,app.charY = (450,450)
    app.charWidth,app.charHeight = (10,15)

    app.openInventory = False
    app.closeInvHeight = 25
    app.closeInvX0 = 825
    app.closeInvY0 = 50

    app.invItems = [
                    [ ['apple', 0],['peach',1],['lemon',3],['strawberry',2],
                    ['orange',0],['tomatoes',4] ],

                    [ ['apple seed',8],['peach seeds',4],['lemon seeds',8],
                    ['strawberry seeds',5],['sample',0],['sample',0] ],

                    [ ['sample',1],['sample',1],['sample',1],['sample',1],
                    ['sample',1],['sample',1] ],

                    [ ['sample',1],['sample',1],['sample',1],['sample',1],
                    ['sample',1],['sample',1] ] 
                    ]
                    
    
    app.exitHeight = 50
    app.exitWidth = 50
    app.exitSaveX0,app.exitSaveY0 = (350,325)
    app.exitSaveWidth,app.exitSaveHeight = (200,75)
    app.exitCloseX0,app.exitCloseY0 = (350,450)
    app.exitCancelX0,app.exitCancelY0 = (400,575)
    app.exitCancelWidth,app.exitCancelHeight = (100,30)

    app.menuButtonHeight = 50
    app.menuButtonWidth = 100
    
    app.plantButtonX0 = 150
    app.plantButtonY0 = 0
    app.wateringX0 = 250
    app.wateringY0 = 0
    app.harvestingX0 = 350
    app.harvestingY0 = 0

    app.openPlanting = False
    app.closePlantingHeight = 25
    app.closePlantX0 = 825
    app.closePlantY0 = 200
    app.plantingSlot = 75
    app.plantingMarginTop = 200
    app.plantingMarginSide = 50
    app.plantingX0,app.plantingX1,app.plantingY0,app.plantingY1 = (50,850,
                                                                    200,500)
    app.unplantX0,app.unplantY0 = (750,475)
    app.unplantWidth = 100
    app.unplantHeight = 25
    app.removingPlants = False

    app.stopRemoveX0,app.stopRemoveY0 = (500,10)
    app.stopRemoveWidth = 90
    app.stopRemoveHeight = 30

    app.waterStartX0,app.waterStartY0 = (250,0)
    app.waterStartWidth,app.waterStartHeight = (100,50)
    app.waterStopX0,app.waterStopY0 = (500,10)
    app.waterStopWidth,app.waterStopHeight = (90,30)
    app.isWatering = False

    app.plantingSide = ((app.plantingX1-app.plantingX0)-(app.plantingSlot*3))/4
    app.plantingTop = ((app.plantingY1-app.plantingY0)-(app.plantingSlot*2))/3


    app.seedInv = [ [['apple seed',0],['peach seed',0],['lemon seed',0]],
                [['strawberry seed',0],['tomato seed',0],['blackberry seed',0]] ]
    
    app.treePoints = {'apple':[],'peach':[],'lemon':[]}
    app.plantPoints = {'strawb':[],'blackb':[],'tomato':[]}
    app.allSeedClasses = {}
    app.allPlantClasses = {}

    app.appleSeeds = 5
    app.apples = 0
    app.appleSeedInvX0 = (app.plantingX0+app.plantingSide)
    app.appleSeedInvY0 = (app.plantingY0+app.plantingTop)

    app.peachSeeds = 5
    app.peaches = 0
    app.peachSeedInvX0 = (app.plantingX0+app.plantingSlot+app.plantingSide*2)
    app.peachSeedInvY0 = (app.plantingY0+app.plantingTop)

    app.lemonSeeds = 5
    app.lemons = 0
    app.lemonSeedInvX0 = (app.plantingX0+app.plantingSlot*2+app.plantingSide*3)
    app.lemonSeedInvY0 = (app.plantingY0+app.plantingTop)

    app.strawbSeeds = 5
    app.strawberries = 0
    app.strawbSeedInvX0 = (app.plantingX0+app.plantingSide)
    app.strawbSeedInvY0 = (app.plantingY0+app.plantingSlot+app.plantingTop*2)

    app.tomatoSeeds = 5
    app.tomatoes = 0
    app.tomatoSeedInvX0 = (app.plantingX0+app.plantingSlot+app.plantingSide*2)
    app.tomatoSeedInvY0 = (app.plantingY0+app.plantingSlot+app.plantingTop*2)

    app.blackbSeeds = 5
    app.blackberries = 0
    app.blackbSeedInvX0 = (app.plantingX0+app.plantingSlot*2+app.plantingSide*3)
    app.blackbSeedInvY0 = (app.plantingY0+app.plantingSlot+app.plantingTop*2)

    app.isPlanting = False
    app.currSeed = None

    app.currTemp = 75

    # dictionary mapping level to generated terrain
    app.terrain = makeTerrain(app)
    app.cellSize = 10
    app.rows,app.cols = (app.height//app.cellSize,app.width//app.cellSize)
    app.board = [[0]*app.cols for row in range(app.rows)]
    updateBoard(app)
    updateSeedInv(app)

def timerFired(app):
    # TEMP if 10 seconds pass, move on
    app.timeElapsed += 10
    if (app.mode!='exitMode' and app.mode!='startMode' and app.mode!='nightMode'
         and app.timeElapsed >= 800):
        checkForGrowth(app)
        app.mode = 'nightMode'
        nightMode_reduceWater(app)
        app.timeElapsed = 0
    

def makeTerrain(app):
    # makes terrain to app.terrain
    gameHeight = app.height-app.menuButtonHeight
    voronoiPoints = voronoiSeeds(app.width,gameHeight)
    return getClosestSeeds(voronoiPoints,app.width,gameHeight)

def updateBoard(app):
    terrains = [0,1,2,3,4]
    colorPairs = []
    i = 0
    # seed point
    for seed in app.terrain:
        terrainType = terrains[i]
        i += 1
        # list of point and terrain type number tuples
        colorPairs.append((seed,terrainType))
    
    for seedPair in colorPairs:
        terrainType = seedPair[1]
        seed = seedPair[0]
        for (row,col) in app.terrain[seed]:
            app.board[row][col] = terrainType
  

def isLegalMove(app,dx,dy):
    # is moving character legal
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

    # use enter key to pick seed and start planting
    if app.openPlanting and app.currSeed!=None and event.key=='Enter':
        app.openPlanting = False
        app.isPlanting = True


def mousePressed(app,event):
    app.cx,app.cy = event.x,event.y

    # exit game
    if clickedOn(app.cx,app.cy,0,0,app.exitWidth,app.exitHeight):
        app.mode = 'exitMode'

    # open/close inventory
    elif clickedOn(app.cx,app.cy,50,0,50+app.menuButtonWidth,
        app.menuButtonHeight):
        app.openInventory = True
        app.openPlanting = False
        app.isPlanting = False
    elif (app.openInventory) and clickedOn(app.cx,app.cy,app.closeInvX0,
        app.closeInvY0,app.closeInvHeight,app.closeInvHeight):
        app.openInventory = False
    
    #open/close planting
    if clickedOn(app.cx,app.cy,app.plantButtonX0,app.plantButtonY0,
                                app.menuButtonWidth,app.menuButtonHeight):
        app.openPlanting = True
        app.openInventory = False
        app.isPlanting = False
    elif (app.openPlanting) and clickedOn(app.cx,app.cy,app.closePlantX0,
        app.closePlantY0,app.closePlantingHeight,app.closePlantingHeight):
        app.openPlanting = False
    
    if (app.openPlanting):
        # pick the seed to plant only if there are seeds
        if clickedOn(app.cx,app.cy,app.appleSeedInvX0,app.appleSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'apple'
            if app.appleSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.peachSeedInvX0,app.peachSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'peach'
            if app.peachSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.lemonSeedInvX0,app.lemonSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'lemon'
            if app.lemonSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.strawbSeedInvX0,app.strawbSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'strawb'
            if app.strawbSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.tomatoSeedInvX0,app.tomatoSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'tomato'
            if app.tomatoSeeds < 1:
                app.currSeed = None
        elif clickedOn(app.cx,app.cy,app.blackbSeedInvX0,app.blackbSeedInvY0,
            app.plantingSlot,app.plantingSlot):
            app.currSeed = 'blackb'
            if app.blackbSeeds < 1:
                app.currSeed = None
        
        # start removing plants
        if clickedOn(app.cx,app.cy,app.unplantX0,app.unplantY0,
            app.unplantWidth,app.unplantHeight):
            app.removingPlants = True
            app.openPlanting = False
    
    if app.isPlanting and app.openPlanting==False:
        # planting seed 
        (row,col) = getBoardRowCol(app,app.cx,app.cy)

        # if tree and in the right terrain
        if (app.currSeed in ['apple','lemon','peach'] and (app.board[row][col]==1
                 or app.board[row][col]==3)):
            if isLegalTree(app,row,col,5,1,3):
                treeOnBoard(app,row,col,5)
                app.treePoints[app.currSeed].append((row+2,col))
                startSeed(app,row+2,col)
                app.isPlanting = False

        elif (app.currSeed in ['strawb','blackb','tomato'] and 
                (app.board[row][col]==2 or app.board[row][col]==4)):
            if isLegalPlant(app,row,col,6,2,4):
                plantOnBoard(app,row,col,6)
                app.plantPoints[app.currSeed].append((row+1,col))
                startSeed(app,row+1,col)
                app.isPlanting = False
        if app.isPlanting==False:
            updateSeeds(app)

    if app.openPlanting==False and app.removingPlants:
        # remove plants
        (row,col) = getBoardRowCol(app,app.cx,app.cy)

        if app.board[row][col] in (50,51,52,53,54,55,56):
            removeTree(app,row,col)
        elif app.board[row][col] in (30,31,32,33,34,35,36):
            removePlant(app,row,col)
        elif clickedOn(app.cx,app.cy,app.stopRemoveX0,app.stopRemoveY0,
            app.stopRemoveWidth,app.stopRemoveHeight):
            app.removingPlants = False

    if (app.isPlanting==False and app.removingPlants==False and 
        clickedOn(app.cx,app.cy,app.waterStartX0,app.waterStartY0,
            app.waterStartWidth,app.waterStartHeight)):
        app.isWatering = True
        app.openPlanting = False
        app.currSeed = None
        app.isPlanting = False
        app.openInventory = None
    
    elif clickedOn(app.cx,app.cy,app.waterStopX0,app.waterStopY0,
        app.waterStopWidth,app.waterStopHeight) and app.isWatering:
        app.isWatering = False
    
    if app.isWatering:
        # update class and water
        (row,col) = getBoardRowCol(app,app.cx,app.cy)
        changeWaterLevel(app,row,col,True)

def changeWaterLevel(app,row,col,watering):
    # change water and change soil
        for treeType in app.treePoints:
            coord = (row,col)
            if (coord in app.treePoints[treeType] and 
                coord in app.allSeedClasses):
                seed = app.allSeedClasses[coord]
                if watering:
                    seed.waterPlant()
                status = getWaterState(seed)
                changeSoilColor(app,row,col,'tree',status)
            elif (coord in app.treePoints[treeType] and 
                coord in app.allPlantClasses):
                plant = app.allPlantClasses[coord]
                if watering:
                    plant.waterPlant()
                status = getWaterState(plant)
                changeSoilColor(app,row,col,'tree',status)
        
        for plantType in app.plantPoints:
            coord = (row,col)
            if (coord in app.plantPoints[plantType] and 
                coord in app.allSeedClasses):
                seed = app.allSeedClasses[coord]
                if watering:
                    seed.waterPlant()
                status = getWaterState(seed)
                changeSoilColor(app,row,col,'plant',status)
            elif (coord in app.plantPoints[plantType] and 
                coord in app.allPlantClasses):
                plant = app.allPlantClasses[coord]
                if watering:
                    plant.waterPlant()
                status = getWaterState(plant)
                changeSoilColor(app,row,col,'plant',status)

def getWaterState(plant):
    if plant.isOverwatered:
        return 'overwatered'
    elif plant.isDry:
        return 'dry'
    else:
        return

def changeSoilColor(app,row,col,type,status):
    # change soil color once watered
    if type=='tree':
        for drow in range(-4,+1):
            for dcol in range(-2,3):
                newRow = row + drow
                newCol = col + dcol
                if newCol!=col or newRow!=row:
                    if status=='overwatered':
                        app.board[newRow][newCol] = 101
                    elif status=='dry':
                        app.board[newRow][newCol] = 99
                    else:
                        app.board[newRow][newCol] = 100
    elif type=='plant':
        for drow in range(-2,+1):
            for dcol in range(-1,2):
                newRow = row + drow
                newCol = col + dcol
                if newCol!=col or newRow!=row:
                    if newCol!=col or newRow!=row:
                        if status=='overwatered':
                            app.board[newRow][newCol] = 101
                        elif status=='dry':
                            app.board[newRow][newCol] = 99
                        else:
                            app.board[newRow][newCol] = 100


def removeTree(app,row,col):
    for drow in range(-5,1):
        for dcol in range(-2,4):
            newRow = row + drow
            newCol = col + dcol
            app.board[newRow][newCol] = 1
    for treeType in app.treePoints:
        if (row,col) in app.treePoints[treeType]:
            app.treePoints[treeType].remove((row,col))

def removePlant(app,row,col):
    for drow in range(-2,1):
        for dcol in range(-1,3):
            newRow = row + drow
            newCol = col + dcol
            app.board[newRow][newCol] = 2
    for plantType in app.plantPoints:
        if (row,col) in app.plantPoints[plantType]:
            app.plantPoints[plantType].remove((row,col))
    if (row,col) in app.allSeedClasses:
        app.allSeedClasses.remove((row,col))
    elif (row,col) in app.allPlantClasses:
        app.allPlantClasses.remove((row,col))


def updateSeedInv(app):
    # update seed inventory for display
    app.seedInv[0][0][1]= app.appleSeeds
    app.seedInv[0][1][1] = app.peachSeeds
    app.seedInv[0][2][1] = app.lemonSeeds
    app.seedInv[1][0][1] = app.strawbSeeds
    app.seedInv[1][1][1] = app.tomatoSeeds
    app.seedInv[1][2][1] = app.blackbSeeds

def updateSeeds(app):
    # update seed inventory
    if app.currSeed=='apple':
        app.appleSeeds -= 1
    elif app.currSeed =='peach':
        app.peachSeeds -= 1
    elif app.currSeed == 'lemon':
        app.lemonSeeds -= 1
    elif app.currSeed == 'strawb':
        app.strawbSeeds -= 1
    elif app.currSeed == 'tomato':
        app.tomatoSeeds -= 1
    elif app.currSeed == 'blackb':
        app.blackbSeeds -= 1
    app.currSeed = None
    updateSeedInv(app)

def treeOnBoard(app,row,col,plantType):
    # update board and plant tree
    for drow in (-2,-1,0,+1,+2):
        for dcol in (-2,-1,0,+1,+2):
            newRow = row + drow
            newCol = col + dcol
            if ((drow == +2) and (dcol==0)):
                app.board[newRow][newCol] = 50
            else:
                app.board[newRow][newCol] = plantType

def plantOnBoard(app,row,col,plantType):
    # update board and plant plant
    for drow in (-1,0,+1):
        for dcol in (-1,0,+1):
            newRow = row + drow
            newCol = col + dcol
            if ((drow == +1) and (dcol==0)):
                app.board[newRow][newCol] = 30
            else:
                app.board[newRow][newCol] = plantType

def isLegalTree(app,row,col,plantType,terrainType1,terrainType2):
    # plots cannot overlap and must be spaced out
    for drow in (list(range(-8,8))):
        for dcol in (list(range(-5,5))):
            newRow = row + drow
            newCol = col + dcol
            if (newRow<2 or newCol<2 or newRow>(app.rows-3) or 
                                            newCol>(app.cols-3)):
                return False
            elif ((app.board[newRow][newCol]==plantType or 
                (app.board[newRow][newCol]!=terrainType1 and 
                app.board[newRow][newCol]!=terrainType2))):
                return False

    return True

def isLegalPlant(app,row,col,plantType,terrainType1,terrainType2):
    # plots cannot overlap and must be spaced out
    for drow in (list(range(-6,6))):
        for dcol in (list(range(-4,4))):
            newRow = row + drow
            newCol = col + dcol
            if (newRow<2 or newCol<2 or newRow>(app.rows-3) or 
                                            newCol>(app.cols-3)):
                return False
            elif ((app.board[newRow][newCol]==plantType or 
                (app.board[newRow][newCol]!=terrainType1 and 
                app.board[newRow][newCol]!=terrainType2))):
                return False

    return True


def getBoardRowCol(app,x,y):
    row = int((y - app.menuButtonHeight) / app.cellSize)
    col = int(x / app.cellSize)
    return (row,col)


def startSeed(app,row,col):
    coord = (row,col)
    newSeed = NewPlant(coord,app.currSeed)
    app.allSeedClasses[coord] = newSeed
    app.currSeed = None



def checkForGrowth(app):
    print('in')
    for coord in app.allPlantClasses:
        # check all plants
        plant = app.allPlantClasses[coord]
        plant.checkTemp(app.currTemp)
        plant.growPlant()
        plant.checkGrowth(plant.type)
        (row,col) = plant.coord
        if plant.stage == 2:
            # if small plant/tree
            if plant.type in ['apple','peach','lemon']:
                app.board[row][col] = 51
            else:
                app.board[row][col] = 61
        elif plant.stage == 3:
            # if med plant/tree
            if plant.type in ['apple','peach','lemon']:
                app.board[row][col] = 52
            else:
                app.board[row][col] = 62
        elif plant.stage == 4:
            # if mature plant/tree
            if plant.type in ['apple','peach','lemon']:
                app.board[row][col] = 53
            else:
                app.board[row][col] = 63
        elif plant.stage == 5:
            # flowering
            if plant.type in ['apple','peach','lemon']:
                app.board[row][col] = 54
            else:
                app.board[row][col] = 64
        elif plant.stage == 6:
            # unripe
            if plant.type in ['apple','peach','lemon']:
                app.board[row][col] = 55
            else:
                app.board[row][col] = 65
        elif plant.stage == 7:
            # fruiting
            if plant.type in ['apple','peach','lemon']:
                app.board[row][col] = 56
            else:
                app.board[row][col] = 66

    removing = []
    for coord in app.allSeedClasses:
        # check all seeds, upgrade to plant if needed
        plant = app.allSeedClasses[coord]
        # just a seed
        plant.checkTemp(app.currTemp) # updates class temps
        plant.growPlant() # updates plant growth
        print(plant.type)
        if plant.growth>=4:
            sprout = Seed(coord,plant.type)
            removing.append((coord))
            app.allPlantClasses[coord] = sprout
    if removing != []:
        for coord in removing:
            app.allSeedClasses.pop(coord)
        removing = []



####################
#### START MODE ####
####################

def startMode_redrawAll(app,canvas):
    drawStartScreen(app,canvas)
    if app.isNewGame:
        pass

def drawStartScreen(app,canvas):
    x0,y0,x1,y1 = (0,0,app.width,app.height)
    canvas.create_rectangle(x0,y0,x1,y1,fill='black')
    titleX0 = 150
    titleY0 = 100
    titleWidth = 600
    titleHeight = 150
    canvas.create_rectangle(titleX0,titleY0,titleX0+titleWidth,
                            titleY0+titleHeight)
    canvas.create_text(titleX0+(titleWidth/2),titleY0+(titleHeight/2),
                text='GENTLE GARDEN',font='Courier 50 bold italic',fill='white')
    
    canvas.create_rectangle(app.newX0,app.newY0,app.newX0+app.newWidth,
                            app.newY0+app.newHeight,fill='white')
    canvas.create_text(app.newX0+(app.newWidth/2),app.newY0+(app.newHeight/2),
                    text='start new game',font='Courier 18')

    canvas.create_rectangle(app.oldX0,app.oldY0,app.oldX0+app.newWidth,
                        app.oldY0+app.newHeight,fill='white')
    canvas.create_text(app.oldX0+(app.newWidth/2),app.oldY0+(app.newHeight/2),
                    text='load saved game',font='Courier 18')

def startMode_mousePressed(app,event):
    app.cx,app.cy = (event.x,event.y)
    # new game
    if clickedOn(app.cx,app.cy,app.newX0,app.newY0,app.newWidth,app.newHeight):
        app.isNewGame = True
        app.mode = None
    # load saved game
    elif clickedOn(app.cx,app.cy,app.oldX0,app.oldY0,
                                            app.newWidth,app.newHeight):
        app.isNewGame = False
        app.mode = None

####################

###################
#### EXIT MODE ####
###################

def exitMode_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')
    canvas.create_text(450,175,text='LEAVING GENTLE GARDEN...',
        font='Courier 40 bold italic',fill='white')

    canvas.create_rectangle(app.exitSaveX0,app.exitSaveY0,
        app.exitSaveX0+app.exitSaveWidth,
        app.exitSaveY0+app.exitSaveHeight,fill='white')
    canvas.create_text(app.exitSaveX0+app.exitSaveWidth/2,
        app.exitSaveY0+app.exitSaveHeight/2,text='save progress',
        font='Courier 14')
    
    canvas.create_rectangle(app.exitCloseX0,app.exitCloseY0,
        app.exitCloseX0+app.exitSaveWidth,
        app.exitCloseY0+app.exitSaveHeight,fill='white')
    canvas.create_text(app.exitCloseX0+app.exitSaveWidth/2,
        app.exitCloseY0+app.exitSaveHeight/2,
        text='exit without saving',font='Courier 14')
    
    canvas.create_text(app.exitCancelX0+app.exitCancelWidth/2,
        app.exitCancelY0+app.exitCancelHeight/2,
        text='cancel',font='Courier 12',fill='white')

def exitMode_mousePressed(app,event):
    app.cx,app.cy = (event.x,event.y)
    
    # don't save
    if clickedOn(app.cx,app.cy,app.exitCloseX0,app.exitCloseY0,
                app.exitSaveWidth,app.exitSaveHeight):
        pass
    # save progress
    elif clickedOn(app.cx,app.cy,app.exitSaveY0,app.exitSaveY0,
        app.exitSaveWidth,app.exitSaveHeight):
        pass
    elif clickedOn(app.cx,app.cy,app.exitCancelX0,app.exitCancelY0,
        app.exitCancelWidth,app.exitCancelHeight):
        app.mode = None


###################

####################
#### NIGHT MODE ####
####################

def nightMode_timerFired(app):
    app.timeElapsed += 10
    if app.timeElapsed >= 500:
        app.timeElapsed = 0
        app.mode = None

def nightMode_reduceWater(app):
    # decrease water level each night so user must water again when needed
    for coord in app.allPlantClasses:
        plant = app.allPlantClasses[coord]
        plant.waterOvernight()
        row,col = coord
        changeWaterLevel(app,row,col,False)
    
    for coord in app.allSeedClasses:
        seed = app.allSeedClasses[coord]
        seed.waterOvernight()
        row,col = coord
        changeWaterLevel(app,row,col,False)
        

def nightMode_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')
    canvas.create_text(app.width/2,app.height/2,text='it is night.',
        font='Courier 14',fill='white')
    canvas.create_text(app.width/2,app.height/2+50,
        text='your plants are growing!',font='Courier 14',fill='white')

#################

def redrawAll(app,canvas):
    
    drawTerrain(app,canvas)
    drawChar(app,canvas)
    drawMenuHead(app,canvas)

    if app.openInventory:
        drawInventory(app,canvas)
    elif app.openPlanting:
        drawPlanting(app,canvas)
    elif app.removingPlants:
        drawStopRemove(app,canvas)
    elif app.isWatering:
        drawStopWater(app,canvas)

def drawStopWater(app,canvas):
    canvas.create_rectangle(app.waterStopX0,app.waterStopY0,
        app.waterStopX0+app.waterStopWidth,app.waterStopY0+app.waterStopHeight)
    canvas.create_text(app.waterStopX0+app.waterStopWidth/2,
        app.waterStopY0+app.waterStopHeight/2,text='finish watering')

def drawStopRemove(app,canvas):
    canvas.create_rectangle(app.stopRemoveX0,app.stopRemoveY0,
        app.stopRemoveX0+app.stopRemoveWidth,  
        app.stopRemoveY0+app.stopRemoveHeight)
    canvas.create_text(app.stopRemoveX0+app.stopRemoveWidth/2,
        app.stopRemoveY0+app.stopRemoveHeight/2,text='finish')


def drawTerrain(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            color = getTerrainColor(app,app.board[row][col])
            x0 = col*app.cellSize
            y0 = row*app.cellSize + app.menuButtonHeight
            x1 = x0 + app.cellSize
            y1 = y0 + app.cellSize + app.menuButtonHeight
            canvas.create_rectangle(x0,y0,x1,y1,fill=color,outline='grey')


def getTerrainColor(app,terrainNum):
    # GRASS
    if terrainNum==0:
        return rgbString(126,200,80)
    # TREE
    elif terrainNum==1 or terrainNum==3:
        return rgbString(180,207,236)
    # OTHER PLANT
    elif terrainNum==2 or terrainNum==4:
        return rgbString(131,105,83)
    
    # TEMP planted tree seed
    elif terrainNum==5:
        return rgbString(0,128,0)
    elif terrainNum==50:
        # TEMP color to rep stages -- sprout, green
        return rgbString(50,205,50)
    elif terrainNum==51:
        # small tree -- purple
        return rgbString(123,104,238)
    elif terrainNum==52:
        # medium tree -- red
        return rgbString(255,0,0)
    elif terrainNum==53:
        # mature tree -- lime
        return rgbString(173,255,47)
    elif terrainNum==54:
        # blooming -- pink
        return rgbString(255,105,180)
    elif terrainNum==55:
        # unripe -- orange
        return rgbString(255,140,0)
    elif terrainNum==56:
        # fruits -- gray
        return rgbString(105,105,105)

    # TEMP planted plant seed
    elif terrainNum==6:
        return rgbString(0,255,127)
    elif terrainNum==30:
        # TEMP color to rep -- sprout, yellow
        return rgbString(255,255,0)
    elif terrainNum==31:
        # small plant -- blue
        return rgbString(135,206,250)
    elif terrainNum==32:
        # medium plant -- light green
        return rgbString(143,188,143)
    elif terrainNum==33:
        # mature plant -- purple
        return rgbString(148,0,211)
    elif terrainNum==34:
        # flowers -- magenta
        return rgbString(255,0,255)
    elif terrainNum==35:
        # unripe -- brown
        return rgbString(139,69,19)
    elif terrainNum==36:
        # fruit -- teal
        return rgbString(32,178,170)
    
    elif terrainNum==100:
        # watered soil
        return rgbString(71,24,4)
    
    elif terrainNum==99:
        # dry soil
        return rgbString(150, 108, 80)
    elif terrainNum==101:
        # overwatered soil
        return rgbString(48, 37, 29)


def drawChar(app,canvas):
    x0 = app.charX - app.charWidth/2
    y0 = app.charY - app.charHeight/2
    x1 = app.charX + app.charWidth/2
    y1 = app.charY + app.charHeight/2
    canvas.create_rectangle(x0,y0,x1,y1,fill="yellow")


def drawMenuHead(app,canvas):
    canvas.create_rectangle(0,0,app.exitWidth,app.exitHeight)
    canvas.create_text(app.exitWidth/2,app.exitHeight/2,text='exit')
    menuItems = ["Inventory","Plant","Water","Harvest"]
    for i in range(4):
        x0 = i*100 + app.exitWidth
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


def drawInventory(app,canvas):
    # draw inventory of food items
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

            item = app.invItems[i][j][0]
            count = app.invItems[i][j][1]
            canvas.create_text(colX0+colWidth/2,colY0+colWidth/2,
                                    text=item+" "+str(count))
    
    canvas.create_text(825+app.closeInvHeight/2,50+app.closeInvHeight/2,
                            text='X')

def drawPlanting(app,canvas):
    # draw screen for seeds and to plant
    canvas.create_text(app.plantingX0+(app.plantingX1-app.plantingX0)/2,
        app.plantingY0+(app.plantingY1-app.plantingY0)/2,
        text='select seed to plant and press enter to start planting!')
    
    canvas.create_rectangle(app.plantingX0,app.plantingY0,
                            app.plantingX1,app.plantingY1,fill="white")
    canvas.create_text(app.plantingX1-app.closePlantingHeight/2,
                    app.plantingY0+app.closePlantingHeight/2,text="X")
    
    for j in range(2):
        for i in range(3):
            colX0 = (app.plantingX0+app.plantingSlot*i + app.plantingSide*(i+1))
            colY0 = (app.plantingY0+ app.plantingSlot*j + app.plantingTop*(j+1))
            canvas.create_rectangle(colX0,colY0,colX0+app.plantingSlot,
                colY0+app.plantingSlot)
            
            seedName = app.seedInv[j][i][0]
            seedCount = app.seedInv[j][i][1]
            canvas.create_text(colX0+app.plantingSlot/2,
                colY0+app.plantingSlot/2,text=seedName+' '+str(seedCount))
    
    canvas.create_rectangle(app.unplantX0,app.unplantY0,
        app.unplantX0+app.unplantWidth,app.unplantY0+app.unplantHeight)
    canvas.create_text(app.unplantX0+app.unplantWidth/2,
        app.unplantY0+app.unplantHeight/2,text='remove plants')

runApp(width=900,height=700)