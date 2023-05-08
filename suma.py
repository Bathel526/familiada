import pygame


class Sum():
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        self.stats = ai_game.stats

        self.text_color = (255, 255, 0)
        self.font_path = 'fonts/DOTMATRI.ttf'
        self.font = pygame.font.Font(self.font_path, 64)
        self.prep_sum()


    def prep_sum(self):
        self.msg = 'Suma:  '
        self.text = f'{self.msg}{self.stats.suma}'
        self.image = self.font.render(self.text, True, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.right = 1550
        self.rect.top = 800
        self.screen.blit(self.image, self.rect)
