from cmu_112_graphics import *
import random

class NewPlant:
    # super class with watering, temp, and all main fxns

    def __init__(self,coord,type):
        self.coord = coord
        self.type = type
        self.growth = 0
        # stage = seed, small tree, small plant, etc.
        self.stage = 0

        # different plants have different temperatures to grow
        if type=='peach' or type=='apple':
            self.bestGrowth = (65,75)
            self.slowGrowth = (40,64,76,100)
        elif type=='lemon':
            self.bestGrowth = (75,85)
            self.slowGrowth = (40,74,86,99)
        elif type=='tomato':
            self.bestGrowth = (60,75)
            self.slowGrowth = (40,59,76,99)
        elif type=='strawb':
            self.bestGrowth = (60,80)
            self.slowGrowth = (40,59,81,99)
        elif type=='blackb':
            self.bestGrowth = (60,70)
            self.slowGrowth = (40,59,71,99)

        self.tempStatus = None

        self.waterLevel = 2
        self.isDry = False
        self.isOverwatered = False
    
        self.overallStatus = 10
        # self.isDead = isPlantDead()
    
    def waterOvernight(self):
        # plant loses water status at night
        self.waterLevel -= 2
        self.updateWaterStatus()

    def waterPlant(self):
        # fxn to water plant
        self.waterLevel += 1
        self.updateWaterStatus()
    
    def updateWaterStatus(self):
        if self.waterLevel >= 5:
            self.isOverwatered = True
        elif self.waterLevel < 0:
            self.isDry = True
        else:
            self.isDry = False
            self.isOverwatered = False

    def checkTemp(self,currTemp):
        # perfect temp
        if (currTemp>=self.bestGrowth[0]) and (currTemp<=self.bestGrowth[1]):
            self.tempStatus = 4
        # too cold
        elif (currTemp>=self.slowGrowth[0]) and (currTemp<=self.slowGrowth[1]):
            self.tempStatus = 2
        # too warm
        elif (currTemp>=self.slowGrowth[2]) and (currTemp<=self.slowGrowth[3]):
            self.tempStatus = 3

    def getOverallStatus(self):
        if self.tempStatus==3:
            # too warm and too dry is bad
            if self.isDry:
                self.overallStatus -= 2
                self.waterLevel -= 1
                self.updateWaterStatus()
            # warm when overwatered
            elif self.isOverwatered:
                self.waterLevel -= 1
                self.updateWaterStatus()
                # still overwatered
                if self.isOverwatered:
                    self.overallStatus -= 1
            else:
                # given otherwise perfect conditions, moderate growth
                self.overallStatus -= 1
        
        elif self.tempStatus==2:
            if self.isDry or self.isOverwatered:
                self.overallStatus -= 2
            else:
                self.overallStatus -= 1
        
        # perfect temperature! basically resets
        elif self.tempStatus==4: 
            self.overallStatus = 10
            if self.isDry or self.isOverwatered:
                self.overallStatus -= 3
        
        if self.overallStatus <= 3:
            # plant doesn't die but doesn't grow :(
            self.overallStatus = 3
    
    
    def growPlant(self):
        self.getOverallStatus()
        if self.overallStatus >= 8:
            self.growth += 2
        elif self.overallStatus >= 4 and self.overallStatus <= 7:
            self.growth += 1


class Seed(NewPlant):
    # checks if full seed plant
    def __init__(self,coord,type):
        super().__init__(coord,type)
        self.growth = 0
        self.stage = 0
    
    def checkGrowth(self,type):
        if self.growth>=4 and self.growth<8:
            # sprout
            self.stage = 1
        # split between plant and tree
        elif self.growth>=8:
            self.stage = 2
            if type in ['peach','apple','lemon']:
                return Tree(self.coord,self.type)
            else:
                return Plant(self.coord,self.type)

# trees - second attempt
class Tree(NewPlant):
    def __init__(self,coord,type):
        super().__init__(coord,type)
        self.growth = 0
        # small tree
        self.stage = 2
        self.numFruits = 0
    
    def checkGrowth(self,type):
        self.getOverallStatus()
        if self.growth>=6 and self.growth<10:
            print('success')
            # medium tree
            self.stage = 3
        elif self.growth>=10 and self.growth<18:
            # mature tree
            self.stage = 4
        elif self.growth>=18 and self.growth<24:
            # blooming tree
            self.stage = 5
        elif self.growth>=24 and self.growth<28:
            # unripe tree
            self.stage = 6
        elif self.growth>=28:
            # has fruits
            self.stage = 7
            self.growFruit()
    
    def pickFruit(self):
        self.numFruits -= 1
        if self.numFruits < 0:
            self.numFruits = 0
    
    def growFruit(self):
        if self.type=='apple' or self.type=='lemon':
            self.numFruits = 6
        elif self.type=='peach':
            self.numFruits = 4


class Plant(NewPlant):
    def __init__(self,coord,type):
        super().__init__(coord,type)
        self.growth = 0
        # small plant
        self.stage = 2
        self.numFruits = 0
    
    def checkGrowth(self,type):
        self.getOverallStatus()
        if self.growth>=2 and self.growth<6:
            # med plant
            self.stage = 3
        elif self.growth>=6 and self.growth<10:
            # mature plant
            self.stage = 4
        elif self.growth>=10 and self.growth<14:
            # flowering plant
            self.stage = 5
        elif self.growth>=14 and self.growth<18:
            # unripe plant
            self.stage = 6
        elif self.growth>=18:
            # fruiting plant
            self.stage = 7
            self.growFruit()
    
    def pickFruit(self):
        self.numFruits -= 1
        if self.numFruits < 0:
            self.numFruits = 0
    
    def growFruit(self):
        if self.type=='blackb':
            self.numFruits = 7
        elif self.type=='strawb':
            self.numFruits = 5
        elif self.type=='tomato':
            self.numFruits = 6