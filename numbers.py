import pygame
from pygame.sprite import Sprite

class Number(Sprite):
    def __init__(self, ai_game, text):
        super().__init__()
        self.screen = ai_game.screen
        self.font_path = 'fonts/familiada.ttf'
        self.font = pygame.font.Font(self.font_path, 48)
        self.image = self.font.render(text, True, (255, 255, 0))
        self.rect = self.image.get_rect()