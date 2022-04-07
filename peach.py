from cmu_112_graphics import *

# plant tree
class PeachSeed:
    def __init__(self):
        self.growthStages = ['seed','germinating','small tree','medium tree',
            'mature tree','budding','flowering','unripe','fruits','no fruits']
        self.growthStage
        self.growth = 0
        self.canHarvest = False

        # 0 == dry, 1 == damp, 2 == wet, 4 == overwatered
        self.waterLevel =  0
        self.isDry = False
        self.isOverwatered = False

        # 4, 3, 2, 1, 0 levels of temp based on below ranges (0 == dead)
        self.tempStatus = None
        self.bestGrowth = (65,75)
        self.slowGrowth = (50,64,76,90)
        self.noGrowth = (40,49,91,99)

        # range of 0 to 10, changes based on environmental influences 
        # start from best growth situation
        # 0 - 1 is no growth
        # 2 - 4 is slow growth
        # 5 - 7 is moderate growth
        # 8 - 10+ is best growth
        self.overallStatus = 10
        self.isDead = self.isPeachDead(self)

    
    def waterPeach(self):
        self.waterLevel += 1
        self.updateWaterStatus(self)
    
    def updateWaterStatus(self):
        if self.waterLevel >= 4:
            self.isOverwatered = True
        elif self.waterLevel < 0:
            self.isDry = True
        else:
            self.isDry = False
            self.isOverwatered = False
    
    def checkGrowPeach(self,currTemp):
        # check temperature + update status
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
        # first check is worst case
        if self.tempStatus==0:
            self.overallStatus -= 4
        
        # with no growth status
        elif self.tempStatus==1:
            self.overallStatus -= 3

        elif self.tempStatus==3:
            # too warm and too dry is bad
            if self.isDry:
                self.overallStatus -= 2
            # warm when overwatered
            elif self.isOverwatered:
                self.waterLevel -= 1
                self.updateWaterStatus(self)
                if self.isOverwatered:
                    self.overallStatus -= 2
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
        
    def isPeachDead(self):
        if self.overallStatus < 0:
            return True
        return False
    
    def growPeach(self):
        if self.overallStatus >= 8:
            # like normal, take ~2 days for each stage
            pass
        elif 5<=self.overallStatus<=7:
            pass
        elif 2<=self.overallStatus<=4:
            pass
        elif self.overallStatus <= 1:
            # do not advance
            pass
        

                



def plantPeach(remainingSeeds,numPlanted):
    remainingSeeds -= numPlanted
    return remainingSeeds
