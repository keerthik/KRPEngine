from Engine.UI import UI, UIitem, UIDraggable
import Engine.Base

TOP = 0
RIGHT = 1
BOT = 2
LEFT = 3 

class PRObotUI(UI):
    def __init__(self, surface):
        UI.__init__(self, surface)
        
        Forwards = UIitem("DFS", self.surf, "forward.bmp")
        Forwards.SetToolTip("Code to move the robot forward")
        self.Add(Forwards)
        self.SetOnClick("DFS", ["GenDrag", "Fd"])
        
        Jumps = UIitem("DJS", self.surf, "jump.bmp")
        Jumps.SetToolTip("Code to make the robot jump forward if its a different elevation")
        self.Add(Jumps)
        self.SetOnClick("DJS", ["GenDrag", "Jp"])

        GoButton = UIitem("Go", self.surf, "run.bmp")
        GoButton.SetToolTip("This button runs the robot code")
        self.Add(GoButton)
        self.SetOnClick("Go", "Go")
                
        self.MakeUI(self.GetUIitems(), BOT)            
        
class RunTable(UI):
    def __init__(self, surface):
        UI.__init__(self, surface)
        
        for i in range(5):
            Runbox = UIitem("R"+str(i), self.surf, "run.bmp")
            self.Add(Runbox)
        
        self.MakeUI(self.GetUIitems(), BOT)