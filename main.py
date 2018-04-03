import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
import random
from random import *
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")

background = pygame.image.load("images/background.png").convert()

#载入游戏音乐
pygame.mixer.music.load("sound/game_music.mp3")
pygame.mixer.music.set_volume(0.2)

enemy3_down_sound = pygame.mixer.Sound("sound/enemy3.wav")
enemy3_down_sound.set_volume(0.2)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def add_small_enemies(group1, group2, num):
	for i in range(num):
		e1 = enemy.SmallEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)

def add_mid_enemies(group1, group2, num):
	for i in range(num):
		e1 = enemy.MidEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)

def add_big_enemies(group1, group2, num):
	for i in range(num):
		e1 = enemy.BigEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)

def inc_speed(target, inc):
	for each in target:
		each.speed += inc

def main():
#pygame.mixer.music.play(n,start,stop)
#第一个参数为播放次数，如果是-1表示循环播放，省略表示只播放1次。第二个参数和第三个参数分别表示播放的起始和结束位置。
	pygame.mixer.music.play(-1)

	clock = pygame.time.Clock()
#生成我方飞机
	me = myplane.MyPlane(bg_size)
#生成敌方飞机
	enemies = pygame.sprite.Group()
#生成敌方小型飞机
	small_enemies = pygame.sprite.Group()
	add_small_enemies(small_enemies, enemies, 15)

	mid_enemies = pygame.sprite.Group()
	add_mid_enemies(mid_enemies, enemies, 4)

	big_enemies = pygame.sprite.Group()
	add_big_enemies(big_enemies, enemies, 2)

#中弹图片索引
	e1_destroy_index = 0
	e2_destroy_index = 0
	e3_destroy_index = 0
	me_destroy_index = 0

	#统计得分
	score = 0
	score_font = pygame.font.Font(None, 36)

	life_image = pygame.image.load("images/me2.png").convert_alpha()
	life_rect = life_image.get_rect()
	life_num = 3

	#标志是否暂停游戏
	paused = False
	pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
	pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
	resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
	resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
	paused_rect = resume_nor_image.get_rect()
	paused_rect.left, paused_rect.top = width-paused_rect.width-10, 10
	paused_image = resume_nor_image


#生成普通子弹
	bullet1 = []
	bullet1_index = 0
	bullet1_num = 4
	for i in range(bullet1_num):
		bullet1.append(bullet.Bullet1(me.rect.midtop))

#生产超级子弹
	bullet2 = []
	bullet2_index = 0
	bullet2_num = 8
	for i in range(bullet2_num):
		bullet2.append(bullet.Bullet2((me.rect.centerx-20, me.rect.centery)))
		bullet2.append(bullet.Bullet2((me.rect.centerx+20, me.rect.centery)))

	running = True
#用于延迟
	delay = 100

#设置难度等级
	level = 1

	bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
	bomb_rect = bomb_image.get_rect()
	bomb_font = pygame.font.Font(None, 48)
	bomb_num = 3

	#每30s发放一个补给包
	bullet_supply = supply.Bullet_Supply(bg_size)
	bomb_supply = supply.Bomb_Supply(bg_size)
	#用户自定义事件
	SUPPLY_TIME = USEREVENT
	pygame.time.set_timer(SUPPLY_TIME, 30*1000)

	#超级子弹定时器
	DOUBLE_BULLET_TIME = USEREVENT + 1

	#标志是否使用超级子弹
	is_double_bullet = False

	#解除我方无敌 状态定时器
	INVINCIBLE_TIME = USEREVENT + 2


	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
#如果用IDLE打开的话，直接关闭窗口的话 无法关闭，加上这个能关闭窗口
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and paused_rect.collidepoint(event.pos):
					paused = not paused
					if paused:
						#发放包设置为0，取消这个事件
						pygame.time.set_timer(SUPPLY_TIME, 0)
						pygame.mixer.music.pause()#背景音乐暂停
						pygame.mixer.pause()#暂停音效
					else:
						pygame.time.set_timer(SUPPLY_TIME, 30*1000)
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()

			elif event.type == MOUSEMOTION:
				if paused_rect.collidepoint(event.pos):
					if paused:
						pass
					else:
						paused_image = pause_nor_image
				else:
					if paused:
						pass
					else:
						paused_image = resume_nor_image

			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if bomb_num:
						bomb_num -= 1
						for each in enemies:
							if each.rect.bottom > 0:
								each.active = False

			elif event.type == SUPPLY_TIME:
				if choice([True, False]):
					bomb_supply.reset()
				else:
					bullet_supply.reset()

			elif event.type == DOUBLE_BULLET_TIME:
				is_double_bullet = False
				pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

			elif event.type == INVINCIBLE_TIME:
				me.invincible = False
				pygame.time.set_timer(INVINCIBLE_TIME, 0)

		screen.blit(background, (0, 0))

		if level == 1 and score > 5000:
			level = 2
			add_big_enemies(big_enemies, enemies, 1)
			add_mid_enemies(mid_enemies, enemies, 2)
			add_small_enemies(small_enemies, enemies, 3)
			inc_speed(small_enemies, 1)

		if level == 2 and score > 6000000:
			level = 3
			add_big_enemies(big_enemies, enemies, 1)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_small_enemies(small_enemies, enemies, 5)
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)

		if level == 3 and score > 9000000:
			level = 4
			add_big_enemies(big_enemies, enemies, 1)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_small_enemies(small_enemies, enemies, 5)
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)

		if level == 4 and score > 10000000:
			level = 5
			add_big_enemies(big_enemies, enemies, 1)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_small_enemies(small_enemies, enemies, 5)
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)

		if life_num and not paused:
			#检测用户的键盘操作 key_pressed包含所有键盘的布尔值
			key_pressed = pygame.key.get_pressed()

			if key_pressed[K_w] or key_pressed[K_UP]:
				me.moveUp()
			if key_pressed[K_s] or key_pressed[K_DOWN]:
				me.moveDown()
			if key_pressed[K_a] or key_pressed[K_LEFT]:
				me.moveLeft()
			if key_pressed[K_d] or key_pressed[K_RIGHT]:
				me.moveRight()
#绘制全屏炸弹补给并检测
			if bomb_supply.active:
				bomb_supply.move()
				screen.blit(bomb_supply.image, bomb_supply.rect)
				if pygame.sprite.collide_mask(me, bomb_supply):
					if bomb_num < 3:
						bomb_num += 1
					bomb_supply.active = False

			if bullet_supply.active:
				bullet_supply.move()
				screen.blit(bullet_supply.image, bullet_supply.rect)
				if pygame.sprite.collide_mask(me, bullet_supply):
					is_double_bullet = True
					pygame.time.set_timer(DOUBLE_BULLET_TIME, 18*1000)
					bullet_supply.active = False

	#发射子弹
			if not(delay % 10):
				if is_double_bullet:
					bullets = bullet2
					bullets[bullet2_index].reset((me.rect.centerx-20, me.rect.centery))
					bullets[bullet2_index].reset((me.rect.centerx+20, me.rect.centery))
					bullet2_index = (bullet2_index+1)%bullet2_num
				else:
					bullets = bullet1 
					bullets[bullet1_index].reset(me.rect.midtop)
					bullet1_index = (bullet1_index + 1) % bullet1_num

	#检测子弹是否击中敌机
			for b in bullets:
				if b.active:
					b.move()
					screen.blit(b.image, b.rect)
					enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
					if enemy_hit:
						b.active = False
						for e in enemy_hit:
							if e in mid_enemies or e in big_enemies:
								e.energy -= 1
								if e.energy == 0:
									e.active = False
							else:
								e.active = False


	#绘制大型机
			for each in big_enemies:
				if each.active:
					each.move()
					screen.blit(each.image, each.rect)

	#绘制血槽
					pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top-5), (each.rect.right, each.rect.top-5), 2)

					energy_remain = each.energy / enemy.BigEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top-5), (each.rect.left+each.rect.width*energy_remain, each.rect.top-5), 2)

	#即将出现在画面中，播放音效
					if each.rect.bottom > -50 and each.rect.bottom < each.height // 2:
						enemy3_down_sound.play(-1)
	#毁灭
				else:
					screen.blit(each.destroy_images[e3_destroy_index], each.rect)
					e3_destroy_index = (e3_destroy_index + 1) % 1
					if e3_destroy_index == 0:
						score += 10000
						each.reset()

	#绘制中型机
			for each in mid_enemies:
				if each.active:
					each.move()
					screen.blit(each.image, each.rect)
	#绘制血槽
					pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top-5), (each.rect.right, each.rect.top-5), 2)

					energy_remain = each.energy / enemy.MidEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top-5), (each.rect.left+each.rect.width*energy_remain, each.rect.top-5), 2)
	#毁灭
				else:
					screen.blit(each.destroy_images[e2_destroy_index], each.rect)
					e2_destroy_index = (e2_destroy_index + 1) % 1
					if e2_destroy_index == 0:
						score += 6000
						each.reset()

	#绘制小型机
			for each in small_enemies:
				if each.active:
					each.move()
					screen.blit(each.image, each.rect)
	#毁灭
				else:
					screen.blit(each.destroy_images[e1_destroy_index], each.rect)
					e1_destroy_index = (e1_destroy_index + 1) % 1
					if e1_destroy_index == 0:
						score += 1000
						each.reset()
	#检查我方飞机是否被碰撞, 这个函数的第一个参数就是单个精灵，第二个参数是精灵组，第三个参数是一个bool值，当为True的时候，会删除组中所有冲突的精灵，False的时候不会删除冲突的精灵
			enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
			if enemies_down and not me.invincible:
				me.active = False
				for e in enemies_down:
					e.active = False

	#绘制我方飞机
			if me.active:
				screen.blit(me.image, (me.rect.left, me.rect.top))
	#毁灭
			else:
				screen.blit(each.destroy_images[me_destroy_index], each.rect)
				me_destroy_index = (me_destroy_index + 1) % 1
				if me_destroy_index == 0:
					life_num -= 1
					me.reset()
					pygame.time.set_timer(INVINCIBLE_TIME, 3*1000)


#绘制剩余生命的数量
			if life_num:
				for i in range(life_num):
					screen.blit(life_image, (width-10-(i+1)*life_rect.width, height-10-life_rect.height))

			score_text = score_font.render("Score: %s" % str(score), True, WHITE)
			screen.blit(score_text, (10, 5))
			screen.blit(paused_image, paused_rect)

#绘制全屏炸弹
			bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
			text_bomb = rect = bomb_text.get_rect()
			screen.blit(bomb_image, (10, height-10-bomb_rect.width))
			screen.blit(bomb_text, (20+bomb_rect.width, height-5-text_bomb.height))

			if not delay:
				delay = 100
			delay = delay - 1
			pygame.display.flip()
	#一秒钟页面刷新60次,即60帧，即一次while循环是1帧
			clock.tick(60)
		elif life_num == 0:
			print("GAME OVER!")
			running = False

if __name__ == '__main__':
	try:
		main()
#如果正常退出sys.exit()会抛出SystemExit异常，此时什么都不做
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()
		input()











