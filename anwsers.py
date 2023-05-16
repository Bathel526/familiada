import pygame

from pygame.sprite import Sprite

class Answer(Sprite):
    def __init__(self, ai_game, text):
        super().__init__()
        self.screen = ai_game.screen
        self.font_path = 'fonts/familiada.ttf'
        self.font = pygame.font.Font(self.font_path, 48)
        self.image = self.font.render(text, True, (255, 255, 0))
        self.rect = self.image.get_rect()

    def update_bottom(self, numbers_group, i):
        number = numbers_group.sprites()[i]
        self.rect.bottom = number.rect.bottom

