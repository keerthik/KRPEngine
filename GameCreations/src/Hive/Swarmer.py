from Engine.GameElements import GameObject
import Engine.Base as Base
import random, math
from Decision import *
import pygame

class Swarmer(GameObject):
    def __init__(self, Name, surf, alliance, pos, sensors = 50):
        
        if alliance == 0:GameObject.__init__(self, Name, surf, "swarmer-green.png", pos)
        elif alliance == 1: GameObject.__init__(self, Name, surf, "swarmer.png", pos)
        self.Sensors = sensors
        self.Alliance = alliance
        self.World = None

        self.makeTree()                    
        
        self.hitpoints = 100
        self.speed = 5
        self.atrange = Base.mean(self.Sprite.rect.size)+10
        self.atcd = 10
        self.cur_atcd = 0
        self.atdmg = 10
        
    def makeTree(self):
        Scout = DecisionTree(self.Scout)
        Retreat = DecisionTree(self.Retreat)
        Attack = DecisionTree(self.Attack)
        if self.Alliance == 0:file = open('condition1.py')
        elif self.Alliance == 1:file = open('condition2.py')
        exec file
        
    def getPos(self):
        return self.Sprite.rect.center
    
    def isAlive(self):
        if self.hitpoints > 0:
            return True
        else:
            self.Sprite.kill()
        return False
    
    def takeDamage(self, damage):
        self.hitpoints -= damage
    
    def setWorld(self, world):
        self.World = world
        
    def sortEnemies(self):
        dists = [(Base.distance(enemy.getPos(), self.getPos()), enemy) for enemy in self.Enemies]
        dists.sort()
        self.Enemies = dists

    def sense(self):
        enemies = 1-self.Alliance
        radius = self.Sensors
        self.Enemies = self.World.getUnits(self.getPos(), radius, enemies)
        self.sortEnemies()
        self.Allies = self.World.getUnits(self.getPos(), radius, self.Alliance)
#        self.Allies.remove(self)
        
    def Retreat(self):
        if self.Enemies == []:
            return False
#        print self.Name, "is Retreating"
        vector = [0, 0]
        for enemy in self.Enemies:
            distx, disty = Base.tuple_add(enemy[1].getPos(), self.getPos(), '-')
            if distx == 0:forcex = random.choice([-1, 0, 1]) 
            else:forcex = self.Sensors/distx
            if disty == 0:forcey = random.choice([-1, 0, 1]) 
            else:forcey = self.Sensors/disty
            vector = Base.tuple_add(vector, (-forcex,-forcey))
        x, y = vector
        if self.move(x,y):
            return True
        else:
            return False

    def Attack(self, enemy = None):
        if self.Enemies == []:
            return False
        if enemy == None:
            enemy = self.Enemies[0]
        if enemy[0] > self.atrange:
#            print self.Name, "is Attacking: Moving into range"
            x, y= Base.tuple_add(enemy[1].getPos(), self.getPos(), '-')
            self.move(x, y)
        else:
            if self.cur_atcd == 0:
#                print self.Name, "attacked for", self.atdmg, "damage;", \
#                    enemy[1].Name, "has", enemy[1].hitpoints, "hp left"
                enemy[1].takeDamage(self.atdmg)
                self.cur_atcd = 10
            else: self.cur_atcd -=1
        return True
    
    def Scout(self):
        if self.Enemies == []:
            print self.Name, "is Scouting"
            direction = random.randint(-1,1),random.randint(-1,1)
            self.move(direction[0], direction[1])
        return True
    
# Act is based on action = decide(condition, trueact, falseact); run(action)
# *check condition
# *if condition holds, return true-action
# *if not, return false-action
# Notes: true-action and false-action can be other "decide" calls
# A simple case-based decision tree is the output plan here

    def act(self):
        self.Action = self.decide()
        self.Action()
    
    def decide(self):
        return self.Tree.getDecision(ifparams = self)
    
    def move(self, x, y):
        X,Y = Base.normalize((x,y))
        return self.Sprite.Translate((self.speed*X,self.speed*Y), None, True)
    
    def update(self):
        if not self.isAlive():
            return True
        self.sense()
        self.act()
        return True

    