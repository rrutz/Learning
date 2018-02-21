import numpy as np
import pygame as pg

class World():
    
    def __init__( self, width = 4, height = 4 ):
        self.images = {}
        self.__loadImages__()
        self.screen = pg.display.set_mode((width * 114, height * 139))
        self.titles = []
        for y in range( height ):
            self.titles.append([])
            for x in range( width ):
                self.titles[y].append( Title( x * 114, y *139  ) )
        self.titles[ np.random.randint(0, height)][ np.random.randint(0, width)].hasGold = True
        self.titles[ np.random.randint(0, height)][ np.random.randint(0, width)].hasWumpus = True
        self.titles[0][0].hasPit = False
        for row in range(height):
            for col in range(width):
                self.titles[row][col].getNeighInfo(self.titles, row, col)
        
    def __loadImages__( self ):
        self.images["pit"] =  pg.image.load("C:\\Users\\Ruedi\\OneDrive\\School\\University of Toronto\\AI\\wumpus\\pit.png")
        self.images["grass"] =  pg.image.load("C:\\Users\\Ruedi\\OneDrive\\School\\University of Toronto\\AI\\wumpus\\grass.png")
        self.images["gold"] =  pg.image.load("C:\\Users\\Ruedi\\OneDrive\\School\\University of Toronto\\AI\\wumpus\\gold.png")
        self.images["badGuy"] =  pg.image.load("C:\\Users\\Ruedi\\OneDrive\\School\\University of Toronto\\AI\\wumpus\\badGuy.png")
        

        
    def draw( self ):
        for row in self.titles:
            for title in row:
                title.draw(self.screen, self.images)
    
class Title():
    def __init__( self, x, y ):
        self.hasGold = False
        self.hasWumpus = False
        self.hasPit = np.random.binomial( n = 1, p = 0.2)
        self.x = x
        self.y = y
        self.isRevealed = False
    
    def getNeighInfo(self, titles, row, col):
        self.breeze = False
        self.stench = False
        if( self.hasPit or self.hasWumpus ):
            return()
        for rowOffset in [-1,0,1]:
            if( row + rowOffset > 0 and  row + rowOffset < 4 ):
                for colOffset in [-1,0,1]:
                    if( col + colOffset > 0 and  col + colOffset < 4 and ( np.abs(colOffset) + np.abs(rowOffset ) ==1 )):
                        if titles[ col + colOffset ][  row + rowOffset ].hasWumpus:
                            self.stench = True
                        if titles[ col + colOffset ][  row + rowOffset ].hasPit:
                            self.breeze = True
        
        
    def draw(self, screen, images ):
        if not(self.isRevealed):
            pg.draw.rect( screen, (90,90,90), pg.Rect(self.x, self.y,139,114 ))
        elif( self.hasGold ):
            screen.blit( images["gold"], dest = (self.x, self.y) )
        elif ( self.hasPit ):
            screen.blit( images["pit"], dest = (self.x, self.y) )
        elif ( self.hasWumpus ):
            screen.blit( images["badGuy"], dest = (self.x, self.y) )
        else:
            screen.blit( images["grass"], dest = (self.x, self.y) )
        
            
        

class Guy():
    def __init__(self):
        self.bordPos = np.array( [0,0])
        self.x = 0
        self.y = 0
        self.hasGold = False
        self.image =  pg.image.load("C:\\Users\\Ruedi\\OneDrive\\School\\University of Toronto\\AI\\wumpus\\guy.png")
        self.alive = True
        self.knowledge = { "bre" : [] }
    
    def move(self, dx, dy, screen ):
        self.x += dx * self.image.get_rect().size[1]
        self.y += dy* self.image.get_rect().size[0]
        self.bordPos += np.array( [ dx, dy ])
        
        if( self.x < 0 or self.x > pg.display.Info().current_w -  self.image.get_rect().size[1] ):
            print( "Hit wall" )
            self.x -=  dx * self.image.get_rect().size[1]
            self.bordPos -= np.array( [ dx, dy ])
        if( self.y < 0 or self.y > pg.display.Info().current_h -  self.image.get_rect().size[0] ):
            print( "Hit wall" )
            self.bordPos -= np.array( [ dx, dy ])
            self.y -= dy* self.image.get_rect().size[0]
        return(self.bordPos)
 
    def checkGoal( self, world ):
        if world.titles[ self.bordPos[1]][self.bordPos[0] ].hasPit:
            print( "fell into pit" )
            self.alive = False
        if world.titles[ self.bordPos[1]][self.bordPos[0] ].hasWumpus: 
            print("you were eaten")
            self.alive = False
        if world.titles[self.bordPos[1]][self.bordPos[0] ].hasGold: 
            print("you win")
            self.alive = False
        
    def draw(self, screen ):
        screen.blit( self.image, dest = (self.x, self.y))

    

            
def __main__():
    pg.init()
    world = World()
    guy = Guy()
    done = False
    pos = np.array( [0, 0])
    while( not done ):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                pos = guy.move( 0, -1, world.screen )
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                pos = guy.move( 0, 1, world.screen )
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                pos = guy.move( -1,0, world.screen )
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                pos = guy.move( 1,0, world.screen )
        
        world.titles[ pos[1]][ pos[0]].isRevealed = True    

        world.screen.fill((0, 0, 0))
        world.draw()
        guy.draw(world.screen)
        guy.checkGoal(world)
        pg.display.flip()
        
        if not(guy.alive):
            done = True
    
__main__()
