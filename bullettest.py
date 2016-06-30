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

screen = pygame.display.set_mode(size)
everything = pygame.sprite.Group()


def cpumove(cpu,target):
    if target.rect.left < cpu.rect.left:
        cpu.trigger = 1
        cpu.speed = -2
    elif target.rect.left > cpu.rect.left:
        cpu.trigger = 1
        cpu.speed = 2

      

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
    def __init__(self,groups,weapon_groups,isenemy=False):
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
        self.groups = [groups, weapon_groups]
        self.shot = False
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
    def shoot(self):
        x,y = self.rect.center
        self.shot = bullet(x,y)
        self.shot.add(self.groups)

class bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        #for i in range(5, 0, -1):
        #    color = 255.0 * float(i)/5
        #pygame.draw.circle(self.image, (225, 15, 15), (5, 5), 5, 0)
        pygame.draw.rect(self.image,(12,225,15),(4,0,2,20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-36)

    def update(self):
        x, y = self.rect.center
        y -= 20
        self.rect.center = x, y
        if y <= 0:
            self.kill()


def main():
    gameOver = False
    starfield = stars()
    
    #enemy = player()
    #enemy.__init__(True)

    weapon_fire = pygame.sprite.Group()
    user = player(everything,weapon_fire)
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
                elif event.key == pygame.K_UP:
                    user.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    user.trigger = 2
                    user.speed = 0

        #cpumove(enemy,user)
            
        user.updateposition()
        #enemy.updateposition()
        
        user.checkbounds()
        #enemy.checkbounds()
        
        screen.fill(sky)
        
        starfield.drawstars()
        
        user.drawplayer()
        #enemy.drawplayer()
        everything.update()
        everything.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        
        moveplayer(user)
        #moveplayer(enemy)
        print(user.rect.left," ",user.rect.right)
        
    pygame.quit()
    quit()


        
    
        
         



main()



