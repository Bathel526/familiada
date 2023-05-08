import sys

from time import sleep

import csv

import pygame

from settings import Settings
from button import Button
from numbers import Number
from anwsers import Answer
from game_stats import GameStats
from points import Point
from suma import Sum
from errors import Error

class Familiada():

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.image = pygame.image.load('pictures/tlo.bmp')
        self.screen_rect = self.image.get_rect()
        self.settings.screen_height = self.image.get_rect().height
        self.settings.screen_width = self.image.get_rect().width
        pygame.display.set_caption(self.settings.caption)

        self.pop_odp_sound = pygame.mixer.Sound('sounds/pop_odp.wav')
        self.err_odp_sound = pygame.mixer.Sound('sounds/err_odp.wav')
        self.next_round_sound = pygame.mixer.Sound('sounds/next_round.wav')
        self.beginning = pygame.mixer.Sound('sounds/beginning.mp3')

        self.stats = GameStats(self)

        self.file = open('data/baza.txt', 'r')

        self.numbers = pygame.sprite.Group()
        self.answers = pygame.sprite.Group()
        self.points = pygame.sprite.Group()

        self.errors_left = pygame.sprite.Group()
        self.errors_right = pygame.sprite.Group()
        self.play_button = Button(self, "MOSTOLIADA")

        self.suma = Sum(self)

        self.game_active = False

    def _create_numbers(self, row):
        number = Number(self, '0')
        number_width, number_height = number.rect.size
        for i in range(1, int(len(row))):
            number = Number(self, str(i)+'.')
            number.rect.left = 270
            number.rect.centery = 200 + ( 2 * number_height * (i - 1))
            self.numbers.add(number)

    def _create_answers(self, f):
        try:
            reader = csv.reader(f)
            row = next(reader)

            self._create_numbers(row)

            question = Answer(self, str(row[0]))
            self.answers.add(question)
            question.rect.left = 350
            question.rect.top = 60
            print('--------------------------')
            print(row[0])
            for i in range (1, int(len(row))):
                result = [ ' '.join(row[i].split()[:-1]), int(row[i].split()[-1]) ]
                answer = Answer(self, str(result[0]))
                answer.rect.left = 340
                answer.update_bottom(self.numbers, (i-1))
                self.answers.add(answer)
                print(f'{i}: {result[0]}, {result[1]}')
                self._create_points(row)
            print('\np -rozpocznij gre\n'
                  'a -pokaz pozostale odpowiedzi\n'
                  'r -zla odpowiedz prawa druzyna\n'
                  'l - zla odpowiedz lewa druzyna\n'
                  'n - nastepna runda\n'
                  'q - wyjdz\n')

        except StopIteration:
            print('Nie ma wiecej wierszy w pliku!!!')
            self.close_file()

    def _create_points(self, row):
        for i in range(1, int(len(row))):
            result = [' '.join(row[i].split()[:-1]), int(row[i].split()[-1])]
            point = Point(self, str(result[1]))
            point.rect.right = 1550
            point.update_bottom(self.numbers, (i - 1))
            self.points.add(point)

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.close_file()
                    sys.exit()
                elif event.key == pygame.K_1:
                    if self.game_active and int(len(self.numbers)) >= 1:
                        if not self.stats.first_answer:
                            self.stats.suma += int(self.points.sprites()[0].number)
                            self.pop_odp_sound.play()
                        self.stats.first_answer = True
                elif event.key == pygame.K_2:
                    if self.game_active and int(len(self.numbers)) >= 2:
                        if not self.stats.second_answer:
                            self.stats.suma += int(self.points.sprites()[1].number)
                            self.pop_odp_sound.play()
                        self.stats.second_answer = True
                elif event.key == pygame.K_3:
                    if self.game_active and int(len(self.numbers)) >= 3:
                        if not self.stats.third_answer:
                            self.stats.suma += int(self.points.sprites()[2].number)
                            self.pop_odp_sound.play()
                        self.stats.third_answer = True
                elif event.key == pygame.K_4:
                    if self.game_active and int(len(self.numbers)) >= 4:
                        if not self.stats.fourth_answer:
                            self.stats.suma += int(self.points.sprites()[3].number)
                            self.pop_odp_sound.play()
                        self.stats.fourth_answer = True
                elif event.key == pygame.K_5:
                    if self.game_active and int(len(self.numbers)) >= 5:
                        if not self.stats.fivth_answer:
                            self.stats.suma += int(self.points.sprites()[4].number)
                            self.pop_odp_sound.play()
                        self.stats.fivth_answer = True
                elif event.key == pygame.K_n:
                    if self.game_active:
                        self.next_round_sound.play()
                        sleep(4)
                        self._start_game()
                elif event.key == pygame.K_a:
                    if self.game_active:
                        self.show_answers()
                elif event.key == pygame.K_r:
                    if self.game_active:
                        self.add_error_right()
                elif event.key == pygame.K_l:
                    if self.game_active:
                        self.add_error_left()
                elif event.key == pygame.K_p:
                    self._start_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def add_error_right(self):
        if self.stats.error_right < self.settings.errors_allowed:
            error = Error(self)
            y = 810
            x = 1750
            if self.stats.error_right:
                for i in range(len(self.errors_right)+1):
                    y = 810 - (270 * i)
            self.stats.error_right += 1
            error.rect.centerx = x
            error.rect.centery = y
            self.errors_right.add(error)
            self.err_odp_sound.play()

    def add_error_left(self):
        if self.stats.error_left < self.settings.errors_allowed:
            error = Error(self)
            y = 810
            x = 150
            if self.stats.error_left:
                for i in range(len(self.errors_left)+1):
                    y = 810 - (270 * i)
            self.stats.error_left += 1
            error.rect.centerx = x
            error.rect.centery = y
            self.errors_left.add(error)
            self.err_odp_sound.play()

    def show_answers(self):
        self.stats.game_active = True
        if int(len(self.answers)) >= 6:
            self.stats.first_answer = True
            self.stats.second_answer = True
            self.stats.third_answer = True
            self.stats.fourth_answer = True
            self.stats.fivth_answer = True
        if int(len(self.answers)) >= 5:
            self.stats.first_answer = True
            self.stats.second_answer = True
            self.stats.third_answer = True
            self.stats.fourth_answer = True
        if int(len(self.answers)) >= 4:
            self.stats.first_answer = True
            self.stats.second_answer = True
            self.stats.third_answer = True
        if int(len(self.answers)) >= 3:
            self.stats.first_answer = True
            self.stats.second_answer = True
        if int(len(self.answers)) >= 2:
            self.stats.first_answer = True

    def _check_play_button(self, mouse_pos):
        """
        Rozpoczecie nowej gry po kliknieciu przycisku Gra przez
        uzytkownika
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()

    def close_file(self):
        self.file.close()
        sleep(0.5)
        sys.exit()

    def _start_game(self):
        self.game_active = True

        self.stats.reset_stats()

        self.numbers.empty()
        self.errors_right.empty()
        self.errors_left.empty()
        self.answers.empty()
        self.points.empty()

        self._create_answers(self.file)

        pygame.mouse.set_visible(False)


    def _update_screen(self):
        self.screen.blit(self.image, self.screen_rect)
        if not self.game_active:
            if self.stats.beginning == 0:
                self.stats.beginning += 1
                self.beginning.play()
            self.play_button.draw_button()
        else:
            self.numbers.draw(self.screen)
            self.errors_left.draw(self.screen)
            self.errors_right.draw(self.screen)

            question = self.answers.sprites()[0]
            self.screen.blit(question.image, question.rect)

            self.suma.prep_sum()

            if self.stats.first_answer:
                answer_1 = self.answers.sprites()[1]
                self.screen.blit(answer_1.image, answer_1.rect)

                point_1 = self.points.sprites()[0]
                self.screen.blit(point_1.image, point_1.rect)
            if self.stats.second_answer:
                answer_2 = self.answers.sprites()[2]
                self.screen.blit(answer_2.image, answer_2.rect)

                point_2 = self.points.sprites()[1]
                self.screen.blit(point_2.image, point_2.rect)
            if self.stats.third_answer:
                answer_3 = self.answers.sprites()[3]
                self.screen.blit(answer_3.image, answer_3.rect)

                point_3 = self.points.sprites()[2]
                self.screen.blit(point_3.image, point_3.rect)
            if self.stats.fourth_answer:
                answer_4 = self.answers.sprites()[4]
                self.screen.blit(answer_4.image, answer_4.rect)

                point_4 = self.points.sprites()[3]
                self.screen.blit(point_4.image, point_4.rect)
            if self.stats.fivth_answer:
                answer_5 = self.answers.sprites()[5]
                self.screen.blit(answer_5.image, answer_5.rect)

                point_5 = self.points.sprites()[4]
                self.screen.blit(point_5.image, point_5.rect)
        pygame.display.flip()

if __name__ == '__main__':
    ai = Familiada()
    ai.run_game()