'''
Created on Mar 1, 2011

@author: keerthik
'''
from Engine import Base
from Engine.GameElements import GameObject
from Engine.UI import UI, UIitem, UIDraggable

class HiveUI(UI):
    def __init__(self, surface):
        UI.__init__(self, surface)
        self.levels = 1
        self.makeUI()
        
    def makeUI(self):
        last = Base.tuple_add(self.surf.get_rect().center, (-(111+self.levels*75), -75/2))
        Start = GameObject("Start", self.surf, "code-start.png", last)
        self.Add(Start)
        start_code = Base.tuple_add(last, (75*2, 0))
        self.draw_branch(start_code)
        Code1 = CodeElement("Code1", "def cond1(self):\n\
        if len(self.Enemies) > len(self.Allies):\n\
            return True\n\
        else:\n\
            return False#dividercond1", self.surf, "code-start.png", (10,10))
        Code2 = CodeElement("Code2", "Retreat", self.surf, "code-start.png", (100,10))
        Code3 = CodeElement("Code3", "Attack", self.surf, "code-start.png", (190,10))
        Code1.SetSnapTo(self.get_container_sprites(),True)
        Code2.SetSnapTo(self.get_container_sprites(),True)
        Code3.SetSnapTo(self.get_container_sprites(),True)
        self.Add(Code1, Code2, Code3)
        Compile = UIitem("Compile", self.surf, "code-start.png", Base.tuple_add(self.surf.get_size(), (-100,-100)))
        Compile.SetOnClick({"Action": "Compile"})
        self.Add(Compile)
    
    def CompileCode(self):
        print "Compiling..."
        file = open('condition1.py', 'w')
        code = self.makeTreeCode("CB0-0", "self.Tree")
        file.truncate(0)
#        file.close
#        file = open('condition1.py')
        file.write(code)
        file.close()
        print "Compiled code:\n", code
        return True
    
    def makeTreeCode(self, startpoint, treename = "UnnamedTree"):        
        children = self.getChildren(startpoint, True)
        this_code = self.Get(startpoint).Code
        #If this is a terminal node, return terminus code
        if children == None:
            return ''
#            return this_code + '\n'
        this_condcode, this_condname = this_code.split("#divider")
        
        #Condition goes before the decision tree statement
        code = this_condcode + '\n'
        
        #The code ends with a decision tree statement
        code += treename + " = DecisionTree("

        if self.getChildren(children[0].Name, True) != None:
            c0_treename = children[0].Name.replace('-','')
        else:
            c0_treename = children[0].Code
        if self.getChildren(children[1].Name, True) != None:
            c1_treename = children[1].Name.replace('-','')
        else:
            c1_treename = children[1].Code
        code += c0_treename + ', '
        code += this_condname + ', ' 
        code += c1_treename + ')\n'
        code =  self.makeTreeCode(children[0].Name, c0_treename) + self.makeTreeCode(children[1].Name, c1_treename) + code
        return code
    
    def getChildren(self, parentName, Coded = False):
        level, id = parentName.split("CB")[-1].split('-')
        c_lvl = str(int(level)+1)
        name1, name2 = self.getCodeName(c_lvl, int(id)**2), self.getCodeName(c_lvl, int(id)**2+1)
        try:
            if Coded:
                if self.Get(name1).Code == None or self.Get(name2).Code == None:
                    return None                   
            return self.Get(name1), self.Get(name2)
        except:
            return None
                
    def getCodeName(self, level, id):
        return "CB"+str(level)+"-"+str(id)
    
    def getCodeBox(self, in_sprite):
        for i in range(self.levels+1):
            for j in range(2**i):
                obj = self.Get(self.getCodeName(i, j))
                if in_sprite is obj.Sprite:
                    return obj
        return None
    
    def get_container_sprites(self):
        sprites = []
        for i in range(self.levels+1):
            for j in range(2**i):
                sprites.append(self.Get(self.getCodeName(i, j)).Sprite)
        return sprites
    
    def draw_branch(self, pos, level = 0, id = 0, true_branch = True):
        #draw the condition blocks
        self.Add((CodeContainer(self.getCodeName(level, id), self.surf, pos)))
        spread = 75*(2**(self.levels-level-2))
        truepos = Base.tuple_add(pos, (75*2, -spread))
        falsepos = Base.tuple_add(pos, (75*2, spread))
            
        if level == self.levels-1:
            self.Add(CodeContainer(self.getCodeName(level+1, 2*id), self.surf, truepos))
            self.Add(CodeContainer(self.getCodeName(level+1, 2*id+1), self.surf, falsepos))
            return id+1
        else:
            self.draw_branch(truepos, level + 1, 2*id, True)
            self.draw_branch(falsepos, level + 1, 2*id+1, False)
        
    def draw_connectors(self):
        start = self.Get("Start").Sprite.rect.midright
        for i in range(self.levels+1):
            for j in range(2**i):
                if i >0 and j%2 == 0:start = self.Get(self.getCodeName(i-1, str(j/2))).Sprite.rect.midright
                end = self.Get(self.getCodeName(i, str(j))).Sprite.rect.midleft
                pygame.draw.aaline(self.surf, (255,100,0), start, end, 20)
        
    def draw(self):
        if self.Uishow:
            self.draw_connectors()
            self.Drawables.draw(self.surf)
        return True        

class CodeContainer(UIitem):
    def __init__(self, Name, surf, position = (0,0)):
        base_image = "code-box.png"
        UIitem.__init__(self, Name, surf, base_image, position)
        self.Code = None
        self.ConditionCode = None
            
    def setCode(self, code):
        self.Code = code
        return True
    
class CodeElement(UIDraggable):
    def __init__(self, Name, code, surf, base_image, position = (0,0)):
        UIDraggable.__init__(self, Name, surf, base_image, position)
        self.ReturnBundle["Code"] = code
        self.ReturnBundle["PickupZone"] = None
        self.ReturnBundle["DropZone"] = None
        
    def OnDrag(self):
        UIDraggable.OnDrag(self)
        self.ReturnBundle["Action"] = "Dragged"
        
    def OnCursorLatch(self):
        UIDraggable.OnCursorLatch(self)
        self.ReturnBundle["PickupZone"] = self.ReturnBundle["DropZone"]
        self.ReturnBundle["Action"] = "Picked"
        
    def OnCursorDetach(self):
        self.ReturnBundle["DropZone"] = UIDraggable.OnCursorDetach(self)
        self.ReturnBundle["Action"] = "Dropped"
