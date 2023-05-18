"""Timer 클래스 game_functions에 부가적으로 필요한 클래스입니다."""
import pygame
import constant as c
import settings as s
import rect_functions as rf


class Timer:
    def __init__(self):
        self.current_time = 0
        self.settings = s.Settings().get_setting()
        self.screen = pygame.display.set_mode(
            (self.settings['screen']), flags=self.settings['fullscreen'])
        self.size = (self.settings['screen'])
        self.text_pos = (self.size[0] * 9 / 10, self.size[1] * 1 / 10)
        self.text = []
        self.start_time = 0
        self.set_tmr()

    def set_tmr(self):
        for i in range(0, 11):
            text = rf.TextRect(self.screen, str(i), 30, c.WHITE)
            self.text.append(text)

    def reset_tmr(self):
        self.start_time = pygame.time.get_ticks()

    def show_tmr(self, turn):
        if turn != 0:
            return 0
        self.text[10 - self.current_time].show(self.text_pos)

    def tick_tmr(self) -> bool:
        self.current_time = (pygame.time.get_ticks() - self.start_time) // 1000
        if self.current_time >= c.TIME:
            self.current_time = 0
            self.reset_tmr()
            return False
