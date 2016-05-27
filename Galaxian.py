import os,pygame,sys,time,math,random
from pygame.locals import *

pygame.init()



size = width, height = 1000,600
black = 0,0,0
white = 255,255,255
sky = 0,0,40
clock = pygame.time.Clock()
FPS = 20
maxspeed = 15
gameOver = False

screen = pygame.display.set_mode(size)

"""jet = pygame.image.load("Sprites/fighter_scale.png").convert()
enemy = pygame.image.load("Sprites/enemy2_scale.png").convert()
colorkey = jet.get_at((0,0))
jet.set_colorkey(colorkey,pygame.RLEACCEL)
enemy.set_colorkey(colorkey,pygame.RLEACCEL)

jetrect = jet.get_rect()
enemyrect = enemy.get_rect()
jetrect.top = 500
jetrect.left = 200
enemyrect.top = 100
enemyrect.left = width/2

movejet = [0,0]
emovejet = [0,0]
speed = 0
espeed = 0

trigger = 0
etrigger = 0
"""

def cpumove(cpu,target):
    #rnd = random.randrange(0,2)
    """if rnd == 2:
        cpu.trigger = 1
        cpu.speed = 2
    elif rnd == 1:
        cpu.trigger = 1
        cpu.speed = -2
    elif rnd == 0:
        cpu.trigger = 2
        cpu.speed = 0
    """
    #if rnd == 0:
    if target.rect.left < cpu.rect.left:
        cpu.trigger = 1
        cpu.speed = -2
    elif target.rect.left > cpu.rect.left:
        cpu.trigger = 1
        cpu.speed = 2
    #else:
     #   cpu.trigger = 2
      #  cpu.speed = 0

def load_image(name, colorkey=None):
    fullname = os.path.join('Sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def moveplayer(Player):
    if Player.rect.left >= 0 and Player.rect.right <= width:
        if Player.trigger == 1:
            Player.move[0] = Player.move[0] + Player.speed
            if Player.move[0] < -maxspeed:
               Player.move[0] = -maxspeed
            elif Player.move[0] > maxspeed:
                Player.move[0] = maxspeed
        elif Player.move[0] >= -maxspeed and Player.move[0] < 0 and Player.trigger == 2:
            Player.move[0] += math.fabs(Player.move[0]/20)
            if Player.move[0] > 0:
                Player.move[0] = 0
        elif Player.move[0] <= maxspeed and Player.move[0] > 0 and Player.trigger == 2:
            Player.move[0] -= Player.move[0]/20
            if Player.move[0] < 0:
                Player.move[0] = 0
           
        
class stars():
    def __init__(self):
        self.starpos = [[0 for j in range(2)] for i in range(100)]
        for x in range(100):
            self.starpos[x][0] = random.randrange(0,width)
            self.starpos[x][1] = random.randrange(0,height)
        
    def drawstars(self):
        for x in range(100):
            pygame.draw.rect(screen, white, [self.starpos[x][0],self.starpos[x][1],2,2])
        self.movestars()
    def movestars(self):
        for x in range(100):
            self.starpos[x][1] += 5
            if self.starpos[x][1] > height:
                self.starpos[x][1] = 0
                
class player(pygame.sprite.Sprite):
    def __init__(self,isenemy=False):
        pygame.sprite.Sprite.__init__(self)
        if not isenemy:
            self.image, self.rect = load_image('fighter_scale.png',-1)
            self.rect.top = 500
            self.rect.left = 200
        else:
            self.image, self.rect = load_image('enemy2_scale.png',-1)
            self.rect.top = 100
            self.rect.left = width/2
        
        self.speed = 0
        self.move = [0,0]
        self.trigger = 0
    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.move[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.move[0] = 0
            self.speed=0
    def updateposition(self):
        self.rect = self.rect.move(self.move)
    def drawplayer(self):
        screen.blit(self.image,self.rect)
    
        
        
            

starfield = stars()
user = player()
enemy = player()
enemy.__init__(True)
        
pygame.display.set_caption('Galaxian')
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            user.trigger = 1
            if event.key == pygame.K_LEFT:
                user.speed = -2
            elif event.key == pygame.K_RIGHT:
                user.speed = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                user.trigger = 2
                user.speed = 0

        cpumove(enemy,user)
        """if cpumove() == 0:
            enemy.trigger = 1
            enemy.speed = 2
        elif cpumove() == 1:
            enemy.trigger = 1
            enemy.speed = -2
        elif cpumove() == 2:
            enemy.trigger = 2
            enemy.speed = 0
    
    jetrect = jetrect.move(movejet)
    enemyrect = enemyrect.move(emovejet)"""
    user.updateposition()
    enemy.updateposition()
    """if jetrect.left < 0:
            jetrect.left = 0
            movejet[0]=0
            speed=0
    if jetrect.right > width:
            jetrect.right = width
            movejet[0]=0
            speed=0

    if enemyrect.left < 0:
            enemyrect.left = 0
            emovejet[0]=0
            espeed=0
    if enemyrect.right > width:
            enemyrect.right = width
            emovejet[0]=0
            espeed=0
       """
    user.checkbounds()
    enemy.checkbounds()
    #screen.fill(white)
    screen.fill(sky)
    #drawstars()
    starfield.drawstars()
    """screen.blit(jet,jetrect)
    screen.blit(enemy,enemyrect)"""
    user.drawplayer()
    enemy.drawplayer()
    pygame.display.update()
    clock.tick(FPS)

    """if jetrect.left >= 0 and jetrect.right <= width:
        if trigger == 1:
            movejet[0] = movejet[0] + speed
            if movejet[0] < -maxspeed:
               movejet[0] = -maxspeed
            elif movejet[0] > maxspeed:
                movejet[0] = maxspeed

        elif movejet[0] >= -maxspeed and movejet[0] < 0 and trigger == 2:
            movejet[0] += math.fabs(movejet[0]/20)
            if movejet[0] > 0:
                movejet[0] = 0
        elif movejet[0] <= maxspeed and movejet[0] > 0 and trigger == 2:
            movejet[0] -= movejet[0]/20
            if movejet[0] < 0:
                movejet[0] = 0
    #starfield.movestars()
        
    if enemyrect.left >= 0 and enemyrect.right <= width:
        if etrigger == 1:
            emovejet[0] = emovejet[0] + espeed
            if emovejet[0] < -maxspeed:
               emovejet[0] = -maxspeed
            elif emovejet[0] > maxspeed:
                emovejet[0] = maxspeed

        elif emovejet[0] >= -maxspeed and emovejet[0] < 0 and etrigger == 2:
            emovejet[0] += math.fabs(emovejet[0]/20)
            if emovejet[0] > 0:
                emovejet[0] = 0
        elif emovejet[0] <= maxspeed and emovejet[0] > 0 and etrigger == 2:
            emovejet[0] -= emovejet[0]/20
            if emovejet[0] < 0:
                emovejet[0] = 0

    """
    moveplayer(user)
    moveplayer(enemy)
    print(user.rect.left," ",user.rect.right)
    
pygame.quit()
quit()



