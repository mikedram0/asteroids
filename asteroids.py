import sys
import pygame
import time
import math
import random


pygame.init()

width = 1280
height = 720
#size = width, height = 1600, 900
black = 0, 0, 0
white = 255, 255, 255

#screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

sysfont = pygame.font.SysFont(None , 40)
text = sysfont.render("Health = "+str(100),True,(255,255,255))

pew=pygame.mixer.Sound("pew.wav")
lasersound=pygame.mixer.Sound("lasersound.wav")
breaksound = pygame.mixer.Sound("break.wav")
thrustsound = pygame.mixer.Sound("thrust.wav")
pygame.mixer.music.load('beat.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.pre_init(44100,-16,1, 1024)
#pygame.mixer.music.set_volume(0.03)
laser_img=pygame.image.load("laser.png")
ship1 = pygame.image.load("starship.png")
ship2 = pygame.image.load("starship2.png")
bullet_img = pygame.image.load("bullet.png")
asteroid_small = pygame.image.load("small.png")
asteroid_medium = pygame.image.load("medium.png")
asteroid_large = pygame.image.load("large.png")
ammobox1 = pygame.image.load("ammo.png")
ammobox2 = pygame.image.load("laser_ammo_image.png")
healthpack = pygame.image.load("health_pck_img.png")

astersize = {1:asteroid_small,2:asteroid_medium,3:asteroid_large}
ammoboximage = {1:ammobox1 , 2:ammobox2 , 3:healthpack }



FPS=60
bullets=[]
asteroids_list=[]
consumables_list=[]
textlist = []


class Player:

	def __init__(self,x,y):
		self.x = x 
		self.y = y
		self.vx = 0
		self.vy = 0
		self.ax = 0
		self.ay = 0
		self.health = 100
		self.normalammo = 20
		self.laserammo = 10
		self.image = ship1
		self.angle = 0
		self.anglev = 0
		self.rect = self.image.get_rect()

	def move(self):

		self.vx += self.ax
		self.vy += self.ay

		self.x += self.vx
		self.y += self.vy

		self.angle += self.anglev

		if self.angle >= 360:
			self.angle -= (self.angle%360)*360

		if self.x-self.rect[2]>width:
			self.x = 0 - self.rect[2]
		if self.x+ self.rect[2]<0:
			self.x = width
		if self.y>height:
			self.y = 0 - self.rect[3]
		if self.y<0-self.rect[3]:
			self.y = height


	def healthcheck(self):

		if self.health > 100 : health = 100
		if self.health <= 0 : sys.exit()

	def draw(self):
		self.newimage=pygame.transform.rotate(self.image,player1.angle)
		self.rect = self.newimage.get_rect()
		self.rect.center = (self.x,self.y)
		screen.blit(self.newimage,self.rect)









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
		if player1.x > self.x and player1.x < self.x + self.bbox[2] and player1.y > self.y and player1.y < self.y + self.bbox[3]:
			if self.type == 1: player1.normalammo += 10
			if self.type == 2: player1.laserammo += 5
			if self.type == 3: player1.health += 20

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
				pygame.mixer.Sound.play(breaksound)
				bullets.remove(bullet)
				if self.size > 1 and bullet.type == 1:
					asteroids_list.append(asteroid(self.aposx,self.aposy,self.size-1))
					asteroids_list.append(asteroid(self.aposx,self.aposy,self.size-1))
		if player1.x > self.aposx and player1.x < self.aposx + self.bbox[2] and player1.y > self.aposy and player1.y < self.aposy + self.bbox[3]:            
			player1.health -= self.size*10
			asteroids_list.remove(self)
			pygame.mixer.Sound.play(breaksound)
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

		self.angle=player1.angle
		self.bposx=bposx
		self.bposy=bposy
		self.bvx=math.sin(player1.angle*3.1415/180 +3.1415) 
		self.bvy=math.cos(player1.angle*3.1415/180+3.1415)
		self.type = typee # Type of Bullet , 1 is a normal bullet , 2 is a laser
		if self.type == 1: player1.normalammo -= 1
		if self.type == 2: player1.laserammo -= 1


	   # self.fire()

	def checkdelete(self):
		if self.bposx >width or self.bposx<0 or self.bposy > height or self.bposy < 0:
			bullets.remove(self)

	def draw(self):
		
		
		if self.type==1:
			screen.blit(bullet_img, (self.bposx,self.bposy))

		if self.type==2:
			self.new_l=pygame.transform.rotate(laser_img,self.angle)
			rect = self.new_l.get_rect()
			rect.center = (self.bposx,self.bposy)
			screen.blit(self.new_l, rect)
		
	def move(self):
		self.bposx=self.bposx+self.bvx*20
		self.bposy=self.bposy+self.bvy*20



for i in range(5):
		asteroids_list.append(asteroid(random.randint(0,width),random.randint(0,height),random.randint(1,3)   ))

for i in range(10):
	consumables_list.append(Consumables(random.randint(0,width),random.randint(0,height),random.randint(1,3)))


helathtext = Text()
ammo1text = Text()
ammo2text = Text()

player1=Player(width/2,height/2)


def main():

	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
		if event.type == pygame.KEYDOWN:
			
			if event.key==pygame.K_ESCAPE:
				sys.exit()

			if event.key==pygame.K_a:
				player1.anglev=player1.anglev+2

			if event.key==pygame.K_SPACE:
				if player1.normalammo > 0:
					bullets.append(Bullet(player1.x,player1.y,1,player1.angle))
					pygame.mixer.Sound.play(pew)
					#print("piew")

			if event.key==pygame.K_LSHIFT:
				if player1.laserammo > 0:
					bullets.append(Bullet(player1.x,player1.y,2,player1.angle))
					pygame.mixer.Sound.play(lasersound)
				#print("piew")

			if event.key==pygame.K_d:
				player1.anglev=player1.anglev-2


			if event.key == pygame.K_w:
				player1.image = ship2
				player1.ax = math.sin(player1.angle*3.1415/180 +3.1415) * 0.1
				player1.ay = math.cos(player1.angle*3.1415/180+3.1415) * 0.1 
				pygame.mixer.Sound.play(thrustsound,-1)

				
		if event.type  == pygame.KEYUP:

			if event.key == pygame.K_a:
				player1.anglev = 0

			if event.key == pygame.K_d:
				player1.anglev = 0

			if event.key == pygame.K_w:
				player1.image = ship1
				player1.ax = 0
				player1.ay = 0
				pygame.mixer.Sound.stop(thrustsound)



	clock.tick(FPS)
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

	for consumable in consumables_list:
		consumable.collisiondetect()
		consumable.draw()

	player1.healthcheck()
	player1.move()
	player1.draw()
	pygame.draw.rect(screen,white,player1.rect,3)

	#helathtext.set_text("Health: "+str(player1.health),sysfont,white) 
	helathtext.set_text("x: "+str(int(player1.x))+" y: "+str(int(player1.y))+" FPS: "+str(clock.get_fps()),sysfont,white) 
	ammo1text.set_text("Bullets: "+str(player1.normalammo),sysfont,white) 
	ammo2text.set_text("Lasers: "+str(player1.laserammo),sysfont,white) 

	helathtext.draw(width/100,10) 
	ammo1text.draw(width/100,40) 
	ammo2text.draw(width/100,70) 
	pygame.display.update()


while 1:
	main()
pygame.quit()
quit()