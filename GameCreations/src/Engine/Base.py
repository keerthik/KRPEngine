import os, sys, pygame
import math
from pygame.locals import *
# from numpy import *
from random import *
DISP_SIZE = (1200, 700)
RES_PATH = 'ImageData' 

if not pygame.font:
    print "Warning, Fonts disabled!"

if not pygame.mixer:
    print "Warning, Sound disabled!"

def Exit():
    sys.exit()

def set_resource_path(path):
    global RES_PATH
    RES_PATH = path

def load_image(name, colourkey = None):
    fullname = os.path.join(RES_PATH,name)
    try:
        image = pygame.image.load(fullname) 
#        print "Loading Resource - Image:", fullname
    except pygame.error, message:
        print "Cannot load image: ", name
        raise SystemExit, message
    image = image.convert()
    if colourkey:
        if colourkey == -1:
            colourkey = image.get_at((0,0))
        image.set_colorkey(colourkey, RLEACCEL)
    return image, image.get_rect()

#def ExtractImageList(imagelist):
#    imagename = 

def load_sound(name):
    class NoneSound:
        def play(self):pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data',name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "Cannot Load sound:", name
        raise SystemExit, message
    return sound


def tuple_add(t1,t2,operation = '+'):
    """ Performs operation on 2-tuples t1 and t2,
        element-wise. Default operation is '+'
        Returns a 2-tuple.
    """
    if operation == '-':
        return (t1[0]-t2[0],t1[1]-t2[1])    
    elif operation == '*':
        return (t1[0]*t2[0],t1[1]*t2[1])
    elif operation == '/':
        return (t1[0]/t2[0],t1[1]/t2[1])
    elif operation == '%':
        return (t1[0]%t2[0],t1[1]%t2[1])
    else:
        return (t1[0]+t2[0],t1[1]+t2[1])    

def mean(L):
    mean = 0.0
    for i in L:
        mean += i
    mean /=len(L)
    return mean

def mag(P):
    """ Calculate magnitude of a vector"""
    retval = 0.0
    for x in P:
        retval += x**2
    retval**=0.5
    return retval

def normalize(P):
    """ Return a normal a vector, of magnitude 1 in the direction of given vector"""
    try:
        return tuple_add(P,[mag(P)]*2,'/')
    except:
        return (0, 0)

def distance(P1, P2):
    """ Give the distance between two positions """
    if len(P2) != len(P1):
        return None
    distance = 0
    for i in range(len(P1)):
        distance += float((P1[i]-P2[i])**2) 
    return distance**0.5

def tuple_lim(t, xlim, ylim, wrap = False):
    """ Limits the 2-tuple elements to xlim and ylim,
        and wraps through zero if 'wrap' is True
    """
    t = list(t)
    try:
        xlim[1]
    except:
        xlim = (0,xlim)         
    try:
        ylim[1]
    except:
        ylim = (0, ylim)

    t[0] = Limit(t[0], xlim, wrap)
    t[1] = Limit(t[1], ylim, wrap)

    return tuple(t)

def Limit(n, bounds, wrap = False):
    return limit(n, bounds[0], bounds[1], wrap)

def limit(n, lower, upper, wrap = False):
    if upper < lower:
        print "Valid region for limit negative: ", upper, "<", lower
    if n<=upper and n>=lower:return n
    if n<lower:
        if wrap:return (upper - (lower - n))
        else:return lower 
    if n>upper:
        if wrap:return (lower + (n-upper))
        else:return upper
    
#===============================================================================

class OrderedRenderPlain(pygame.sprite.OrderedUpdates):
    """ Wrapper class around the pygame RenderPlain group class
        to provide for ordered drawing of the sprites"""
    def __init__(self,sprites):
        pygame.sprite.RenderUpdates.__init__(self, self.sprites)
        
    def Update(self):
        pygame.sprite.RenderUpdates.update(self)
        
    def Draw(self, *argsv):
        pygame.sprite.RenderUpdates.draw(self, *argsv)
