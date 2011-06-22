from GameElements import GameObject, GameplayObjects
import pygame, Base
from pygame.locals import *

TOP = 0
RIGHT = 1
BOT = 2
LEFT = 3 

class UI(GameplayObjects):
    """A base class intended to be used as a game object in the main game
    Listens for clicks and drags on the elements inside"""
    def __init__(self, surface):
        GameplayObjects.__init__(self, surface)
        self.Uishow = False
        
        self.TOPLEFT = (0,0)
        self.BOTRIGHT = self.surf.get_size()
        self.TOPRIGHT = (self.BOTRIGHT[0], self.TOPLEFT[1])
        self.BOTLEFT = (self.TOPLEFT[0], self.BOTRIGHT[1])
        
        self.ToolItem = None
        self.ToolTipBox = pygame.Surface((0,0)).convert()
    
    def Show(self):
        """Make the UI drawable in the next draw cycle"""
        self.Uishow = True
        
    def Hide(self):
        """Prevent the UI from being shown in the next draw cycle"""
        self.Uishow = False
        
    def ShowHide(self):
        """Toggle the Shown/Hidden state of this UI"""
        self.Uishow = not self.Uishow
        
    def SetOnClick(self, uiitemName, onclick):
        """Set the onclick operation for an item in this UI"""
        self.GameObjects[uiitemName].SetOnClick(onclick)
        
    def draw(self):
        if self.Uishow:
            self.Drawables.draw(self.surf)
            self._blitToolTip()
        return True

    def _blitToolTip(self):
        """Check if a tooltip is expected and draw it"""
        if not pygame.font or self.ToolItem == None:
            self.ToolTipBox = pygame.Surface((0,0)).convert()
            return True
        elif self.ToolItem.DrawToolTip:
            fontsize = 20
            self.surf.blit(self.ToolTipBox, Base.tuple_add(self.ToolItem.Sprite.rect.topleft,(10,fontsize+5), '-'))
            return False
    
    def HandleEvents(self, event):
        UIreturn = None
        for uiitem in self.GameObjects.values():
#            if uiitem.DrawToolTip:
#                self.ToolTipBox = uiitem.ToolTipBox
#                self.ToolItem = uiitem
            try:
                if uiitem.ClickEvent(event):
                    UIreturn = uiitem.OnClick()
            except:
                """no click event defined"""
            try:
                if uiitem.DragEvent(event):
                    UIreturn = uiitem.ReturnBundle
                    return UIreturn
            except:
                """no drag event defined"""
        return UIreturn
    
    def GetUIdict(self):
        """Returns the dictionary of UI objects with their names as keys"""
        return self.GameObjects
    
    def GetUIitems(self):
        """Returns a list of the UI objects"""
        return self.GameObjects.values()        

    def GetUIsprites(self):
        """Returns a pygame Spritegroup of the UI sprites"""
        return self.Drawables

class UIitem(GameObject):
    """A UI object class that recognizes more user actions""" 
    def __init__(self, Name, screen, base_image, position = (0,0)):
        GameObject.__init__(self, Name, screen, base_image, position)
        self.ToolTip = None
        self.ReturnBundle = {}
        self.ShowTip = False
        self.DrawToolTip = False
        self.ToolTipBox = None
        
    def OnClick(self):
        """Returns a signature string that is set as the event return
        for the UI class that contains this object. This string can be set
        and recognized outside to carry out a corresponding action"""
        return self.ReturnBundle

    def SetOnClick(self, Bundle):
        """Sets the signature string for this UI object to return when it
        is clicked on"""
        self.ReturnBundle = Bundle
            
    def OnMouseOver(self):
        """Actions to be carried out when this UI object is moused over. 
        By default looks for whether a tooltip has been assigned, and will show
        the tooltip"""
        if self.ShowTip:
            if not self.DrawToolTip:
                self.ToolTipBox = self.RenderToolTip()
            self.DrawToolTip = True
        else:
            self.DrawToolTip = False

    def RenderToolTip(self):
        """Prepares a tooltip for the UI class to draw if needed. TODO: Needs to
        be refactored"""
        if self.ToolTip == None:
            return False
        fontsize = 20
        font = pygame.font.Font(None, fontsize)
        text = font.render(self.ToolTip, 1, (250, 250, 250))
        hoverBox = pygame.Surface(Base.tuple_add(text.get_rect()[2:],(fontsize,6))).convert()
        hoverBox.fill((0,100,200))
        textpos = text.get_rect(centerx=hoverBox.get_width()/2, centery=hoverBox.get_height()/2)
        hoverBox.blit(text, textpos)
        return hoverBox
    
    def SetToolTip(self, text, showOnHover = True):
        """Set the text for tooltip on hovering over this UI button"""
        self.ToolTip = text
        if showOnHover:
            self.ShowTip = True
            
    def Update(self):
        self.DrawToolTip = False
        if self.CursorOver():
            self.OnMouseOver()
        return GameObject.Update(self)

class UIDraggable(UIitem):
    def __init__(self, Name, screen, base_image, position = (0,0)):
        UIitem.__init__(self, Name, screen, base_image, position)
        self.Dragged = False
        self.Snap = False
        
    def OnCursorLatch(self):
        self.Dragged = True
        self.previous_pos = pygame.mouse.get_pos()
        
    def OnDrag(self):
        """When the draggable is latched to the cursor, this is carried out. 
        By default it moves the draggable along with the cursor. TODO: Correct
        the unintentional displacement of the draggable if the mouse was moved 
        quickly right before dragging the box"""
        translation = Base.tuple_add(pygame.mouse.get_pos(), self.previous_pos, '-')
        self.Translate(translation, None, True)
        self.previous_pos = pygame.mouse.get_pos()
    
    def OnCursorDetach(self):
        """When the drag operation is cancelled [generally by releasing the
        mouse button] this is carried out""" 
        self.Dragged = False
        if self.Snap:
            return self._SnapTo()
        return None
        
    def SetSnapTo(self, Sprites, Snap = True):
        """Set the sprites to which you want the draggable to snap on being 
        dropped, if this is desirable"""
        self.SnapSprites = Sprites
        self.Snap = Snap
        
    def _SnapTo(self):
        for sprite in self.SnapSprites:
            if pygame.sprite.collide_rect(self.Sprite, sprite):
                self.Recenter(sprite.rect.center)
                return sprite
        return None

    def DragEvent(self, event):
        """Recognize the stages of the drag event [click, drag, release] and 
        notify the calling class that the drag has occurred"""
        if self.Dragged:
            if event.type == MOUSEMOTION:
                self.OnDrag()
        if self.CursorOver():
            if event.type == MOUSEBUTTONDOWN:
                self.OnCursorLatch()
                return True
            if event.type == MOUSEBUTTONUP:
                self.OnCursorDetach()
                return True
        return False
    
    def Update(self):
        return GameObject.Update(self)