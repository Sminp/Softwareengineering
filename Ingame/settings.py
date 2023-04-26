"""게임 기본 설정 저장하는 공간. 버튼 클래스나 setting 클래스가 들어가면 좋지
시작화면 및 설정화면"""
from constant import *
import sys
import pygame
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Settings:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.bg_color = WHITE
        self.font = MALGUNGOTHIC
        self.player_num = 2
        self.difficulty = 1

    # 변화 후 값들
    def window_change(self, size):
        if size == 16:
            self.screen_width = 1280
            self.screen_height = 720

    def sound_volume(self, filename):
        pass

    def reset(self):
        pass

