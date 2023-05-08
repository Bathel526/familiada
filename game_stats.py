
class GameStats:
    """Monitorowanie danych statystycznych w grze: ,,Inwazja obcych''."""

    def __init__(self, ai_game):
        """Inicjalizacja danych statystycznych"""

        self.settings = ai_game.settings
        self.reset_stats()
        self.beginning = 0

    def reset_stats(self):
        self.error_left = 0
        self.error_right = 0
        self.suma = 0
        self.game_active = False
        self.first_answer = False
        self.second_answer = False
        self.third_answer = False
        self.fourth_answer = False
        self.fivth_answer = False


