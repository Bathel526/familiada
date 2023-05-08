import pygame
from pygame.sprite import Sprite

class Error(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('pictures/error.bmp')
        self.rect = self.image.get_rect()