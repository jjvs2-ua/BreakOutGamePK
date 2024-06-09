import pygame
from settings import *
from os import walk

class SurfaceMaker:
    #import graphics 
    def __init__(self):
        for index, info in enumerate(walk('../graphics/blocks')):
            if index == 0:
                self.assets = {color:{} for color in info[1]}
            else:
                for image_name in info[2]:
                    color_type = list(self.assets.keys())[index-1]
                    full_path = '../graphics/blocks' + f'/{color_type}/' + image_name
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.assets[color_type][image_name.split('.')[0]] = surf
        
    #create a surface and return an image
    def get_surf(self,block_type,size):
        image = pygame.Surface(size)
        sides = self.assets[block_type]

        #4 corners
        image.blit(sides['topleft'],(0,0))
        image.blit(sides['topright'],(size[0] - sides['topright'].get_width() ,0))
        image.blit(sides['bottomright'],(size[0] - sides['bottomright'].get_width() ,size[1] - sides['bottomright'].get_height()))
        image.blit(sides['bottomleft'],(0 ,size[1] - sides['bottomleft'].get_height()))
        #top side
        top_width = size[0] - (sides['topleft'].get_width() + sides['topright'].get_width())
        scaled_top_surf = pygame.transform.scale(sides['top'],(top_width,sides['top'].get_height()))
        image.blit(scaled_top_surf,(sides['topleft'].get_width(),0))
        #bottom side
        bottom_width = size[0] - (sides['bottomleft'].get_width() + sides['bottomright'].get_width())
        scaled_bottom_surf = pygame.transform.scale(sides['bottom'],(bottom_width,sides['bottom'].get_height()))
        image.blit(scaled_bottom_surf,(sides['bottomleft'].get_width(),size[1] - sides['bottomleft'].get_height()))

        #center color
        


        return image