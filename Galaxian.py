import os,pygame,sys,time,math,random
pygame.init()



size = width, height = 1000,600
black = 0,0,0
white = 255,255,255
sky = 0,0,40
clock = pygame.time.Clock()
FPS = 20

screen = pygame.display.set_mode(size)

jet = pygame.image.load("Sprites/fighter_scale.png").convert()
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
gameOver = False
movejet = [0,0]
emovejet = [0,0]
speed = 0
espeed = 0
maxspeed = 15
trigger = 0
etrigger = 0


def cpumove():
    return random.randrange(0,3)
        
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
            

starfield = stars()
        
pygame.display.set_caption('Galaxian')
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            trigger = 1
            if event.key == pygame.K_LEFT:
                speed = -2
            elif event.key == pygame.K_RIGHT:
                speed = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                trigger = 2
                speed = 0

        if cpumove() == 0:
            etrigger = 1
            espeed = 2
        elif cpumove() == 1:
            etrigger = 1
            espeed = -2
        elif cpumove() == 2:
            etrigger = 2
            espeed = 0
    
    jetrect = jetrect.move(movejet)
    enemyrect = enemyrect.move(emovejet)
    if jetrect.left < 0:
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
            
    #screen.fill(white)
    screen.fill(sky)
    #drawstars()
    starfield.drawstars()
    screen.blit(jet,jetrect)
    screen.blit(enemy,enemyrect)
    pygame.display.update()
    clock.tick(FPS)

    if jetrect.left >= 0 and jetrect.right <= width:
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

    
    print(jetrect.left," ",jetrect.right)
    
pygame.quit()
quit()



