#test 1

import sys
import pygame
import time
import math
import random


pygame.init()

size = width, height = 1920, 1080
#size = width, height = 1600, 900
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((width, height))

sysfont = pygame.font.SysFont(None , 40)
text = sysfont.render("Health = "+str(100),True,(255,255,255))

pew=pygame.mixer.Sound("pew.wav")
lasersound=pygame.mixer.Sound("lasersound.wav")
pygame.mixer.music.load('beat.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.pre_init(44100,-16,1, 1024)
#pygame.mixer.music.set_volume(0.03)
laser_img=pygame.image.load("laser.png")
ship = pygame.image.load("starship.png")
bullet_img = pygame.image.load("bullet.png")
asteroid_small = pygame.image.load("small.png")
asteroid_medium = pygame.image.load("medium.png")
asteroid_large = pygame.image.load("large.png")
ammobox1 = pygame.image.load("ammo.png")
ammobox2 = pygame.image.load("laser_ammo_image.png")
healthpack = pygame.image.load("health_pck_img.png")

astersize = {1:asteroid_small,2:asteroid_medium,3:asteroid_large}
ammoboximage = {1:ammobox1 , 2:ammobox2 , 3:healthpack }


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
consumables_list=[]
textlist = []
health = 100
normalammo = 20
laserammo = 10

class Text:

	def __init__(self):
		textlist.append(self)

	def set_text(self,text,font,color):
		self.text = font.render(text,True,color)

	def draw(self,x,y):
		screen.blit(self.text,(x,y))		





class Consumables:

	def __init__(self,x,y,ammotype):
		self.x = x
		self.y = y
		self.type = ammotype 
		self.image = ammoboximage[self.type]
		self.bbox = self.image.get_rect()

	def collisiondetect(self):
		global normalammo
		global laserammo
		global health
		if x > self.x and x < self.x + self.bbox[2] and y > self.y and y < self.y + self.bbox[3]:
			if self.type == 1: normalammo += 10
			if self.type == 2: laserammo += 5
			if self.type == 3: health += 20

			consumables_list.remove(self)

	def draw(self):
		screen.blit(self.image, (self.x,self.y))


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
	def __init__(self,bposx,bposy,typee,angle):
		global laserammo
		global normalammo

		self.angle=angle
		self.bposx=bposx
		self.bposy=bposy
		self.bvx=math.sin(angle*3.1415/180 +3.1415) 
		self.bvy=math.cos(angle*3.1415/180+3.1415)
		self.type = typee # Type of Bullet , 1 is a normal bullet , 2 is a laser
		if self.type == 1: normalammo -= 1
		if self.type == 2: laserammo -= 1


	   # self.fire()

	def checkdelete(self):
		if self.bposx >width or self.bposx<0 or self.bposy > height or self.bposy < 0:
			bullets.remove(self)

	def draw(self):
		global angle
		'''
		old=shiprect.center
		new_ship=pygame.transform.rotate(ship,angle)
		shiprect = new_ship.get_rect()
		shiprect.center=old
		screen.blit(new_ship, (x,y))
		'''
		if self.type==1:
			screen.blit(bullet_img, (self.bposx,self.bposy))

		if self.type==2:
			#self.old_r=self.r.center
			self.new_l=pygame.transform.rotate(laser_img,self.angle)
			self.r=self.new_l.get_rect()
			self.r.center=old
			screen.blit(self.new_l, (self.bposx,self.bposy))
		
	def move(self):
		self.bposx=self.bposx+self.bvx*20
		self.bposy=self.bposy+self.bvy*20

	for i in range(10):
		asteroids_list.append(asteroid(random.randint(0,width),random.randint(0,height),random.randint(1,3)   ))

	for i in range(20):
		consumables_list.append(Consumables(random.randint(0,width),random.randint(0,height),random.randint(1,3)))


helathtext = Text()
ammo1text = Text()
ammo2text = Text()




while 1:
	#global angle
	time.sleep(1/FPS)
	angle=angle+anglev

	if health > 100: health = 100
	if health <= 0: sys.exit()
	
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
				if normalammo > 0:
					bullets.append(Bullet(x,y,1,angle))
					pygame.mixer.Sound.play(pew)
					#print("piew")

			if event.key==pygame.K_LSHIFT:
				if laserammo > 0:
					bullets.append(Bullet(x,y,2,angle))
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


	#screen.blit(text,(width/2,height/2))

	for aster in asteroids_list:
		aster.collisiondetect()
		aster.move()
		aster.draw()

	for bullet in bullets:
		bullet.checkdelete()
		if bullets.count(bullet):
			bullet.move()
			bullet.draw()

	for consumable in consumables_list:
		consumable.collisiondetect()
		consumable.draw()


	screen.blit(new_ship, (x,y))

	helathtext.set_text("Health: "+str(health),sysfont,white) 
	ammo1text.set_text("Bullets: "+str(normalammo),sysfont,white) 
	ammo2text.set_text("Lasers: "+str(laserammo),sysfont,white) 

	helathtext.draw(200,110) 
	ammo1text.draw(200,140) 
	ammo2text.draw(200,170) 


	pygame.display.update()

pygame.quit()
quit()