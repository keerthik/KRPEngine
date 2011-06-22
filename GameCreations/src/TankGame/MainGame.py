import time
import ctypes
import random

import pygame
import Engine.Base as Base
from Engine.Game import Game
from Engine.Menu import Menu, MenuItem
from Engine.GameElements import GameplayObjects, GameSprite, GameObject, AnimationList
from pygame.locals import *
import math

class TankGame(Game):
    def __init__(self):
        Game.__init__(self, "Tank Wars!", False, (100, 100, 255), (1024, 700))
        self.Menu = TankMenu(self.screen)

    def init_USB(self):
        self.GET_DATA=1
        self.usb = ctypes.cdll.LoadLibrary('usb.dll')
        self.usb.initialize()
        self.buffer = ctypes.c_buffer(8)
        self.dev = self.usb.open_device(0x6666, 0x0003)
        if self.dev<0:
            print "No matching device found...\n"
        else:
            ret = self.usb.control_transfer(self.dev, 0x00, 0x09, 1, 0, 0, self.buffer)
            if ret<0:
                print "Unable to send SET_CONFIGURATION standard request.\n"

    def Init(self):
        Game.Init(self)
        self.init_USB()

        Base.set_resource_path('Resources')
        offscreen = self.screen.get_size()

        T1Gun = TankGun(self.screen, offscreen)
        T2Gun = TankGun(self.screen, offscreen)
        
        T1Power = TankPBar(self.screen, (10,10))
        T2Power = TankPBar(self.screen, (self.screen.get_width()-60,10))
        
        Shell1 = Shell("Shell1", self.screen, "LShell.PNG", True, offscreen)
        Shell2 = Shell("Shell2", self.screen, "RShell.PNG", False, offscreen)

        Tank1 = Tank("T1", self.screen, "LTank.PNG", T1Gun, T1Power, Shell1, True, (9,85), offscreen)
        Tank2 = Tank("T2", self.screen, "RTank.PNG", T2Gun, T2Power, Shell2, False, (9,85), offscreen)
        Tank1.Reposition((70,self.screen.get_height()-Tank1.Size()[1]-25))
        Tank2.Reposition((self.screen.get_width()-Tank2.Size()[0]-70,
                          self.screen.get_height()-Tank2.Size()[1]-25))
        Tanks = GameplayObjects(self.screen, Tank1, Tank2)
        
        Shell1.AddAnimationList("Explode", AnimationList(["Explo_"+str(i+1)+".PNG" for i in range(20)]))
        Shell2.AddAnimationList("Explode", AnimationList(["Explo_"+str(i+1)+".PNG" for i in range(20)]))
        Shells = GameplayObjects(self.screen, Shell1, Shell2)
        shells = ([Shells.Get("Shell1"), Shells.Get("Shell2")])
        tanks = ([Tanks.Get("T1"),Tanks.Get("T2")])
        Checker = HitCheck(shells, tanks)
        
        self.AddFeature("T1Gun", T1Gun)
        self.AddFeature("T2Gun", T2Gun)
        self.AddFeature("T1Pbar", T1Power)
        self.AddFeature("T2Pbar", T2Power)
        self.AddFeature("Tanks", Tanks)
        self.AddFeature("Shells", Shells)
        self.AddFeature("Global", Checker)
        
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

    def UserEventHandle(self):
        """Function overwrite for our special USB flavour of game"""
                
        self.usb.control_transfer(self.dev, 0xC0, self.GET_DATA, 0, 0, 3, self.buffer)
        Trigger = ord(self.buffer[0]);
        Wheel = ord(self.buffer[1]);
        Tilt = ord(self.buffer[2]);

        Launch = False
        if Trigger > 0:
            Launch = True
        if not self.Menu.isActive():
            T2 = self.Get("Tanks").Get("T2")
            T2.SetAngle(self.T2A(Tilt))
            T2.SetPower(int(float(Wheel)/4))
            if Launch:T2.Fire()
#            if self.Get("Global").GameOver:
#                self.PauseGame()
#                self.Menu.Activate()
        
        return Game.UserEventHandle(self)
    
    def T2A(self, Tilt):
        angle = 45
        if (Tilt==4):
            angle=10
        elif (Tilt==6):
            angle=22
        elif (Tilt==7):
            angle=34
        elif (Tilt==67):
            angle=40
        elif (Tilt==65):
            angle=52
        elif (Tilt==193):
            angle=58
        elif (Tilt==192):
            angle=64
        elif (Tilt==128):
            angle=76
        return angle

    def HandleGameEvent(self, event):
        if event.type == QUIT:
            print "Requesting quit"
            return False
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                T1 = self.Get("Tanks").Get("T1") 
                T1.StopAiming()
                return True
            if event.key == K_UP or event.key == K_DOWN:
                T2 = self.Get("Tanks").Get("T2")
                T2.StopAiming() 
                return True
        
            if event.key == 113 or event.key == 97:
                T1 = self.Get("Tanks").Get("T1") 
                T1.StopPowering()
                return True
            if event.key == 93 or event.key == 39:
                T2 = self.Get("Tanks").Get("T2")
                T2.StopPowering() 
                return True
            
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.PauseGame()
                print "Pausing and navigating to menu"
                self.Menu.Activate()
                return True
            
            if event.key == K_LSHIFT:
                T1 = self.Get("Tanks").Get("T1")
                T1.Fire()
                return True
            if event.key == K_RSHIFT:
                T2 = self.Get("Tanks").Get("T2")
                T2.Fire()
                return True
            
            if event.key == K_LEFT:
                T1 = self.Get("Tanks").Get("T1") 
                T1.Aiming(True)
                return True
            if event.key == K_RIGHT:
                T1 = self.Get("Tanks").Get("T1")
                T1.Aiming(False)
                return True
            if event.key == K_UP:
                T2 = self.Get("Tanks").Get("T2")
                T2.Aiming(True) 
                return True
            if event.key == K_DOWN:
                T2 = self.Get("Tanks").Get("T2")
                T2.Aiming(False)
                return True
            
            if event.key == 113:
                T1 = self.Get("Tanks").Get("T1") 
                T1.Powering(True)
                return True
            if event.key == 97:
                T1 = self.Get("Tanks").Get("T1")
                T1.Powering(False)
                return True
            if event.key == 93:
                T2 = self.Get("Tanks").Get("T2")
                T2.Powering(True) 
                return True
            if event.key == 39:
                T2 = self.Get("Tanks").Get("T2")
                T2.Powering(False)
                return True
        
        return True

class TankPBar():
    def __init__(self, screen, position = (0,0)):
        self.Surf = screen
        self.position = position
        self.size = (50, 200)
        self.rect = (self.position, self.size)
        self.Value = 0
    
    def SetVal(self, Val):
        self.Value = Val
    
    def GetVal(self):
        return self.Value
    
    def draw(self):
        pygame.draw.rect(self.Surf,(0,0,0), self.rect, 5)
        pygame.draw.rect(self.Surf,(255,0,0), self.FillRect, 0)
        return True
        
    def update(self):
        percent = int(math.ceil(190*(float(self.Value)/50)))
        TopLeft = Base.tuple_add(self.rect[0], self.rect[1])
        TopLeft = Base.tuple_add(TopLeft,(-45,-percent-5))
        self.FillRect = (TopLeft, (40, percent))
        return True
                
class HitCheck():
    """A class to global updating"""
    def __init__(self, shells, tanks):
        self.shells = pygame.sprite.Group(shells)
        self.tanks = tanks
        self.GameOver = False
        
    def draw(self):
        "Game over splash"
        if self.GameOver:
            """hi"""
#            print "Game Over Spash Screen here!"
        return True
    
    def update(self):        
        self.GameOver = False
        for tank in self.tanks:            
            if pygame.sprite.spritecollideany(tank.Sprite, self.shells):
                self.GameOver = True
                print "GameOver!"
        return True

class Tank(GameObject):
    def __init__(self, Name, screen, image, Gun, Power, shell, facing = True, Arange = (0,180),position = (0,0)):
        GameObject.__init__(self, Name, screen, image, position)
        self.Facing = facing
        self.Gun = Gun
        self.shell = shell
    
        self.Arange = Arange
        self.Araisemode = False
        self.Alowermode = False

        self.Praisemode = False
        self.Plowermode = False
    
        self.Angle = 15
        self.Power = Power
        
    def Powering(self, Raising = True):
        self.StopPowering()
        if Raising: self.Praisemode = True
        else: self.Plowermode = True
    
    def StopPowering(self):
        self.Praisemode = False
        self.Plowermode = False

    def Aiming(self, Raising = True):
        self.StopAiming()
        if Raising: self.Araisemode = True
        else: self.Alowermode = True
    
    def StopAiming(self):
        self.Araisemode = False
        self.Alowermode = False
    
    def Fire(self):
        self.shell.Launch(self.Angle, self.Power.GetVal(), self.Gun.position)
        "Launch!"
        
#Internal operations, not expected to be called from anywhere else    
    def SetPower(self, power):
        self.Power.SetVal(Base.Limit(power, (1,50)))

    def SetAngle(self, angle):
        self.Angle = Base.Limit(angle, self.Arange)

    def RaisePower(self, increment = 5):
        self.SetPower(self.Power.GetVal()+increment)

    def LowerPower(self, decrement = 5):
        self.SetPower(self.Power.GetVal()-decrement)
        
    def RaiseAngle(self, increment = 5):
        self.SetAngle(self.Angle+increment)
    
    def LowerAngle(self, decrement = 5):
        self.SetAngle(self.Angle-decrement)
    
    def setGunPos(self):
        C = self.Sprite.rect.center
        try: xadd = int(math.ceil(20*math.cos(math.radians(self.Angle))))
        except: xadd = 0
        try: yadd = int(math.ceil(20*math.sin(math.radians(self.Angle))))
        except: yadd = 10
        if not self.Facing: xadd*=-1
        GunPos = Base.tuple_add(C, (xadd, -yadd))
        return GunPos
    
    def Update(self):
        GameObject.Update(self)
        if self.Araisemode:self.RaiseAngle()
        if self.Alowermode:self.LowerAngle()
        if self.Praisemode:self.RaisePower()
        if self.Plowermode:self.LowerPower()
        self.Gun.setPos(self.setGunPos())
        return True

class TankGun:
    def __init__(self, screen, position = (0,0)):
        self.Surf = screen
        self.position = position
    
    def setPos(self, position):
        self.position = position
        
    def update(self):
        return True
    
    def draw(self):
        pygame.draw.circle(self.Surf, (0,0,0), self.position, 5, 0)
        return True

class Shell(GameObject):
    def __init__(self, Name, screen, image, facing = True, position = (0,0)):
        GameObject.__init__(self, Name, screen, image, position)
        self.orig_im = self.Sprite.image
        self.orig_rect = self.Sprite.rect 
        self.Facing = facing
        self.Velocity = (0,0)
        self.Angle = 0
        self.Launched = False
    
    def isCrashed(self, ground = 25):
        if self.Launched:
            if self.Sprite.rect.center[1] >= self.Sprite.surf.get_height()-ground-self.orig_im.get_height():
                return True
        return False 
        
    def RotateTo(self, angle):
        self.Sprite.image=self.orig_im
        self.Sprite.image = pygame.transform.rotate(self.Sprite.image,-angle)
        
    def Launch(self, angle, power, position):
        self.Sprite.image = self.orig_im
        self.Sprite.rect = self.orig_rect
        if self.Launched:
            return True
        self.Angle = angle
        self.RotateTo(self.Angle)
        
        vx = int(math.ceil(power*math.cos(math.radians(angle))))
        vy = int(-math.ceil(power*math.sin(math.radians(angle))))
        if not self.Facing: vx*=-1
        self.Velocity = (vx, vy)
        self.Recenter(Base.tuple_add(position,self.Velocity))

        self.Launched = True
        self.LaunchCount = 0
        return True
    
    def step(self):
        if self.LaunchCount == 0:
            vx, vy = self.Velocity
            self.Translate(self.Velocity)
            self.Velocity = (vx, vy + 1)
            try:self.Angle = math.degrees(math.atan(float(vy+1)/vx))
            except:self.Angle = 90
            self.RotateTo(self.Angle)
        self.LaunchCount = Base.limit(self.LaunchCount+1, -1, 1, True)

    def Update(self):
        if self.Launched and not self.isCrashed():
            self.step()
        if self.isCrashed():
            self.SetUpdateState("Exploded")
        if self.GetUpdateState() == "Exploded":
            self.Animate("Explode", 1, False)
        if self.GetUpdateState() == "Idle" and self.isCrashed():
            self.Launched = False
            self.Reposition(self.Sprite.surf.get_size())      
        return GameObject.Update(self)
        
class TankMenu(Menu):
    def __init__(self, surface):
        Menu.__init__(self, surface, [], "Tank Wars! Main Menu", Nshown = 5)
        self.AddMenuItem(MenuItem("New Game", (0, 255, 0), "NewGame"))
        self.AddMenuItem(MenuItem("Resume Game", (0, 255, 0), "Continue"))
        self.AddMenuItem(MenuItem("Exit", (0, 255, 0), "Exit"))
        self.Highlight(0)
        
def LaunchGame():
    print "Launching TankWars!..."
    game = TankGame()
    game.RunGame()
    game.usb.close_device(game.dev)

if __name__ == "__main__":
    LaunchGame()