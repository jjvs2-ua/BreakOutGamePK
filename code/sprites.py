from typing import Any
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.Surface((WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        self.image.fill((52, 235, 216))

        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20 ))

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
        self.input()
        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.position.x)
        self.screen_constraint()
        
