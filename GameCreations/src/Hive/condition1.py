def cond1(self):
        if len(self.Enemies) > len(self.Allies):
            return True
        else:
            return False
self.Tree = DecisionTree(Retreat, cond1, Attack)
