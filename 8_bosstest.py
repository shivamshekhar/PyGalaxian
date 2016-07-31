from __future__ import print_function
import os,pygame,sys,time,math,random
from pygame.locals import *


pygame.init()

size = width, height = 1000,600
black = 0,0,0
white = 255,255,255
green = 0,155,0
red = 155,0,0 
sky = 0,0,40
clock = pygame.time.Clock()
FPS = 20
maxspeed = 15

screen = pygame.display.set_mode(size)

def cpumove(cpu,target):
    if target.rect.left < cpu.rect.left:
        cpu.trigger = 1
        cpu.speed = -2
    elif target.rect.left > cpu.rect.left:
        cpu.trigger = 1
        cpu.speed = 2
    if random.randrange(0,3) == 1:
        cpu.fire = 1
    else:
        cpu.fire = 0

\
def bossmove(cpu,target):
    if target.rect.left < cpu.rect.left and cpu.spree == False:
        cpu.trigger = 1
        cpu.speed = -2
    elif target.rect.left > cpu.rect.left and cpu.spree == False:
        cpu.trigger = 1
        cpu.speed = 2
    
    
    if random.randrange(0,3) == 1 and cpu.spree == False:
    	cpu.bulletformation = 0
    	cpu.bulletspeed = 20
    	cpu.fire = 1
    else:
        cpu.fire = 0

    
    if cpu.spree == False and random.randrange(0,200) == 71:
    	cpu.spree = True
    else:
    	pass


def load_image(name, sizex, sizey,colorkey=None):
    fullname = os.path.join('Sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)

    image = pygame.transform.scale(image,(sizex,sizey))
    return image, image.get_rect()

def showhealthbar(health,barcolor,pos,unit):
    healthbar = pygame.Surface((health*unit,10),pygame.SRCALPHA, 32)
    healthbar = healthbar.convert_alpha()
    pygame.draw.rect(screen,barcolor,pos)

def displaytext(text, fontsize, x, y, color):
    font = pygame.font.Font(None, fontsize)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)

def moveplayer(Player):
    if Player.rect.left >= 0 and Player.rect.right <= width:
        if Player.trigger == 1:
            Player.movement[0] = Player.movement[0] + Player.speed
            if Player.movement[0] < -maxspeed:
               Player.movement[0] = -maxspeed
            elif Player.movement[0] > maxspeed:
                Player.movement[0] = maxspeed
        elif Player.movement[0] >= -maxspeed and Player.movement[0] < 0 and Player.trigger == 2:
            Player.movement[0] += math.fabs(Player.movement[0]/20)
            if Player.movement[0] > 0:
                Player.movement[0] = 0
        elif Player.movement[0] <= maxspeed and Player.movement[0] > 0 and Player.trigger == 2:
            Player.movement[0] -= math.fabs(Player.movement[0]/20)
            if Player.movement[0] < 0:
                Player.movement[0] = 0


           
        
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('fighter1_scale.png',72,72,-1)
        #self.image = pygame.transform.scale(self.image,(72,72))
        
        self.rect = self.image.get_rect()
        self.rect.top = 500
        self.rect.left = 200
        
        self.speed = 0
        self.fire = 0
        self.movement = [0,0]
        self.trigger = 0
        self.health = 100
        self.shot = False
    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed=0
    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.fire == 1:
            self.shoot()

    def drawplayer(self):
        screen.blit(self.image,self.rect)

    def shoot(self):
        x,y = self.rect.center
        self.shot = bullet(x-14,y,1)
        self.shot = bullet(x+14,y,1)

class boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.containers)
        
        self.image, self.rect = load_image('fighter3.png',200,200,-1)
        
        #self.image = pygame.transform.scale(self.image,(200,200))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image,180)
        self.rect.top = 100
        self.rect.left = random.randrange(0,width-72)
        

        self.speed = 0
        self.fire = 0
        self.movement = [0,0]
        self.trigger = 0
        self.health = 1000
        self.bulletformation = 0
        self.bulletspeed = 20
        self.spreecount = 0
        self.spree = False
        self.shot = False
        self.reloadtime = 0
    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed=0
    def update(self):
        self.checkbounds()
        moveplayer(self)

        self.rect = self.rect.move(self.movement)
        

        if self.fire == 1 and self.reloadtime == 0:
            self.shoot(self.bulletformation,self.bulletspeed)

        if self.reloadtime > 0:
            self.reloadtime -= 1

        if self.health <= 0:
            self.kill()

        if self.spree == True and self.spreecount <= 70:
        	self.spreecount += 1
        	if self.spreecount % 5 == 1:
        		self.movement[0] = 0
        		self.speed = 0
        		self.shoot(1,10)
        	else:
        		pass
        else:
        	self.spree = False
        	self.spreecount = 0
    
    def drawplayer(self):
        screen.blit(self.image,self.rect)
    def shoot(self,bulletformation=0,bulletspeed=20):
        x,y = self.rect.center
    	if bulletformation == 0:
    		self.shot = enemybullet(x,y + (self.rect.height)/2,[0,1],bulletspeed)
    		self.shot = enemybullet(x - self.rect.width/2 + 20,y - (self.rect.height)/2 + 30,[0,1],bulletspeed)
    		self.shot = enemybullet(x + self.rect.width/2 - 20,y - (self.rect.height)/2 + 30,[0,1],bulletspeed)
    	elif bulletformation == 1:
            self.shot = enemybullet(x ,y ,[1.5,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[-1.5,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[1.2,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[-1.2,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[0,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[0.9,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[-0.9,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[0.6,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[-0.6,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[0.3,1],bulletspeed)
            self.shot = enemybullet(x ,y ,[-0.3,1],bulletspeed)
    		
    	elif bulletformation == 2:
            splittingbullet(x,y,[0,1],bulletspeed)
            self.reloadtime = 100
    	elif bulletformation == 3:
    		pass	
    	elif bulletformation == 4:
    		pass

        

class enemy(pygame.sprite.Sprite):
    def __init__(self, n=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        sheet = pygame.image.load("Sprites/enemy_sheet1.png")
        self.images = []
        
        rect = pygame.Rect((0, 0, 85, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((86, 0, 71, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((158, 0, 68, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((227, 0, 65, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)


        self.image = self.images[n]
        self.image = self.image.convert()
        colorkey = -1
        colorkey = self.image.get_at((10,10))
        self.image.set_colorkey(colorkey, RLEACCEL)
        
        self.image = pygame.transform.scale(self.image,(36,36))
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image,180)
        self.rect.top = 0
        self.rect.left = random.randrange(0,width-72)
    
        self.speed = 0
        self.fire = 0
        self.movement = [0,0]
        self.trigger = 0
        self.health = 2

        self.explosion_sound = pygame.mixer.Sound("Sprites/explosion.wav")
        self.explosion_sound.set_volume(0.1)
        
        self.shot = False
    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed=0
    def update(self):
        self.checkbounds()
        
        moveplayer(self)
        self.autopilot()
        self.rect = self.rect.move(self.movement)
        

        if self.fire == 1:
            self.shoot()

        if self.health <= 0:
            self.kill()
            x, y = self.rect.center
            if pygame.mixer.get_init():
                self.explosion_sound.play(maxtime=1000)
            explosion(x,y)
            
    def drawplayer(self):
        screen.blit(self.image,self.rect)
    def shoot(self):
        x,y = self.rect.center
        self.shot = enemybullet(x,y)
        #self.bulletformations()
    def autopilot(self):
        if self.rect.top < height:
            self.movement[1] = 5
        else:
            self.kill()
    
    def bulletformations(self):
    	x,y = self.rect.center
    	self.shot = enemybullet(x,y-(self.rect.height)/2)



class bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction = 1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.Surface((2,18),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        
        pygame.draw.rect(self.image,(12,225,15),(0,0,2,18))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-direction*20)
        self.direction = direction

    def update(self):
        x, y = self.rect.center
        y -= self.direction*20
        self.rect.center = x, y
        if y <= 0 or y >= height:
            self.kill()

class enemybullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,speed):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.Surface((10,10),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        for i in range(5, 0, -1):
            color = 255.0 * float(i)/5
            pygame.draw.circle(self.image, (color,0,155), (5, 5), i, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)#+ direction[1]*20)
        self.direction = direction
        self.speed = speed

    def update(self):
        x, y = self.rect.center
        y += self.direction[1]*self.speed
        x += self.direction[0]*self.speed
        self.rect.center = x, y
        if y <= 0 or y >= height or x <= 0 or x >= width:
            self.kill()


class splittingbullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,speed):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.Surface((10,10),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        for i in range(5, 0, -1):
            color = 255.0 * float(i)/5
            pygame.draw.circle(self.image, (color,0,155), (5, 5), i, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)#+ direction[1]*20)
        self.initpos = (x,y)
        self.direction = direction
        self.speed = speed

    def update(self):
        x, y = self.rect.center
        y += self.direction[1]*self.speed
        x += self.direction[0]*self.speed
        self.rect.center = x, y

        if self.rect.top > self.initpos[1] + 20:
            if len(self.containers) < 10:
                splittingbullet(self.rect.centerx - 10,self.rect.centery + 10, [-0.5,1],self.speed)
                splittingbullet(self.rect.centerx + 10,self.rect.centery + 10, [0.5,1],self.speed)
                self.kill()
        if y <= 0 or y >= height or x <= 0 or x >= width:
            self.kill()



class explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load("Sprites/enemy_explode.png")
        self.images = []
        for i in range(0, 768, 48):
            rect = pygame.Rect((i, 0, 48, 48))
            image = pygame.Surface(rect.size)
            image = image.convert()
            colorkey = -1
            colorkey = image.get_at((10,10))
            image.set_colorkey(colorkey, RLEACCEL)

            image.blit(sheet, (0, 0), rect)
            self.images.append(image)
            
        self.image = self.images[0]
        self.index = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        self.image = self.images[self.index]
        self.index += 1
        if self.index >= len(self.images):
            self.kill()



def main():
    gameOver = False
    starfield = stars()

    bullets = pygame.sprite.Group()
    enemybullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    
    bullet.containers = bullets
    boss.containers = enemies
    enemybullet.containers = enemybullets
    enemy.containers = enemies
    explosion.containers = explosions
    splittingbullet.containers = enemybullets

    user = player()
    #enemy()
    finalboss = boss()

    pygame.display.set_caption('Galaxian')
    #bg_music = pygame.mixer.Sound("Sprites/bg_music.wav")
    #bg_music.play(-1)

    


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
                    user.fire = 1
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    user.trigger = 2
                    user.speed = 0
                if event.key == pygame.K_UP:
                    user.fire = 0

        #if random.randrange(0,8) == 1 and len(enemies) < 10:
         #   enemy(random.randrange(0,4))
        
        #for ship in enemies:
         #   cpumove(ship,user)
        bossmove(finalboss, user)
        for userbullet in bullets:
            if pygame.sprite.collide_mask(finalboss,userbullet):
                finalboss.health -= 1
                userbullet.kill()

        #for userbullet in bullets:
         #   if pixel_perfect_check_collision(userbullet, finalboss) == True:
          #      finalboss.health -= 1
           #     userbullet.kill()
            

        
        for firedbullet in pygame.sprite.spritecollide(user,enemybullets,1):
            user.health -= 1
        
        #for enemycollided in pygame.sprite.spritecollide(user, enemies, 0):
         #   user.health -= 10
          #  enemycollided.health -= 2

        

        pygame.sprite.groupcollide(bullets,enemybullets,1,1)
        

        if user.health <= 0:
            gameOver = True
        user.update()
        user.checkbounds()
        
        screen.fill(sky)
        starfield.drawstars()
        showhealthbar(user.health,green,[100,(height - 20),user.health*8,10],8)
        displaytext("HEALTH",22, 50,height - 15,green)
        
        showhealthbar(finalboss.health,red,[100,20,finalboss.health*0.8,10],0.8)
        displaytext("BOSS",22,50,25,red)
        
        user.drawplayer()
        
        enemies.update()
        bullets.update()
        enemybullets.update()
        explosions.update()
        
        bullets.draw(screen)
        enemybullets.draw(screen)
        enemies.draw(screen)
        explosions.draw(screen)
        
        pygame.display.update()
        
        clock.tick(FPS)

        moveplayer(user)
        
        print(user.health,finalboss.spreecount,finalboss.spree)
        
    pygame.quit()
    quit()


        
    
        
         



main()








