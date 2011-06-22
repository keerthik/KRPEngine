import Engine.Base as Base

class World():
    def __init__(self, units = None):
        if units == None:
            self.Units = []
        else:
            self.Units = units
        self.limbox = [(0,800),(0,600)]
        
    def addUnits(self, Units):
        self.D = Units
        self.Units.extend(self.D.GetAll())
        
    def NewWorld():
        self.Units = []
        
    def getUnits(self, center = (0, 0), radius = 0, alliance = -1):
        reqUnits = []
        if alliance == -1:
            reqUnits.extend(self.Units)
        else:
            for unit in self.Units:
                if unit.Alliance == alliance and unit.isAlive():
                    reqUnits.append(unit)
        if radius == 0:
            return reqUnits
        unitList = reqUnits[:]
        for unit in reqUnits:
            if Base.distance(unit.Sprite.rect.center, center) > radius:
                unitList.remove(unit)
        reqUnits = unitList
        return reqUnits
    
    def draw(self):
        return True
    
    def update(self):
        for unit in self.Units:
            if unit.hitpoints <= 0:
                self.Units.remove(unit)
                self.D.Remove(unit.Name)
                
#        if self.limbox[0][1]-self.limbox[0][0]>50:
#            self.limbox[0] = Base.tuple_add(self.limbox[0], (1,-1))
#        if self.limbox[1][1]-self.limbox[1][0]>50:
#            self.limbox[1] = Base.tuple_add(self.limbox[1], (1,-1))
        return True
