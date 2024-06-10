import pygame,sys,time
from settings import *
from sprites import Player, Ball, Block, Upgrade, Projectile
from surfacemaker import SurfaceMaker
from random import choice,randint

class Game:
    def __init__(self):
        
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Brick Break Game')


        #background
        self.backgorund = self.create_background()
        self.gameover = self.create_gameOver()
        self.gameOverFlag = False

        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()

        self.surfacemaker = SurfaceMaker()
        self.player = Player(self.all_sprites,self.surfacemaker)
        self.stage_setup()
        self.ball = Ball(self.all_sprites,self.player,self.block_sprites)
        self.heart_surf = pygame.image.load('../graphics/other/heart.png').convert_alpha()
        self.heart_surf = pygame.transform.scale(self.heart_surf, (30, 27))
        self.projectile_surf = pygame.image.load('../graphics/other/projectile.png').convert_alpha()
        self.projectile_surf = pygame.transform.scale(self.projectile_surf, (12, 40))
        self.can_shoot = True
        self.shoot_time = 0

        self.crt = CRT()

        self.laser_sound = pygame.mixer.Sound('../sounds/laser.wav')
        self.laser_sound.set_volume(0.1)
 
        self.powerup_sound = pygame.mixer.Sound('../sounds/powerup.wav')
        self.powerup_sound.set_volume(0.1)
 
        self.laserhit_sound = pygame.mixer.Sound('../sounds/laser_hit.wav')
        self.laserhit_sound.set_volume(0.02)
 
        self.music = pygame.mixer.Sound('../sounds/music.wav')
        self.music.set_volume(0.02)
        self.music.play(loops = -1)

    def create_upgrade(self,pos):
        upgrade_type = choice(UPGRADES)
        Upgrade(pos,upgrade_type,[self.all_sprites,self.upgrade_sprites])

    def create_background(self):
        background_original = pygame.image.load('../graphics/other/background.jpg').convert()
        height_w = WINDOW_HEIGHT * (WINDOW_HEIGHT/ background_original.get_height())
        width_w = WINDOW_WIDTH * (WINDOW_WIDTH/ background_original.get_width())
        scale_background = pygame.transform.scale(background_original,(width_w,height_w))
        return scale_background
    
    def create_gameOver(self):
        background_original = pygame.image.load('../graphics/other/gameover.jpg').convert()
        scale_background = pygame.transform.scale(background_original,(WINDOW_WIDTH,WINDOW_HEIGHT))
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

    def upgrade_collision(self):
        overlap_sprites = pygame.sprite.spritecollide(self.player,self.upgrade_sprites,True)
        for sprite in overlap_sprites:
            self.player.upgrade(sprite.upgrade_type)
            self.powerup_sound.play()

    def create_projectile(self):
        if self.player.laser_amount>0:
            self.laser_sound.play()
        for projectile in self.player.laser_rects:
            Projectile(
                projectile.midtop - pygame.math.Vector2(0,30),
                self.projectile_surf,
                [self.all_sprites, self.projectile_sprites])
    
    def laser_timer(self):
        if pygame.time.get_ticks() - self.shoot_time >= 500:
            self.can_shoot = True

    def projectile_block_collision(self):
        for projectile in self.projectile_sprites:
            overlap_sprites  = pygame.sprite.spritecollide(projectile,self.block_sprites,False)
            if overlap_sprites:
                for sprite in overlap_sprites:
                    sprite.get_damage(1)
                projectile.kill()
                self.laserhit_sound.play()


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
                        if self.can_shoot:
                            self.create_projectile()
                            self.can_shoot = False
                            self.shoot_time = pygame.time.get_ticks()


            self.display_surface.blit(self.backgorund,(0,0))
            self.all_sprites.update(dt)
            self.upgrade_collision()
            self.laser_timer()
            self.projectile_block_collision()
            
            self.all_sprites.draw(self.display_surface)
            self.display_hearts()

            self.crt.draw()

            if self.player.hearts <= 0:
                self.gameOverFlag = True
                self.display_surface.blit(self.gameover,(0,0))
            pygame.display.update()

class CRT:
    def __init__(self):
        vignette = pygame.image.load('../graphics/other/tv.png').convert_alpha()
        self.scaled_vignette = pygame.transform.scale(vignette,(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.create_crt_lines()
 
    def create_crt_lines(self):
        line_height = 4
        line_amount = WINDOW_HEIGHT // line_height
        for line in range(line_amount):
            y = line * line_height
            pygame.draw.line(self.scaled_vignette, (20,20,20), (0,y), (WINDOW_WIDTH,y),1)
 
    def draw(self):
        self.scaled_vignette.set_alpha(randint(30,50))
        self.display_surface.blit(self.scaled_vignette,(0,0))
if __name__ == '__main__': #this method was took from class material
    game = Game()
    game.run()