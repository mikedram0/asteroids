import sys
import pygame
import time
import math
import random


pygame.init()

size = width, height = 1920, 1080
#size = width, height = 1600, 900
black = 0, 0, 0

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((width, height))

pew = pygame.mixer.Sound("pew.wav")
lasersound = pygame.mixer.Sound("lasersound.wav")

pygame.mixer.music.load('beat.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.03)
ship = pygame.image.load("starship.png")
bullet_img = pygame.image.load("bullet.png")
asteroid_small = pygame.image.load("small.png")
asteroid_medium = pygame.image.load("medium.png")
asteroid_large = pygame.image.load("large.png")
laser = pygame.image.load("laser.png")

astersize = {1:asteroid_small,2:asteroid_medium,3:asteroid_large}


shiprect = ship.get_rect()
x=width/2
y=height/2
vx=0
vy=0
angle=0
anglev=0
FPS=60
bullets=[]
asteroids_list=[]
health = 100

class asteroid:
    def __init__(self,x,y,size):
        self.aposx=x
        self.aposy=y
        self.avx=random.randint(-1,1)
        self.avy=random.randint(-1,1)
        
        self.size = size
        self.image = astersize[self.size]
        self.bbox = self.image.get_rect()

    def collisiondetect(self):
        global health
        for bullet in bullets:
            if bullet.bposx > self.aposx and bullet.bposx < self.aposx + self.bbox[2] and bullet.bposy > self.aposy and bullet.bposy < self.aposy + self.bbox[3]:
                asteroids_list.remove(self)
                bullets.remove(bullet)
                if self.size > 1 and bullet.type == 1:
                    asteroids_list.append(asteroid(self.aposx,self.aposy,self.size-1))
                    asteroids_list.append(asteroid(self.aposx,self.aposy,self.size-1))
        if x > self.aposx and x < self.aposx + self.bbox[2] and y > self.aposy and y < self.aposy + self.bbox[3]:            
            health = health - self.size*10
            asteroids_list.remove(self)
    def move(self):
        self.aposx=self.aposx+self.avx
        self.aposy=self.aposy+self.avy
        if self.aposx>width:
            self.aposx = 0
        if self.aposx<0:
            self.aposx = width
        if self.aposy>height:
            self.aposy = 0 
        if self.aposy<0:
            self.aposy = height
        
    def draw(self):
        screen.blit(self.image, (self.aposx,self.aposy))



class Bullet:
    def __init__(self,bposx,bposy,typee):
        self.bposx=bposx
        self.bposy=bposy
        self.bvx=math.sin(angle*3.1415/180 +3.1415) 
        self.bvy=math.cos(angle*3.1415/180+3.1415)
        self.type = typee # Type of Bullet , 1 is a normal bullet , 2 is a laser
       # self.fire()

    def checkdelete(self):
        if self.bposx >width or self.bposx<0 or self.bposy > height or self.bposy < 0:
            bullets.remove(self)

    def draw(self):
        if self.type == 1:
            screen.blit(bullet_img, (self.bposx,self.bposy))
        if self.type == 2:
            screen.blit(laser, (self.bposx,self.bposy))
        
    def move(self):
        self.bposx=self.bposx+self.bvx*20
        self.bposy=self.bposy+self.bvy*20

    for i in range(10):
        asteroids_list.append(asteroid(random.randint(0,width),random.randint(0,height),random.randint(1,3)   ))


while 1:
    time.sleep(1/FPS)
    angle=angle+anglev

    #print(health)
    if health <= 0:
        sys.exit()
    
    #print(1)
    for event in pygame.event.get():
        #print(2)
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            
            if event.key==pygame.K_ESCAPE:
                sys.exit()

            if event.key==pygame.K_a:
                anglev=anglev+1

            if event.key==pygame.K_SPACE:
                bullets.append(Bullet(x,y,1))
                
                pygame.mixer.Sound.play(pew)
                #print("piew")

            if event.key==pygame.K_LSHIFT:
                bullets.append(Bullet(x,y,2))
                pygame.mixer.Sound.play(lasersound)
                #print("piew")
                

            if event.key==pygame.K_d:
                anglev=anglev-1


            if event.key == pygame.K_w:
                vx += math.sin(angle*3.1415/180 +3.1415) 
                vy += math.cos(angle*3.1415/180+3.1415) 


    x += vx
    y += vy

    if x-shiprect[2]>width:
        x = 0 - shiprect[1]
    if x+shiprect[2]<0:
        x = width
    if y>height:
        y = 0 - shiprect[3]
    if y<0-shiprect[3]:
        y = height
        
    #print(bullets)
    old=shiprect.center
    new_ship=pygame.transform.rotate(ship,angle)
    shiprect = new_ship.get_rect()
    shiprect.center=old




    screen.fill(black)

    for aster in asteroids_list:
        aster.collisiondetect()
        aster.move()
        aster.draw()

    for bullet in bullets:
        bullet.checkdelete()
        if bullets.count(bullet):
            bullet.move()
            bullet.draw()


    screen.blit(new_ship, (x,y))
    pygame.display.update()

pygame.quit()
quit()

