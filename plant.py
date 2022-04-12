from cmu_112_graphics import *
import random

class Plant:
    # super class with watering, temp, and all main fxns

    def __init__(self,type):
        self.type = type
        self.growth = 0

        # different plants have different temperatures to grow
        if type=='peach' or type=='apple':
            self.bestGrowth = (65,75)
            self.slowGrowth = (50,64,76,90)
            self.noGrowth = (40,49,91,99)
        elif type=='lemon':
            self.bestGrowth = (75,85)
            self.slowGrowth = (60,74,86,99)
            self.noGrowth = (50,59,100,110)
        elif type=='tomato':
            self.bestGrowth = (60,75)
            self.slowGrowth = (50,59,76,84)
            self.noGrowth = (40,49,85,99)
        elif type=='strawberry':
            self.bestGrowth = (60,80)
            self.slowGrowth = (45,59,81,89)
            self.noGrowth = (40,44,90,99)
        elif type=='blackberry':
            self.bestGrowth = (60,70)
            self.slowGrowth = (50,59,71,85)
            self.noGrowth = (40,49,86,99)

        self.tempStatus = None

        self.waterLevel = 2
        self.isDry = False
        self.isOverwatered = False
    
        self.overallStatus = 10
        # self.isDead = isPlantDead()
    
    def waterPlant(self):
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
        elif ((currTemp>=self.noGrowth[0]) and \
                (currTemp<=self.noGrowth[1])) or \
                ((currTemp>=self.noGrowth[2]) and 
                (currTemp<=self.noGrowth[3])):
            self.tempStatus = 1
        else:
            self.tempStatus = 0

    def getOverallStatus(self):
        # first check if worst case
        if self.tempStatus==0 or self.tempStatus==1:
            self.overallStatus = 3

        elif self.tempStatus==3:
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
    
    def isPlantDead(self):
        if self.overallStatus < 0:
            return True
        return False
    
    def growPlant(self):
        if self.overallStatus >= 8:
            self.growth += 2
        elif self.overallStatus >= 4 and self.overallStatus <= 7:
            self.growth += 1


class Seed(Plant):
    # checks if full seed plant
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 4:
            Sprout(type)

class Sprout(Plant):
    def __init__(self,type):
        super().__init__(type)
        # start at 0 again
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 4:
            if type in ['peach','apple','lemon']:
                SmallTree(type)
            else:
                SmallPlant(type)

# trees
class SmallTree(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0

    def checkGrowth(self,type):
        if self.growth >= 6:
            MedTree(type)


class MedTree(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 8:
            MatureTree(type)


class MatureTree(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 8:
            FlowerTree(type)


class FlowerTree(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 4:
            UnripeTree(type)


class UnripeTree(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 4:
            FruitTree(type)


class FruitTree:
    def __init__(self,type):
        self.type = type
        self.numFruits = random.randint(2,6)


# plants
class SmallPlant(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 2:
            MedPlant(type)

class MedPlant(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 4:
            MaturePlant(type)

class MaturePlant(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 6:
            FlowerPlant(type)

class FlowerPlant(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 2:
            UnripePlant(type)

class UnripePlant(Plant):
    def __init__(self,type):
        super().__init__(type)
        self.growth = 0
    
    def checkGrowth(self,type):
        if self.growth >= 4:
            FruitPlant(type)

class FruitPlant:
    def __init__(self,type):
        self.numFruits = random.randint(3,8)
    