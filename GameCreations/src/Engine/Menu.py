from pygame.locals import *
import pygame

class Menu():
    def __init__(self, rendersurface = None, items = [], name = "UnnamedMenu", FontArgs = ["None", 30], Nshown = 5):
        self.Name = name
        self.MenuItems = items
        self.Nshown = Nshown
        self.TextSurfaces = []
        self.doUpdate = True
        self.Active = False
        if not (pygame.font.get_init()):
            pygame.font.init()
        self.Font = pygame.font.SysFont(*FontArgs) 
        self.Surface = rendersurface
        try:
            self.current = self.MenuItems[0]
        except:
            self.current = None
        self.titleColor = (0,0,255)
        self.highlightColor = (255,0,0)
    
    def RenderTitle(self):
        position = [0, 0]
        width, height = self.Font.size(self.Name)
        textSurf = self.Font.render(self.Name, False, self.titleColor).convert()
        position[0] = 0.5*(self.Surface.get_width() - width)
        position[1] = 2*height + 100
        return textSurf, position
        
    def RenderItem(self, menuItem, position):
        if self.MenuItems[self.current] == menuItem:
            textSurf = self.Font.render(menuItem.Name, True, menuItem.Color, self.highlightColor).convert()
        else:
            textSurf = self.Font.render(menuItem.Name, False, menuItem.Color).convert()
        width, height = self.Font.size(menuItem.Name)
        position[0] = 0.5*(self.Surface.get_width() - width)
        position[1] += 2*height
        return textSurf, position
        
        
    def update(self):
        #TODO: Take into account Nshown, and make a scrollable menu
        if self.doUpdate: 
            self.TextSurfaces = []
            textSurf, position = self.RenderTitle()
            self.TextSurfaces.append((textSurf, position[:]))
            for item in self.MenuItems:
                textSurf, position = self.RenderItem(item, position)
                self.TextSurfaces.append((textSurf, position[:]))
#            position = [0, 0]
#            width, height = self.Font.size(self.Name)
#            textSurf = self.Font.render(self.Name, False, (0,0,0)).convert()
#            position[0] = 0.5*(self.Surface.get_width() - width)
#            position[1] = 2*height
#            self.TextSurfaces = []
#            self.TextSurfaces.append((textSurf,position[:]))
#            for menuItem in self.MenuItems:
#                if self.MenuItems[self.current] == menuItem:
#                    textSurf = self.Font.render(menuItem.Name, True, menuItem.Color, (0, 0, 0)).convert()
#                else:
#                    textSurf = self.Font.render(menuItem.Name, False, menuItem.Color).convert()
#                width, height = self.Font.size(menuItem.Name)
#                position[0] = 0.5*(self.Surface.get_width() - width)
#                position[1] += 2*height
#                self.TextSurfaces.append((textSurf, position[:]))
            self.doUpdate = False
        return True
                
    def drawMenuItems(self):
        for item in self.TextSurfaces:
            textSurf = item[0]
            position = item[1]
            self.Surface.blit(textSurf, position)
        return True

    def draw(self):
        return self.drawMenuItems()
        
    def AddMenuItem(self, menuItem, index = -1):
        if index == -1 or index == len(self.MenuItems):
            self.MenuItems.append(menuItem)
        else:
            self.MenuItems.insert(index, menuItem)
        
    def isActive(self):
        return self.Active
    
    def Activate(self):
        self.Active = True

    def Deactivate(self):
        self.Active = False
        
    def ClickItem(self, index):
        return self.MenuItems[index].click()

    def ClickCurrent(self):
        return self.ClickItem(self.current)
        
    def HandleEvent(self, event):
        """ Populate eventhandle function appropriately"""
        self.doUpdate = True
        if event.type == QUIT: 
            return 0
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return 2
            if event.key == K_DOWN:
                return self.Highlight(self.GetNext())
            if event.key == K_UP:
                return self.Highlight(self.GetPrev())
            if event.key == K_RETURN:
                return self.ClickCurrent()
        return True                

    
    def Highlight(self, index):
        """Do the highlighting action on item with name itemname"""
        if index == None:
            self.current = index
            return True
        try:
            self.MenuItems[index]
        except:
            raise ValueError("Menu list does not have an " + str(index) + "th item")
            return False
        self.current = index
        return True
    
    def GetNext(self):
        if self.current == None:
            return None
        nexindex = (self.current)+1
        if nexindex > len(self.MenuItems)-1:
            nexindex = 0
        return nexindex        

    def GetPrev(self):
        if self.current == None:
            return None
        previndex = (self.current)-1
        if previndex < 0: 
            previndex = len(self.MenuItems)-1
        return previndex
    
    def GetCurr(self):
        return self.current
    
    def GetMenuItems(self):
        return self.MenuItems

class MenuItem():
    """ A single item from a menu. 
        This contains the   name [which will be printed in the menu]
                            the color [used to render in the menu]
                            the command id number returned [to be parsed by the
                                        HandleMenuEvent in the game
                            a custom function if the menu class or wrapper item
                            menu item can carry out this function
    """
    def __init__(self, name = None, color = None, val = 2, customFunc = None):
        self.Name = name
        self.Color = color
        self.ClickReturn = val
        self.ClickFun = customFunc
        
    def click(self, **argsv):
        """Abstract function, doesnt know what to do, but will return ClickReturn
        by default, which offloads coding to the game class"""
        if self.ClickFun:
            self.ClickReturn = self.ClickFun(argsv)
        return self.ClickReturn
    
    