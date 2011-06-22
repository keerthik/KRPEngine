from Engine.Game import Game
from Engine.GameElements import GameplayObjects
from Engine.Menu import Menu, MenuItem
from Hive.HiveUI import HiveUI
from Hive.Primitives import *
from Swarmer import Swarmer
from World import World
from pygame.locals import *
import Engine.Base as Base
import pygame

class HiveGame(Game):
    def __init__(self):
        Game.__init__(self, "Hive", True, (0,0,0), (800,600))
        self.Menu = HiveMenu(self.screen)
    
    def Settings(self):
        """Settings operations here: Manipulate menu handlers"""
    def LoadGame(self):
        """Menu handlers for load game menu""" 
    
    def Init(self):
        if hasattr(self,"world"):
            del self.world
        if hasattr(self,"Swarmers"):
            del self.Swarmers
        Game.Init(self)
        self.clockrate = 100
        Base.set_resource_path('Resources')
#        offscreen = self.screen.get_size()
        self.initSwarmers(2,5)
        self.AddFeature("World", self.world)
        self.AddFeature("swarmers", self.Swarmers)
        self.ui = HiveUI(self.screen)
        self.AddFeature("Programmer", self.ui)
        
        self.lastCode = None
        
    def initSwarmers(self,teams,number):
        self.world = World()
        self.Swarmers = GameplayObjects(self.screen)
        for i in range(teams*number):
            team = i%teams
            N = i/teams
            new = Swarmer("S"+str(team)+str(N), self.screen, team, (250+team*100,150+N*70), 200)
            new.setWorld(self.world)
            self.Swarmers.Add(new)
        self.world.addUnits(self.Swarmers)

    def HandleMenuEvent(self, menuEvent):
        if menuEvent == M_EXIT:
            return False
        if menuEvent == M_CONTINUE:
            self.unPauseGame()
            self.Menu.Deactivate()
            return True
        if menuEvent == M_NEWGAME:
            print "New game happening!"
            self.unPauseGame()
            self.Init()
            self.Menu.Deactivate()
            return True
        if menuEvent == M_LOADGAME:
            self.LoadGame()
        if menuEvent == M_SETTINGS:
            self.Settings()
        if menuEvent == True:
            return True
        if menuEvent == False:
            return False
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
                self.Unfreeze()
                return True
            if event.key == K_RETURN:
                self.FlipFreeze()
                self.ui.ShowHide()
            if event.key == K_SPACE:
                    self.FlipFreeze()
        if not self.Paused:
            for swarmer in self.Get("swarmers").GetAll():
                if swarmer.ClickEvent(event):
                    print "Clicked on swarmer", swarmer.Name
        if self.ui.Uishow:
            UIreturn = self.ui.HandleEvents(event)
            if UIreturn != None:
                if UIreturn.has_key("DropZone"):
                    if UIreturn["Action"] == "Dropped" and UIreturn["DropZone"] != None:
                        self.ui.getCodeBox(UIreturn["DropZone"]).setCode(UIreturn["Code"])                        
                    if UIreturn["Action"] == "Picked" and UIreturn["PickupZone"] != None:
                        self.ui.getCodeBox(UIreturn["PickupZone"]).setCode(None)                        
                if UIreturn["Action"] == "Compile":
                    self.ui.CompileCode()
        return True

        
class HiveMenu(Menu):
    def __init__(self, surface):
        Menu.__init__(self, surface, [], "Hive Mind: Main Menu", Nshown = 5)
        self.AddMenuItem(MenuItem("New Game", (0, 255, 0), M_NEWGAME))
        self.AddMenuItem(MenuItem("Resume Game", (0, 255, 0), M_CONTINUE))
        self.AddMenuItem(MenuItem("Load Game", (0, 255, 0), M_LOADGAME))
        self.AddMenuItem(MenuItem("Settings", (0, 255, 0), M_SETTINGS))
        self.AddMenuItem(MenuItem("Exit", (0, 255, 0), M_EXIT))
        self.Highlight(0)

def LaunchGame():
    print "Launching Hive!..."
    game = HiveGame()
    game.RunGame()
    
if __name__ == "__main__":
    LaunchGame()