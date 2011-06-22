def passthrough():
    return True    

class DecisionTree():
    def __init__(self, trueact=None, condition=passthrough, falseact=None):
        self.condition = condition
        self.trueact = trueact
        self.falseact = falseact
        
    def getDecision(self, **params):
        if self.falseact == None:
            return self.trueact
        if self.condition(params['ifparams']):
            try:return self.trueact.getDecision(params['trueparams'])
            except:return self.trueact.getDecision(ifparams=params['ifparams'])
        else:
            try:return self.falseact.getDecision(params['falseparams'])
            except:return self.falseact.getDecision(ifparams=params['ifparams'])

    def setCondition(self, condition):
        self.condition = condition
            
    def setTrueact(self, trueact):
        self.trueact = trueact
    
    def setFalseact(self, falseact):
        self.falseact = falseact
        
    def getMaxDepth(self):
        try:
            return 1+self.trueact.getMaxDepth()
        except:
            try:return 1+self.falseact.getMaxDepth()
            except:return 1
    
    def getMinDepth(self):
        try:
            td = 1+self.trueact.getMinDepth()
            try:fd = 1+self.falseact.getMinDepth()
            except:return 1
            return min(td,fd)
        except:
            return 1
        
