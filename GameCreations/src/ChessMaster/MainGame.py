import pygame
import Engine.Base as Base
from Engine.Game import Game
from Engine.Menu import Menu, MenuItem
from Engine.GameElements import GameplayObjects, GameSprite, GameObject, AnimationList
from pygame.locals import *
import math

class ChessGame(Game):
    def __init__(self):
        Game.__init__(self, "Chess Master!", False, (0, 0, 20), (1024, 700))
        Base.set_resource_path('Resources')
        self.offscreen = self.screen.get_size()
        self.Menu = ChessMenu(self.screen)
        
    def Init(self):
        Game.Init(self)
        Board = ChessBoard(self.screen)
        BlackPieces = Pieces(self.screen, False)
        FullBoard = GameplayObjects(self.screen, Board)
        self.AddFeature("FullBoard", FullBoard)
        print Board.GetTileCenter(0,0)
        
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

class Piece(GameObject):
    def __init__(self, screen, pieceID = 0, iswhite = True):        
        if pieceID < 8: Name = "Pawn"; Image = "Pawn.png"
        elif pieceID == 8 or pieceID == 15: Name = "Rook"; Image = "Rook.png"
        elif pieceID == 9 or pieceID == 14: Name = "Knight"; Image = "Knight.png"
        elif pieceID == 10 or pieceID == 13: Name = "Bishop"; Image = "Bishop.png"
        elif pieceID == 11: Name = "Queen"; Image = "Queen.png"
        elif pieceID == 12: Name = "King"; Image = "King.png"
        
        GameObject.__init__(self, Name, screen, Image)
        self.pieceID = pieceID
        self.isWhite = iswhite
        
        self.Row = 0
        self.Col = 0
        self.SetInitialPos()
        
    def SetInitialPos(self, Board = (8,8)):
        if self.isWhite: self.Row = Board[2]-1-(pieceID<8)
        else: self.Row = int(pieceID<8)
        self.Col = self.pieceID%Board[0]
        
class ChessBoard(GameObject):
    def __init__(self, screen):
        GameObject.__init__(self, "Board", screen, "shell.png")
        self.tile_width = 50
        self.tile_height = 50
        
    def GetTileCenter(self, *argsv):
        position = [0, 0]
        if len(argsv) == 1:
            arg = argsv[0]
            col = arg[0]
            row = arg[1]
        else:
            col = argsv[0]
            row = argsv[1]
        offset = self.Sprite.rect.topleft
        position[0] = int((col+0.5)*self.tile_width)
        position[1] = int((row+0.5)*self.tile_height)
        position = Base.tuple_add(position, offset)
        return position
                

class ChessMenu(Menu):
    def __init__(self, surface):
        Menu.__init__(self, surface, [], "Chess Master! Main Menu", Nshown = 5)
        self.AddMenuItem(MenuItem("New Game", (0, 255, 0), "NewGame"))
        self.AddMenuItem(MenuItem("Resume Game", (0, 255, 0), "Continue"))
        self.AddMenuItem(MenuItem("Settings", (0, 255, 0), "Settings"))
        self.AddMenuItem(MenuItem("Sync Database", (0, 255, 0), "Sync"))
        self.AddMenuItem(MenuItem("Exit", (0, 255, 0), "Exit"))
        self.Highlight(0)

def LaunchGame():
    print "Launching TankWars!..."
    game = ChessGame()
    game.RunGame()
    
if __name__ == "__main__":
    LaunchGame()