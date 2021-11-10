import pygame

from .constants import SCALE
from .pakk import Pakk
    
class Kaart:
    def __init__(self,mast, väärtus, pos):
        self.kaart = Pakk(mast, väärtus)
        temp_pilt = pygame.image.load(f"img/cards/{väärtus}{mast}.png")
        self.pilt = pygame.transform.scale(temp_pilt, (temp_pilt.get_width()/SCALE, temp_pilt.get_height()/SCALE))
        self.pos = pos

    def get_rekt(self):
        return self.pilt.get_rect()
        
        
    def get_kaart(self, pos):
        pass