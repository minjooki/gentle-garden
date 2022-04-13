import random

# procedural terrain generation code based off of Kate Weeden:
# https://medium.com/inspired-to-program-%E3%85%82-%D9%88-%CC%91%CC%91/procedural-generation-in-python-7b75127b2f74 

# start with initial game start (level 1?), which is 900 x 700 board
# every "block" is 50 pixels

def generateNoise(width,height):
    plotSize = 50
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

    print(minVal,firstMid,secondMid,maxVal)

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

print(generateNoise(900,700))