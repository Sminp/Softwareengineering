"""게임 기본 설정 저장하는 공간. 버튼 클래스나 setting 클래스가 들어가면 좋지
시작화면 및 설정화면"""
from constant import *
import sys
import pygame
import os
import pickle


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Settings:
    def __init__(self):
        # self._screen_width = SCREEN_WIDTH
        # self._screen_height = SCREEN_HEIGHT
        # self.bg_color = WHITE
        # self.font = MALGUNGOTHIC
        # self.player_num = 2
        # self.difficulty = 1

        self.setting = self.get_setting()

    def init_setting(self):
        # 초기값을 setting.pickle에 저장
        init_value = {'screen': [800, 600], 'fullscreen': 0, 'font': MALGUNGOTHIC,
                      'keys': {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "click": pygame.K_KP_ENTER
        },
            'sound': {
                "total": 1,
                "background": 1,
                "effect": 1
        }, 'setting_color': False
        }

        self.set_setting(init_value)

    def set_setting(self, setting: dict):
        with open("setting.pickle", "wb") as f:
            pickle.dump(setting, f)  # 위에서 생성한 dict를 setting.pickle로 저장

    def get_setting(self) -> dict:
        with open("setting.pickle", "rb") as fi:
            setting = pickle.load(fi)

        return setting

    def change_setting(self, change_value: dict):
        self.setting = change_value
        self.set_setting(self.setting)

    # 변화 후 값들

    def window_change(self, size):
        if size == 16:
            self.screen_width = 1280
            self.screen_height = 720

    def sound_volume(self, filename):
        pass

    def reset(self):
        pass

    @property
    def screen_width(self):
        return self._screen_width

    @property
    def screen_height(self):
        return self._screen_height

    @screen_width.setter
    def screen_width(self, value):
        self._screen_width = value

    @screen_height.setter
    def screen_height(self, value):
        self._screen_height = value
