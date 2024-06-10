import pygame,sys,time
from settings import *
from sprites import Player, Ball, Block, Upgrade
from surfacemaker import SurfaceMaker
from random import choice

class Game:
    def __init__(self):
        
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Brick Break Game')

        #background
        self.backgorund = self.create_background()

        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()

        self.surfacemaker = SurfaceMaker()
        self.player = Player(self.all_sprites,self.surfacemaker)
        self.stage_setup()
        self.ball = Ball(self.all_sprites,self.player,self.block_sprites)
        self.heart_surf = pygame.image.load('../graphics/other/heart.png').convert_alpha()
        self.heart_surf = pygame.transform.scale(self.heart_surf, (30, 27))
    
    def create_upgrade(self,pos):
        upgrade_type = choice(UPGRADES)
        Upgrade(pos,upgrade_type,[self.all_sprites,self.upgrade_sprites])

    def create_background(self):
        background_original = pygame.image.load('../graphics/other/background.jpg').convert()
        height_w = WINDOW_HEIGHT * (WINDOW_HEIGHT/ background_original.get_height())
        width_w = WINDOW_WIDTH * (WINDOW_WIDTH/ background_original.get_width())
        scale_background = pygame.transform.scale(background_original,(width_w,height_w))
        return scale_background

    def stage_setup(self):
        for index_row,row in enumerate(BLOCK_MAP):
            for index_col, col in enumerate(row):
                if col != ' ':
                    y = TOP_OFFSET + index_row * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE//2
                    x =  index_col * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE//2
                    Block(col,(x,y),[self.all_sprites,self.block_sprites],self.surfacemaker,self.create_upgrade)
        
    def display_hearts(self):
        for i in range(self.player.hearts):
            x = i * self.heart_surf.get_width()
            self.display_surface.blit(self.heart_surf,(x,4))

    #game loop was partly took from https://nimbusintelligence.com
    def run(self):
        last_time = time.time()
        while True:

            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.player.hearts <= 0:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True
            
            self.all_sprites.update(dt)

            self.display_surface.blit(self.backgorund,(0,0))
            self.all_sprites.draw(self.display_surface)
            self.display_hearts()

            pygame.display.update()

if __name__ == '__main__': #this method was took from class material
    game = Game()
    game.run()