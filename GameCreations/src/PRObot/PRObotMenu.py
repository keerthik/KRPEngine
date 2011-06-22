from Engine.Menu import Menu, MenuItem
from pygame.locals import *

class PRObotMenu(Menu):
    def __init__(self, surface):
        Menu.__init__(self, surface, [], "PRObotMenu", Nshown = 5)
        self.AddMenuItem(MenuItem("New Game", (0, 255, 0), "NewGame"))
        self.AddMenuItem(MenuItem("Resume Game", (0, 255, 0), "Continue"))
        self.AddMenuItem(MenuItem("Edit Map", (0, 255, 0), "EditMap"))
        self.AddMenuItem(MenuItem("Exit", (0, 255, 0), "Exit"))
        self.Highlight(0)
        
    def Highlight(self, itemname):
        """ custom highlight function"""
        Menu.Highlight(self,itemname)
                    
if __name__ == "__main__":
    PBM = PRObotMenu()
    print "Compiles"