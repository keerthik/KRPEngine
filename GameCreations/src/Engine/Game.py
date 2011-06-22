import Base
import pygame
from pygame.locals import *
from Menu import Menu

class Game:
    def __init__(self, name = 'UnnamedGame', mouse_exists = True, bgcolor = (0, 0, 0), DISP_SIZE = (0,0)):
        self.Name = name
        self.BGcolor = bgcolor
        self.Mouse = mouse_exists
        if DISP_SIZE == (0, 0):
            self.DISP_SIZE = Base.DISP_SIZE
        else:
            self.DISP_SIZE = DISP_SIZE
        self.PreInit()
        self.Menu = Menu()
        self.Paused = False
        self.freeze = False

    def AddFeature(self, objectName, gameObject):
        """Add an object into the object dictionary. These objects are each 
        iterated over and their draw and update functions are each called
        in the appropriate part of the gameloop"""
        try:
            self.GameFeatures[objectName] = gameObject
        except:
            print "Unable to add game object "+objectName
        
    def Get(self, FeatureName):
        return self.GameFeatures[FeatureName]
    
    def Freeze(self):
        """Stop updating game objects. Continues drawing"""
        self.freeze = True
    
    def Unfreeze(self):
        """Resume updating game objects. Drawing is unaffected"""
        self.freeze = False
        
    def FlipFreeze(self):
        """Flip freeze state"""
        self.freeze = not self.freeze
        
    def PauseGame(self, menu = True):
        """Stop updating or drawing game objects"""
        self.PausedObjects = self.GameFeatures
        self.Paused = True
        if menu:
            self.Menu.Activate()
            self.GameFeatures = self.MenuObjects
        else:
            self.GameFeatures = {}
        
    def unPauseGame(self):
        """Continue updating or drawing game objects"""
        self.Paused = False
        self.GameFeatures = self.PausedObjects
        self.PausedObjects = {}
        
    def RunGame(self):
        """The basic game structure: Initialize, execute game loop, terminate"""
        self.Init()
        self.Loop()
        self.Terminate()

    def PreInit(self):
        """Standard initialization commands and steps"""
        self.screen = pygame.display.set_mode(self.DISP_SIZE)
        pygame.display.set_caption(self.Name)
        pygame.mouse.set_visible(self.Mouse)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(self.BGcolor)
        self.background = self.background.convert()
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.font.init()
        print "Initialized"
        
    def Init(self):
        """Custom initialization specific to the game"""
        self.clockrate = 60
        self.MenuObjects = {"Menu":self.Menu}
        self.PausedObjects = {}
        self.GameFeatures = {}

        return True
    #============================================================================================    
    def Loop(self):    
        """Game loop: Look for events and handle them, update game objects, draw game objects"""
        RunLoop = True
        while(RunLoop == True):    
            EventRunLoop = self._UserEventHandle()
            if not self.freeze:
                UpdateRunLoop = self._Update()
            DrawLoop = self._Draw()
            RunLoop = EventRunLoop and UpdateRunLoop and DrawLoop

    def _UserEventHandle(self):
        EventRunLoop = True
        for event in pygame.event.get():
            EventRunLoop = (EventRunLoop and self._HandleEvent(event))
        return EventRunLoop
    
    def _Update(self):
        self.clock.tick(self.clockrate)
        UpdateRunLoop = self.UpdateGameObjects()
        return UpdateRunLoop

    def _Draw(self):
        DrawRunLoop = self.DrawGameObjects()
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        return DrawRunLoop
    
    def _HandleEvent(self, event):
        """Decides whether to handle menu type events or game type events"""
        if self.Menu.isActive():
            menuEvent = self.Menu.HandleEvent(event)
            return self.HandleMenuEvent(menuEvent)
        else:
            return self.HandleGameEvent(event)

    def HandleMenuEvent(self, menuEvent):
        """When the game menu is activated, this replaces the event handling loop"""
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

    def HandleGameEvent(self, event):
        """Overwrite with function to handle all in-game events"""    
        if event.type == QUIT:
            print "Requesting quit"
            return False         
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.PauseGame()
                print "Pausing and navigating to menu"
                self.Menu.Activate()
                return True
        return True
            
    def UpdateGameObjects(self):
        """ This function updates all the game objects. The game objects should have their
            own definition for "update". These update functions should return true or false
        """
        UpdateRunLoop = True
        for game_object in self.GameFeatures.values():
            objectRunLoop = game_object.update()
            if type(objectRunLoop) != type(True):
                raise ValueError('Game Object Update function has not specified boolean return')
            else:
                UpdateRunLoop = UpdateRunLoop and objectRunLoop
        return UpdateRunLoop

    def DrawGameObjects(self):
        """ This function draws all the game objects. The game objects should have their
            own definition for "draw". These draw functions should return true or false
        """
        DrawRunLoop = True
        for game_object in self.GameFeatures.values():
            if game_object != None:
                objectRunLoop = game_object.draw()
                if type(objectRunLoop) != type(True):
                    raise ValueError('Game Object Draw function has not specified boolean return')
                else:
                    DrawRunLoop = DrawRunLoop and objectRunLoop
        return DrawRunLoop
            
    #============================================================================================    
    def Terminate(self):
        print "Terminating Game"
        pygame.font.quit()
        pygame.quit()
        Base.Exit()
#================================================================================================
    
if __name__ == "__main__":
    TestGame = Game(name = 'TestGame', DISP_SIZE = (500, 500))
    TestGame.RunGame()