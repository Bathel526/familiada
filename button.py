import pygame.font

class Button():
    def __init__(self, ai_game, msg):
        """Inicjalzacja atrybutow przycisku"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # przechowuje kolor podswietlenia i kolor niepodswietlenia xD.

        self.msg = msg
        #zdefiniowanie wymiarow i wlasicwosci przyciskow
        self.width, self.height = 1400, 400
        #self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 0)
        self.font_path = 'fonts/familiada.ttf'
        self.font = pygame.font.Font(self.font_path, 200)

        #utworzenie prostokata przyckisku i wysrodkowanie go
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #komunikat wyswietlany przez przycisk trzeba przygotowac jenokrotnie
        self._prep_msg()

    def _prep_msg(self):
        """
        Umieszczenie komunikatu w wygenerowanym obrazie i wysrodkowanie
        tekstu na przycisku
        """
        self.msg_image = self.font.render(self.msg, True, self.text_color)
        #self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color) #<= podswierlenie przycisku tlo
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #wyswietlenie pustego przycisku, a nastepnie komunikatu na nim
        #self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)