import pygame
from Engine.Game import Game
from Engine.GameElements import GameplayObjects, GameSprite, GameObject, AnimationList
from pygame.locals import *
from PRObotMenu import PRObotMenu
from PRObotUI import PRObotUI, RunTable
from Engine.UI import UIDraggable

class PRObotGame(Game):
    def __init__(self):
        Game.__init__(self, "PRObot", True, (0, 0, 255), (500, 500))
        self.Menu = PRObotMenu(self.screen)    #It is recommended to overwrite this
            
    def Init(self):
        Game.Init(self)
        
        Box1 = PRObotObject("B1", self.screen, "bounce.bmp", (225,225))
        Box1.AddAnimationList("Flip", AnimationList(["bounce.bmp", "drop.bmp", "forward.bmp", "f1.bmp"]))        
        Boxes = GameplayObjects(self.screen, Box1)
        self.AddFeature("Boxes", Boxes)

        self.UI = PRObotUI(self.screen)
        self.AddFeature("GameUI",self.UI)
        
        self.Run = RunTable(self.screen)
        self.AddFeature("RunTable",self.Run)
        self.Draggables = 0
        
    def HandleMenuEvent(self, menuEvent):
        """View Game class for examples on how to handle this function"""
        if menuEvent == True:
            return True
        if menuEvent == False:
            return False
        if menuEvent == "Exit":
            return False
        if menuEvent == "Continue":
            self.unPauseGame()
            self.Menu.Deactivate()
            return True
        if menuEvent == "NewGame":
            self.unPauseGame()
            self.Menu.Deactivate()
            self.Init()
            return True
        return True
                
    def HandleGameEvent(self, event):
        if event.type == QUIT:
            print "Requesting quit"
            return False    
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.PauseGame()
                print "Pausing and navigating to menu"
                self.Menu.Activate()
                return True
            if event.key == K_RETURN:
                self.Go()
                return True
        UIReturn = self.UI.HandleEvents(event)
        if UIReturn != None:
            if UIReturn == "Go":
                self.Go()
                return True
            try:
                if UIReturn[0] == "GenDrag":
                    button = UIReturn[1]
                    self.GenDraggable(button)
                    return True
            except:
                if UIReturn == True:
                    return True
        return True
    
    def GenDraggable(self, button):        
        self.Draggables += 1
        n = self.Draggables
        Draggable = None
        if button == "Fd":
            Draggable = UIDraggable("DF"+str(n), self.screen, "forward.bmp", (-20,-10))
        if button == "Jp":
            Draggable = UIDraggable("DJ"+str(n), self.screen, "jump.bmp", (-20,-10))
        if Draggable != None:
            Draggable.CursorLatch()
            self.UI.AddItem(Draggable)        
    
    def Go(self):
        if self.Get("Boxes").Get("B1").GetUpdateState()=="Flip":
            self.Get("Boxes").Get("B1").SetUpdateState("Idle")
        else:
            self.Get("Boxes").Get("B1").SetUpdateState("Flip")
    
class PRObotObject(GameObject):
    def Update(self):
        if self.UpdateState == "Flip":
            self.Animate("Flip", 5)
        return GameObject.Update(self)

def LaunchGame():
    print "Launching PRObot..."
    game = PRObotGame()
    game.RunGame()
    
if __name__ == "__main__":
    LaunchGame()