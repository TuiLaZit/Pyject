import pyxel as px
class Player:
    IMG = 0
    U = 0
    V = 0
    WIDTH = 16
    HEIGHT = 16
    DX = 4
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 1
        self.blockx= x//16
        self.blocky= y//16

    def move_left(self):
        self.x -= self.DX

    def move_right(self):
        self.x += self.DX

    def falling(self):
         if not self.onground():
            self.velocity += self.gravity
            self.y += self.velocity
            if self.onground():
                self.y = (self.y // 16)*16
    
    def border_left(self):
        if(self.x==0):
            return False
        else:
            return True
        
    def border_right(self,x):
        if(self.x+16==x):
            return False
        else:
            return True
    
    def jump(self):
        if self.onground():
            self.velocity = -13
            self.y += self.velocity
    
    def onground(self):
        botY=self.y+16
        for x in range(self.x, self.x + self.WIDTH):
            if (px.pget(self.x,botY)!=3):
                return True
        return False

            
class Brick:
    IMG = 0
    U = 16
    V = 16
    WIDTH = 16
    HEIGHT = 16
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def placeBrick(self,blockx,blocky):
        self.Brick = Brick(blockx,blocky)
        px.blt(
            self.Brick.x*16,
            self.Brick.y*16,
            self.Brick.IMG,
            self.Brick.U,
            self.Brick.V,
            self.Brick.WIDTH,
            self.Brick.HEIGHT,
        )

class Platform:
    IMG = 0
    U = 32
    V = 16
    WIDTH = 16
    HEIGHT = 16
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def placePlatform(self,blockx,blocky):
        self.Platform=Platform(blockx,blocky)
        px.blt(
            self.Platform.x*16,
            self.Platform.y*16,
            self.Platform.IMG,
            self.Platform.U,
            self.Platform.V,
            self.Platform.WIDTH,
            self.Platform.HEIGHT,
            3
        )

class App:
    def __init__(self):
        self.maxblockx=20
        self.maxblocky=15
        self.maxx = self.maxblockx * 16
        self.maxy = self.maxblocky * 16
        self.drawcheck = False 
        self.savedPlatform =[]
        px.init(self.maxx,self.maxy, title="Hello World")
        px.load("project.pyxres")
        self.Brick = Brick(0,0)
        self.player = Player(16,0)
        px.run(self.update, self.draw) 
                
    def drawMap(self):
        #draw the bottom platform
        for i in range(0,self.maxblockx):
            self.Brick.placeBrick(i,self.maxblocky-1)
            self.savedPlatform.append((i,self.maxblocky-1))
        #draw random platforms
        for i in range (self.maxblocky-1,i>0,-4):
            xr=px.rndi(0,self.maxblockx-2)
            self.Brick.placeBrick(xr,i)
            self.savedPlatform.append((xr,i))

    def update(self):
        if not self.player.onground():
            self.player.falling()
        else:
            self.player.velocity=0
        if px.btn(px.KEY_LEFT):
            if self.player.border_left():
                self.player.move_left()
        if px.btn(px.KEY_RIGHT):
            if self.player.border_right(self.maxx):
                self.player.move_right()
        if px.btnp(px.KEY_UP):
            if self.player.onground() and not self.player.falling():
                self.player.jump()

    def draw(self):
        px.cls(3)
        if not self.drawcheck:
            self.drawMap()
            self.drawcheck = True
        for x, y in self.savedPlatform:
            self.Brick.placeBrick(x,y)
        px.blt(
            self.player.x,
            self.player.y,
            self.player.IMG,
            self.player.U,
            self.player.V,
            self.player.WIDTH,
            self.player.HEIGHT,
            3
        )


App()