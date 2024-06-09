import pygame,sys,time
from settings import *
from sprites import Player, Ball, Block

class Game:
    def __init__(self):
        
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Brick Break Game')

        #background
        self.backgorund = self.create_background()

        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()

        self.player = Player(self.all_sprites)
        self.stage_setup()
        self.ball = Ball(self.all_sprites,self.player,self.block_sprites)
        
    
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
                    y = index_row * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE//2
                    x = index_col * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE//2
                    Block(col,(x,y),[self.all_sprites,self.block_sprites])
        
    #game loop was partly took from https://nimbusintelligence.com
    def run(self):
        last_time = time.time()
        while True:

            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True
            
            self.all_sprites.update(dt)

            self.display_surface.blit(self.backgorund,(0,0))
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

if __name__ == '__main__': #this method was took from class material
    game = Game()
    game.run()