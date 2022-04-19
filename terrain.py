import random

# procedural terrain generation code based off of Kate Weeden:
# https://medium.com/inspired-to-program-%E3%85%82-%D9%88-%CC%91%CC%91/procedural-generation-in-python-7b75127b2f74 

# voronoi with grid row/col values idea from 
# https://www.cs.cmu.edu/~112/notes/student-tp-guides/Terrain.pdf 

def generateTerrain(width,height):
    # use later for temp generation
    plotSize = 10
    rows = height//plotSize
    cols = width//plotSize
    noiseMap = [ [0]*cols for row in range(rows) ]

    minVal = 0
    maxVal = 0

    for row in range(len(noiseMap)):
        for col in range(len(noiseMap[0])):
            if row==0 and col==0:
                seed = random.randint(-50,50)
                noiseMap[row][col] = seed
            elif row==0:
                tmpSeed = random.randint(-50,50)
                prevSeed = noiseMap[row][col-1]
                seed = (prevSeed + tmpSeed)//2
                noiseMap[row][col] = seed
            elif col==0:
                tmpSeed = random.randint(-50,50)
                upperSeed = noiseMap[row-1][col]
                seed = (upperSeed + tmpSeed)//2
                noiseMap[row][col] = seed
            else:
                tmpSeed1 = random.randint(-50,50)
                tmpSeed2 = random.randint(-50,50)
                upperSeed = noiseMap[row-1][col]
                prevSeed = noiseMap[row][col-1]
                tmpUpper = (upperSeed + tmpSeed1)/2
                tmpPrev = (prevSeed + tmpSeed2)/2
                seed = (tmpUpper + tmpPrev)//2
                noiseMap[row][col] = seed
            
            if seed<minVal:
                minVal = seed
            elif seed>maxVal:
                maxVal = seed
        
    # normalize into either 1, 2, or 3
    normalized = []
    interval = (maxVal - minVal)/3
    firstMid = minVal + interval
    secondMid = firstMid + interval

    # check which is the closest division point
    for row in range(len(noiseMap)):
        newRow = []
        for col in range(len(noiseMap[0])):
            currNum = noiseMap[row][col]
            if currNum<=firstMid:
                newRow.append(1)
            elif currNum<=secondMid:
                newRow.append(2)
            else:
                newRow.append(3)
        normalized.append(newRow)
    return normalized


def distance(x0,y0,x1,y1):
    return ((y1-y0)**2 + (x1-x0)**2)**0.5


def voronoiSeeds(width,height):
    # places voronoi seeds in random locations
    numPoints = list(range(5))
    pointCoords = []
    for point in numPoints:
        while True:
            x = random.randint(0,width)
            y = random.randint(0,height)
            if (x,y) not in pointCoords:
                break
        pointCoords.append((x,y))
    return pointCoords


def getClosestSeeds(L,width,height):
    # returns dictionary of each seed point mapped to list of closest cells
    cellSize = 10
    rows = height//cellSize
    cols = width//cellSize
    voronoi = {}

    for row in range(rows):
        for col in range(cols):
            midX = col*cellSize + cellSize/2
            midY = row*cellSize + cellSize/2
            seed = getClosest(L,midX,midY)

            if seed not in voronoi:
                voronoi[seed] = []
            voronoi[seed].append((row,col))
    return voronoi


def getClosest(L,x,y):
    # gets closest seed from the current cell midpoint
    closestPoint = None
    closestDistance = None
    for seed in L:
        if closestDistance==None:
            closestDistance = distance(seed[0],seed[1],x,y)
        x0 = seed[0]
        y0 = seed[1]
        dist = distance(x0,y0,x,y)
        if dist <= closestDistance:
            closestDistance = dist
            closestPoint = seed
    return closestPoint
