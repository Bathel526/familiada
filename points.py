import pygame

from pygame.sprite import Sprite

class Point(Sprite):
    def __init__(self, ai_game, number):
        super().__init__()
        self.screen = ai_game.screen
        self.font_path = 'fonts/DOTMATRI.ttf'
        self.font = pygame.font.Font(self.font_path, 64)
        self.number = str(number)
        self.image = self.font.render(number, True, (255, 255, 0))
        self.rect = self.image.get_rect()

    def update_bottom(self, numbers_group, i):
        number = numbers_group.sprites()[i]
        self.rect.bottom = number.rect.bottom