import pygame
from random import *


class SmallEnemy(pygame.sprite.Sprite):
	def __init__(self, bg_size):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load("images/enemy1.png").convert_alpha()
		self.destroy_images = []
		self.destroy_images.extend([pygame.image.load("images/enemy_destroy_1.png").convert_alpha(),pygame.image. load("images/enemy1.png").convert_alpha()])
		self.active = True
		self.rect = self.image.get_rect()
		self.width,self.height = bg_size[0], bg_size[1]
		self.speed = 2
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-5*self.height, 0)
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.reset()

	def reset(self):
		self.active = True
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-5*self.height, 0)



class MidEnemy(pygame.sprite.Sprite):

	energy = 8

	def __init__(self, bg_size):
		pygame.sprite.Sprite.__init__(self)

		self.energy = MidEnemy.energy

		self.image = pygame.image.load("images/enemy2.png").convert_alpha()
		self.destroy_images = []
		self.destroy_images.extend([pygame.image.load("images/enemy_destroy_2.png").convert_alpha(), pygame.image.load("images/enemy2.png").convert_alpha()])
		self.active = True		
		self.rect = self.image.get_rect()
		self.width,self.height = bg_size[0], bg_size[1]
		self.speed = 1
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-10*self.height, -self.height)
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.reset()

	def reset(self):
		self.energy = MidEnemy.energy
		self.active = True
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-10*self.height, -3*self.height) 


class BigEnemy(pygame.sprite.Sprite):
	energy = 20
	def __init__(self, bg_size):
		pygame.sprite.Sprite.__init__(self)

		self.energy = BigEnemy.energy

		self.image = pygame.image.load("images/enemy3.png").convert_alpha()
		self.destroy_images = []
		self.destroy_images.extend([pygame.image.load("images/enemy_destroy_3.png").convert_alpha(), pygame.image.load("images/enemy3.png").convert_alpha()])
		self.active = True
		self.rect = self.image.get_rect()
		self.width,self.height = bg_size[0], bg_size[1]
		self.speed = 1
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-12*self.height, -5*self.height)
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.reset()

	def reset(self):
		self.energy = BigEnemy.energy
		self.active = True
		self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-15*self.height, -5*self.height) 
