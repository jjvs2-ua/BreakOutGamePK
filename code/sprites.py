from typing import Any
import pygame
from random import choice
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, surfacemaker):
        super().__init__(groups)

        self.surfacemaker = surfacemaker
        self.image = surfacemaker.get_surf('player', (WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        # self.image = pygame.Surface((WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
       # self.image.fill((52, 235, 216))

        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20 ))
        self.old_rect = self.rect.copy()
        self.direction  = pygame.math.Vector2()
        self.speed = 300
        self.position = pygame.math.Vector2(self.rect.topleft)


    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def screen_constraint(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.position.x = self.rect.x

        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = self.rect.x


    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.position.x)
        self.screen_constraint()
        
class Ball(pygame.sprite.Sprite):

    def __init__(self,groups,player,blocks):
        super().__init__(groups)

        #collision
        self.player = player
        self.blocks = blocks
        self.image = pygame.image.load('../graphics/other/ball.png').convert_alpha()

        self.image = pygame.transform.scale(self.image, (32, 32))

        self.rect = self.image.get_rect(midbottom =  player.rect.midtop)
        self.old_rect = self.rect.copy()
        self.direction  = pygame.math.Vector2((choice((1,-1)), -1))
        self.speed = 400
        self.position = pygame.math.Vector2(self.rect.topleft)

        self.active = False
    
    def window_collision(self,direction):
        if direction == 'horizontal':
            if self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
                self.position.x = self.rect.x
                self.direction.x *= -1

            if self.rect.left < 0:
                self.rect.left = 0
                self.position.x = self.rect.x
                self.direction.x *= -1

        if direction == 'vertical':
            if self.rect.bottom > WINDOW_HEIGHT:
                self.active = False
            if self.rect.top < 0:
                self.rect.top = 0
                self.position.y = self.rect.y
                self.direction.y *= -1

    def collision(self,direction):
        pass
        overlap_spr = pygame.sprite.spritecollide(self,self.blocks,False)
        if self.rect.colliderect(self.player.rect):
            overlap_spr.append(self.player)
        
        if overlap_spr:
            if direction == 'horizontal':
                for spr in overlap_spr:
                    if self.rect.right >= spr.rect.left and self.old_rect.right <= spr.old_rect.left:
                        self.rect.right = spr.rect.left -1
                        self.position.x = self.rect.x
                        self.direction.x *= -1

                    if self.rect.left <= spr.rect.right and self.old_rect.left >= spr.old_rect.right:
                        self.rect.left = spr.rect.right +1
                        self.position.x = self.rect.x
                        self.direction.x *= -1
                    
                    if getattr(spr, 'health', None):
                        spr.get_damage(1)

            if direction == 'vertical':
                for spr in overlap_spr:
                    if self.rect.top <= spr.rect.bottom and self.old_rect.top >= spr.old_rect.bottom:
                        self.rect.top = spr.rect.bottom +1
                        self.position.y = self.rect.y
                        self.direction.y *= -1

                    if self.rect.bottom >= spr.rect.top and self.old_rect.bottom <= spr.old_rect.top:
                        self.rect.bottom = spr.rect.top -1
                        self.position.y = self.rect.y
                        self.direction.y *= -1      

                    if getattr(spr, 'health', None):
                        spr.get_damage(1)        

        
 
    def update(self,dt):
        if self.active==True:
            
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            
            #this rect is used to know where de ball was before all the movement
            self.old_rect = self.rect.copy()
            
            self.position.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.position.x) 
            self.collision('horizontal')
            self.window_collision('horizontal')

            self.position.y += self.direction.y * self.speed * dt
            self.rect.y  = round(self.position.y) 
            self.collision('vertical')
            self.window_collision('vertical')
        else:
            self.rect.midbottom = self.player.rect.midtop
            self.position = pygame.math.Vector2(self.rect.topleft)

class Block(pygame.sprite.Sprite):
    def __init__(self,block_type,position,groups,surfacemaker):
        super().__init__(groups)
        self.surfacemaker = surfacemaker
        self.image = self.surfacemaker.get_surf(COLOR_LEGEND[block_type], (BLOCK_WIDTH, BLOCK_HEIGHT))
        #self.image = pygame.Surface((BLOCK_WIDTH,BLOCK_HEIGHT))
        self.rect = self.image.get_rect(topleft = position)
        self.old_rect = self.rect.copy()

        self.health = int(block_type)
    
    def get_damage(self,amount):
        self.health -= amount

        if self.health >0:
            self.image = self.surfacemaker.get_surf(COLOR_LEGEND[str(self.health)], (BLOCK_WIDTH, BLOCK_HEIGHT))
        else:
            self.kill()

