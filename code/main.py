import pygame,sys,time
from settings import *
from sprites import Player

class Game:
    def __init__(self):
        
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Brick Break Game')

        #background
        self.backgorund = self.create_background()

        self.all_sprites = pygame.sprite.Group()

        self.player = Player(self.all_sprites)
    
    def create_background(self):
        background_original = pygame.image.load('../graphics/other/background.jpg').convert()
        height_w = WINDOW_HEIGHT * (WINDOW_HEIGHT/ background_original.get_height())
        width_w = WINDOW_WIDTH * (WINDOW_WIDTH/ background_original.get_width())
        scale_background = pygame.transform.scale(background_original,(width_w,height_w))
        return scale_background


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
            
            self.all_sprites.update(dt)

            self.display_surface.blit(self.backgorund,(0,0))
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

if __name__ == '__main__': #this method was took from class material
    game = Game()
    game.run()