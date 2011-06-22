import Base
import pygame
from pygame.locals import *

class GameplayObjects():
    """ A structure containing a set of game objects. It contains a sprite-list
        as well as a  list of the game objects to call update from"""
    def __init__(self, surf, *gameElements):
        self.Drawables = pygame.sprite.OrderedUpdates()
        self.GameObjects = {}
        for gameElement in gameElements:
            self.Add(gameElement)
        self.surf = surf

    def Add(self, *gameObjects):
        for gameObject in gameObjects:
            try:
                self.GameObjects[gameObject.Name] = gameObject
                self.Drawables.add(gameObject)
            except:
                print "Unable to add game object "+gameObject.Name
    
    def Remove(self, objectName):
        try:
            self.GameObjects.pop(objectName).Sprite.kill
        except:
            print "Unable to remove game object "+objectName
    
    def PrintAll(self):
        #Debugging tool
        print len(self.GameObjects.values()),self.GameObjects.values() 
        
    def GetAll(self):
        return self.GameObjects.values()
    
    def Get(self, objectname):
        return self.GameObjects[objectname]
    
    def update(self):
        self.Drawables.update()
        returnval = True
        for object in self.GameObjects.values():
            returnval = returnval and object.update()
        return returnval
    
    def draw(self):
        self.Drawables.draw(self.surf)
        return True

class AnimationList():
    """ Supports sprite animation using a list of images and 
        animating them by flipping through them 
    """
    def __init__(self, imagelist = []):
        self.ImageList = imagelist
        self.counter = 0
        self.Running = False
        
    def AddImage(self, image):
        self.ImageList.append(image)
    
    def AddImages(self, images):
        self.ImageList.extend(images)
    
    def Init(self, Sprite):
        self.counter = 0
        Sprite.ChangeImage(self.ImageList[self.counter])
        self.Running = True
    
    def Run(self, Sprite, period = 5, loop = True):
        self.counter += 1
        if self.counter == period*len(self.ImageList):
            if loop:
                self.counter = 0
            else:
                self.Running = False
        try:Sprite.ChangeImage(self.ImageList[self.counter/period])
        except:pass
            
    def Animate(self, Sprite, period = 5, loop = True):
        if self.Running:
            self.Run(Sprite, period, loop)
        else:
            self.Init(Sprite)
    
    def Stop(self):
        self.Running = False
        self.counter = 0
    
    def Pause(self):
        self.Running = False
    
    def Unpause(self):
        self.Running = True


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, screen, base_image = None, position = (0,0)):
        pygame.sprite.Sprite.__init__(self)
        if base_image:
            self.image, self.rect = Base.load_image(base_image, -1)
            self.src = base_image
        self.surf = screen
        self.position = position
        self.rect.topleft = self.position
        self.translate_residue = [0.0, 0.0]
        
    def ChangeImage(self, newImage):
        oldcenter = self.rect.center
        self.image, self.rect = Base.load_image(newImage, -1)
        self.src = newImage
        self.rect.center = oldcenter
        self.position = self.rect.topleft        
    
    def Reposition(self, position):
        self.rect.topleft = position
        
    def Recenter(self, position):
        self.rect.center = position
        
    def Translate(self, reposition, translim = None, clip = False, wrap = False):
        """This accumulates residual float movement and uses it to move the sprite over calls"""
        if translim == None:
            limx, limy = Base.tuple_add(self.surf.get_size(), self.rect.size, '-')
        else:
            limx, limy = translim
        oldpos = self.rect.topleft
        #Accumulate residue from new repositioning
        Base.tuple_add(self.translate_residue, [r-int(r) for r in reposition])
        #Trim reposition of float portion
        reposition = [int(x) for x in reposition]
        #Update reposition to take whole residues
        reposition = Base.tuple_add(reposition, [int(r) for r in self.translate_residue])
        #Update residue to remove whole portion used in reposition
        self.translate_residue = [r-int(r) for r in self.translate_residue]
        
        want_to = Base.tuple_add(oldpos, reposition)
        self.rect.topleft = Base.tuple_lim(Base.tuple_add(oldpos, reposition), limx, limy, wrap)
        if not clip:
            self.rect.topleft = want_to
        if self.rect.topleft == want_to:
            return True
        else:
            return wrap or False
        
    def update(self):
        pygame.sprite.Sprite.update(self)
        return True


        
class GameObject(pygame.sprite.RenderPlain):        
    def __init__(self, Name, surf, base_image, position = (0,0)):
        self.Name = Name
        self.Sprite = GameSprite(surf, base_image, position)
        self.initialize()
        
    def initialize(self):
        pygame.sprite.RenderPlain.__init__(self, self.Sprite)
        self.AnimationsDict = {}
        self.UpdateState = "Idle"
        self.Clicked = False
    
    def Size(self):
        return self.Sprite.rect.size
        
    def size(self):
        return self.Size()
    
    def get_position(self):
        return self.Sprite.position
    
    def Reposition(self, position):
        self.Sprite.Reposition(position)

    def Recenter(self, position):
        self.Sprite.Recenter(position)
        
    def Translate(self, reposition,  translim = None, clip = False, wrap = False):
        self.Sprite.Translate(reposition, translim, clip, wrap)
        
    def CursorOver(self):
        return self.Sprite.rect.collidepoint(pygame.mouse.get_pos())
    
    def ClickEvent(self, event):
        if self.CursorOver():
            if event.type == MOUSEBUTTONDOWN:
                self.Clicked = True
                return False
            if event.type == MOUSEBUTTONUP:
                if self.CursorOver() and self.Clicked:
                    self.Clicked = False
                    return True
        return False

    def changeImage(self, newimage):
        self.Sprite.ChangeImage(newimage)
        
    def AddAnimationList(self, AnimationName = "Unnamed", AnimationList = None):
        self.AnimationsDict[AnimationName] = AnimationList
        
    def Animate(self, AnimName, *args):
        self.AnimationsDict[AnimName].Animate(self.Sprite, *args)
        if not self.AnimationsDict[AnimName].Running:
            self.SetUpdateState("Idle")
    
    def SetUpdateState(self, UpdateState):
        self.UpdateState = UpdateState

    def GetUpdateState(self):
        return self.UpdateState
    
    def update(self):
        return self.Update()
        
    def Update(self):
        if self.UpdateState == "Idle":            
            retVal = True
        return True        
    
    def Remove(self):
        self.Sprite.kill()

if __name__ == "__main__":
    print "Hello"