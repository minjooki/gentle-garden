import random

# voronoi with grid row/col values idea from 
# https://www.cs.cmu.edu/~112/notes/student-tp-guides/Terrain.pdf 


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
