
def cond1(self):
#Too many enemies
	if len(self.Enemies) > len(self.Allies):
		return True
	else:
		return False

def cond2(self):
#Hitpoints too low
	if self.hitpoints < 50:
		return True
	else:
		return False

def cond3(self):
#Hope for survival
	if self.Allies != []:
		return True
	else:
		return False

Desp = DecisionTree(Attack, cond3, Attack)
Toolow = DecisionTree(Desp, cond2, Attack)
self.Tree = DecisionTree(Toolow, cond1, Attack)